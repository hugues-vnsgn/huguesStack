#!/usr/bin/env python3
"""Read-only upstream inventory, deterministic deltas and responsibility proposals."""
import argparse
import base64
import copy
import csv
from datetime import datetime, timezone
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import tempfile

REPOSITORY = 'https://github.com/cursor/plugins'
PREFIX = 'pstack/'
ROOT = Path(__file__).resolve().parents[1]
DISPOSITIONS = {'port verbatim', 'port with adaptation', 'ignore with reason', 'pending'}
STATES = {'present', 'planned', 'deferred', 'external', 'not planned', 'pending'}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def unique(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f'duplicate JSON key: {key}')
        result[key] = value
    return result


def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8'), object_pairs_hook=unique)


def encode(value):
    return (json.dumps(value, indent=2, ensure_ascii=False) + '\n').encode()


def oid(kind, data):
    return hashlib.sha1(f'{kind} {len(data)}\0'.encode() + data).hexdigest()


def sha(value, length=40):
    require(isinstance(value, str) and re.fullmatch(f'[0-9a-f]{{{length}}}', value), 'invalid object digest')
    return value


def safe_path(value):
    require(isinstance(value, str) and value.startswith(PREFIX), 'expected pstack path')
    require(value == str(PurePosixPath(value)) and '..' not in PurePosixPath(value).parts
            and not any(c in value for c in '\\\n\r\t`|\0'), 'unsafe upstream path')
    return value


def destination_path(value):
    require(isinstance(value, str) and value and not PurePosixPath(value).is_absolute()
            and value == str(PurePosixPath(value)) and '..' not in PurePosixPath(value).parts
            and not any(c in value for c in '\\\n\r\t\0'), 'unsafe destination path')
    return value


def git(repo, *args):
    env = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1', GIT_TERMINAL_PROMPT='0')
    result = subprocess.run(['git', '-C', str(repo), *args], env=env, capture_output=True, check=True)
    return result.stdout


def trees(data):
    """Parse raw Git tree bytes (including root siblings without exposing contents)."""
    entries = {}
    offset = 0
    while offset < len(data):
        end = data.index(b'\0', offset)
        mode, name = data[offset:end].split(b' ', 1)
        require(end + 21 <= len(data), 'incomplete tree object')
        require(name not in entries, 'duplicate tree entry')
        entries[name] = (mode.decode(), data[end + 1:end + 21].hex())
        offset = end + 21
    return entries


def inventory_tree(files):
    root = {}
    for item in files:
        path = safe_path(item['path'])[len(PREFIX):].split('/')
        node = root
        for part in path[:-1]:
            require(part not in node or isinstance(node[part], dict), 'file/directory collision')
            node = node.setdefault(part, {})
        require(path[-1] not in node, 'duplicate or colliding path')
        require(item['mode'] in {'100644', '100755'}, 'unsupported upstream file mode')
        node[path[-1]] = (item['mode'], sha(item['blob_sha']))

    def digest(node):
        entries = []
        for name, value in node.items():
            mode, blob = ('40000', digest(value)) if isinstance(value, dict) else value
            key = name.encode() + (b'/' if isinstance(value, dict) else b'')
            entries.append((key, mode.encode() + b' ' + name.encode() + b'\0' + bytes.fromhex(blob)))
        return oid('tree', b''.join(value for _, value in sorted(entries)))
    return digest(root)


def validate_snapshot(data):
    require(data['schema_version'] == 1 and data['repository'] == REPOSITORY, 'unknown snapshot source/schema')
    commit = base64.b64decode(data['commit_object'], validate=True)
    require(oid('commit', commit) == sha(data['revision']), 'commit object does not match revision')
    tree = base64.b64decode(data['root_tree_object'], validate=True)
    require(commit.startswith(b'tree ' + oid('tree', tree).encode() + b'\n'), 'root tree does not match commit')
    require(trees(tree).get(b'pstack') == ('40000', sha(data['pstack_tree_sha'])), 'pstack tree does not match root')
    files = data['files']
    require(isinstance(files, list) and files and len(files) == data['file_count'], 'incomplete file inventory')
    require([i['path'] for i in files] == sorted(i['path'] for i in files), 'inventory must be path-sorted')
    for item in files:
        sha(item['sha256'], 64)
        require(type(item['size']) is int and item['size'] >= 0, 'invalid blob size')
    require(inventory_tree(files) == data['pstack_tree_sha'], 'incomplete/inconsistent pstack tree')
    manifest = base64.b64decode(data['manifest_object'], validate=True)
    entry = next(i for i in files if i['path'] == 'pstack/.cursor-plugin/plugin.json')
    require(oid('blob', manifest) == entry['blob_sha'] and len(manifest) == entry['size']
            and hashlib.sha256(manifest).hexdigest() == entry['sha256'], 'manifest does not match inventory')
    version = json.loads(manifest, object_pairs_hook=unique)['version']
    require(version == data['version'], 'version does not match manifest')
    date_line = next(line for line in commit.split(b'\n') if line.startswith(b'committer '))
    date = datetime.fromtimestamp(int(date_line.rsplit(b' ', 2)[1]), timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    require(date == data['committed_at_utc'], 'date does not match commit')
    return data


def snapshot(repo, revision):
    resolved = git(repo, 'rev-parse', '--verify', '--end-of-options', revision + '^{commit}').decode().strip()
    sha(resolved)
    commit = git(repo, 'cat-file', 'commit', resolved)
    root_sha = commit.split(b'\n', 1)[0].split(b' ')[1].decode()
    root_tree = git(repo, 'cat-file', 'tree', root_sha)
    subtree = trees(root_tree)[b'pstack'][1]
    files = []
    manifest = None
    for record in git(repo, 'ls-tree', '-rz', '--full-tree', resolved, '--', 'pstack/').split(b'\0'):
        if not record:
            continue
        header, path = record.split(b'\t', 1)
        mode, kind, blob = header.decode().split(' ')
        require(kind == 'blob' and mode in {'100644', '100755'}, 'unsupported entry in pstack tree')
        body = git(repo, 'cat-file', 'blob', blob)
        require(oid('blob', body) == blob, 'corrupt Git blob')
        name = path.decode('utf-8')
        files.append({'path': name, 'mode': mode, 'blob_sha': blob, 'size': len(body),
                      'sha256': hashlib.sha256(body).hexdigest()})
        if name == 'pstack/.cursor-plugin/plugin.json':
            manifest = body
    require(manifest is not None, 'missing pstack manifest')
    date = git(repo, 'show', '-s', '--format=%ct', resolved).decode().strip()
    data = {'schema_version': 1, 'repository': REPOSITORY, 'revision': resolved,
            'version': json.loads(manifest)['version'],
            'committed_at_utc': datetime.fromtimestamp(int(date), timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
            'pstack_tree_sha': subtree, 'file_count': len(files),
            'commit_object': base64.b64encode(commit).decode(),
            'root_tree_object': base64.b64encode(root_tree).decode(),
            'manifest_object': base64.b64encode(manifest).decode(),
            'files': sorted(files, key=lambda i: i['path'])}
    return validate_snapshot(data)


def changes(before, after):
    require(before['repository'] == after['repository'], 'source mismatch')
    old = {i['path']: i for i in before['files']}
    new = {i['path']: i for i in after['files']}
    result = []
    for path in sorted(old.keys() | new.keys()):
        left, right = old.get(path), new.get(path)
        if left is None or right is None or (left['blob_sha'], left['mode']) != (right['blob_sha'], right['mode']):
            result.append({'path': path, 'change': 'added' if left is None else 'removed' if right is None else 'changed',
                           'before': left, 'after': right})
    return result


def decision(row, allow_pending):
    require(row['disposition'] in DISPOSITIONS, 'invalid disposition')
    require(allow_pending or row['disposition'] != 'pending', 'untriaged responsibility')
    require(isinstance(row['reason'], str) and row['reason'].strip(), 'missing triage reason')
    require(row['implementation_state'] in STATES, 'invalid implementation state')
    require(row['release_target'] in {'0.1.0', '0.2', 'not planned', 'pending'}, 'invalid release target')
    require(isinstance(row['destinations'], list) and all(isinstance(p, str) and p for p in row['destinations']), 'invalid destinations')
    for path in row['destinations']:
        destination_path(path)
    require(row['implementation_state'] != 'present' or row['destinations'], 'present responsibility needs a destination')
    if row['path'].startswith('pstack/skills/principle-'):
        require(row['disposition'] in {'port verbatim', 'pending'}, 'principles must be ported verbatim')


def validate_ledger(data, source, allow_pending=False):
    require(data['schema_version'] == 1 and data['repository'] == REPOSITORY
            and data['revision'] == source['revision'], 'ledger does not match source pin')
    expected = {i['path']: i for i in source['files']}
    rows = data['items']
    require([r['path'] for r in rows] == sorted(expected), 'ledger must cover every source path exactly once')
    for row in rows:
        entry = expected[row['path']]
        require(all(row[k] == entry[k] for k in ('mode', 'blob_sha', 'sha256', 'size')), 'stale ledger fingerprint')
        decision(row, allow_pending)
    retired = data.get('retired_items', [])
    require(len({r['path'] for r in retired}) == len(retired), 'duplicate retired responsibility')
    for row in retired:
        safe_path(row['path'])
        require(row['path'] not in expected, 'active responsibility marked retired')
        sha(row['removed_at_revision'])
        decision(row, allow_pending)
    return data


def reconcile(ledger, before, after):
    validate_ledger(ledger, before, allow_pending=True)
    previous = {r['path']: r for r in ledger['items']}
    changed = {r['path'] for r in changes(before, after)}
    result = {'schema_version': 1, 'repository': REPOSITORY, 'revision': after['revision'],
              'items': [], 'retired_items': copy.deepcopy(ledger.get('retired_items', []))}
    revived = {r['path']: r for r in result['retired_items']}
    for item in after['files']:
        row = copy.deepcopy(previous.get(item['path'], revived.get(item['path'], {})))
        prior = {k: row[k] for k in ('disposition', 'reason', 'release_target', 'destinations', 'implementation_state') if k in row}
        row.pop('removed_at_revision', None)
        row.update(item)
        if item['path'] in changed:
            row.update(disposition='pending', reason='Review upstream diff before choosing a disposition.',
                       release_target='pending', destinations=[], implementation_state='pending')
            if prior:
                row['previous_decision'] = prior
        result['items'].append(row)
    active = {r['path'] for r in result['items']}
    result['retired_items'] = [r for r in result['retired_items'] if r['path'] not in active]
    for path in sorted(previous.keys() - active):
        row = copy.deepcopy(previous[path])
        row['removed_at_revision'] = after['revision']
        result['retired_items'].append(row)
    result['retired_items'].sort(key=lambda r: r['path'])
    return validate_ledger(result, after, allow_pending=True)


def render_csv(ledger):
    stream = io.StringIO(newline='')
    fields = ['path', 'mode', 'blob_sha', 'sha256', 'size', 'disposition', 'release_target',
              'implementation_state', 'destinations', 'reason']
    writer = csv.DictWriter(stream, fields, extrasaction='ignore', lineterminator='\n')
    writer.writeheader()
    for row in ledger['items']:
        writer.writerow(dict(row, destinations=';'.join(row['destinations'])))
    return stream.getvalue().encode()


def check_destinations(ledger, source, root):
    for row in ledger['items']:
        if row['implementation_state'] != 'present':
            continue
        for name in row['destinations']:
            path = root / destination_path(name)
            require(path.is_file() and path.resolve().is_relative_to(root.resolve())
                    and not path.is_symlink(), f'missing/unsafe present destination: {name}')
            if row['disposition'] == 'port verbatim':
                body = path.read_bytes()
                require(oid('blob', body) == row['blob_sha']
                        and hashlib.sha256(body).hexdigest() == row['sha256'], f'verbatim destination differs: {name}')
    receipts = load(root / 'docs/upstream/wp2-provenance.json')
    require(receipts['revision'] == source['revision'] and receipts['repository'] == REPOSITORY,
            'WP2 receipts do not match pin')
    files = {row['path']: row for row in ledger['items']}
    for receipt in receipts['files']:
        row = files[receipt['source']]
        require(row['implementation_state'] == 'present' and receipt['destination'] in row['destinations']
                and receipt['blob_sha'] == row['blob_sha'] and receipt['sha256'] == row['sha256'],
                'WP2 receipt does not match reconciled ledger')


def render_delta(before, after, ledger=None):
    rows = changes(before, after)
    triage = {r['path']: r for r in ledger['items'] + ledger.get('retired_items', [])} if ledger else {}
    counts = {kind: sum(r['change'] == kind for r in rows) for kind in ('added', 'changed', 'removed')}
    lines = ['# pstack upstream delta', '', f"Source: {REPOSITORY}", '',
             f"From: {before['version']} `{before['revision']}`", f"To: {after['version']} `{after['revision']}`", '',
             f"{counts['added']} added / {counts['changed']} changed / {counts['removed']} removed.", '',
             'Dispositions are decisions about scope; they do not establish implementation or observed support.',
             'Pending rows require review before re-pinning. Read adapted playbook diffs; never overwrite the fork.', '',
             '| Path | Change | Previous blob / mode | Current blob / mode | Disposition | Reason |',
             '|---|---|---|---|---|---|']
    def cell(value):
        return str(value).replace('&', '&amp;').replace('<', '&lt;').replace('|', '&#124;').replace('\n', ' ').replace('\r', ' ')
    def fingerprint(item):
        return f"{item['blob_sha']} / {item['mode']}" if item else '—'
    for row in rows:
        entry = triage.get(row['path'], {'disposition': 'pending', 'reason': 'Not triaged.'})
        values = [row['path'], row['change'], fingerprint(row['before']), fingerprint(row['after']), entry['disposition'], entry['reason']]
        lines.append('| ' + ' | '.join(cell(v) for v in values) + ' |')
    return ('\n'.join(lines) + '\n').encode()


def read_pin(path):
    path = Path(path)
    pin = load(path)
    require(pin['schema_version'] == 1 and pin['repository'] == REPOSITORY, 'unknown pin source/schema')
    evidence = Path(pin['snapshot'])
    require(not evidence.is_absolute() and '..' not in evidence.parts, 'unsafe snapshot location')
    data = (path.parent / evidence).read_bytes()
    require(hashlib.sha256(data).hexdigest() == pin['snapshot_sha256'], 'snapshot bytes do not match pin')
    source = validate_snapshot(json.loads(data, object_pairs_hook=unique))
    for key in ('revision', 'version', 'committed_at_utc', 'file_count', 'pstack_tree_sha'):
        require(pin[key] == source[key], f'pin mismatch: {key}')
    return source


def write_output(path, data, check=False):
    path = Path(path)
    if check:
        require(path.read_bytes() == data, f'generated output differs: {path}')
        return
    require(not path.is_symlink(), 'refusing symlink output')
    try:
        with path.open('xb') as stream:
            stream.write(data)
    except FileExistsError:
        require(path.read_bytes() == data, f'refusing to overwrite existing output: {path}')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    capture = sub.add_parser('snapshot', help='capture verified public Git objects from a local upstream clone')
    capture.add_argument('--repo', type=Path, required=True)
    capture.add_argument('--revision', required=True)
    capture.add_argument('--output', type=Path, required=True)
    capture.add_argument('--check', action='store_true')
    diff = sub.add_parser('diff', help='compare the pin with upstream main, or a verified offline snapshot')
    diff.add_argument('--pin', type=Path, default=ROOT / 'docs/upstream/pin.json')
    diff.add_argument('--from-snapshot', type=Path, help='historical comparison instead of current pin')
    diff.add_argument('--to-snapshot', type=Path, help='omit to fetch public upstream main into temporary storage')
    diff.add_argument('--ledger', type=Path)
    diff.add_argument('--output', type=Path)
    diff.add_argument('--check', action='store_true')
    rec = sub.add_parser('reconcile', help='write a separate pending ledger proposal; never change the pin or plugin')
    rec.add_argument('--from-snapshot', type=Path, required=True)
    rec.add_argument('--to-snapshot', type=Path, required=True)
    rec.add_argument('--ledger', type=Path, required=True)
    rec.add_argument('--output', type=Path, required=True)
    rec.add_argument('--check', action='store_true')
    verify = sub.add_parser('check', help='validate checked-in pin, complete ledger and historical delta')
    verify.add_argument('--root', type=Path, default=ROOT)
    args = parser.parse_args(argv)
    if args.command == 'snapshot':
        write_output(args.output, encode(snapshot(args.repo, args.revision)), args.check)
    elif args.command == 'reconcile':
        before = validate_snapshot(load(args.from_snapshot))
        after = validate_snapshot(load(args.to_snapshot))
        write_output(args.output, encode(reconcile(load(args.ledger), before, after)), args.check)
    elif args.command == 'diff':
        require(not args.check or args.output is not None, '--check requires --output')
        before = validate_snapshot(load(args.from_snapshot)) if args.from_snapshot else read_pin(args.pin)
        if args.to_snapshot:
            after = validate_snapshot(load(args.to_snapshot))
        else:
            with tempfile.TemporaryDirectory(prefix='huguesstack-upstream-') as directory:
                git(directory, 'init', '--bare', '--quiet')
                git(directory, 'fetch', '--quiet', '--no-tags', '--depth=1', REPOSITORY + '.git', 'main')
                after = snapshot(directory, 'FETCH_HEAD')
        ledger = validate_ledger(load(args.ledger), after, allow_pending=True) if args.ledger else None
        data = render_delta(before, after, ledger)
        output = args.output or ROOT / f"docs/upstream/delta-{before['revision'][:8]}-{after['revision'][:8]}.md"
        write_output(output, data, args.check)
        print(f"{len(changes(before, after))} upstream changes; report: {output}")
    else:
        directory = args.root / 'docs/upstream'
        before = read_pin(directory / 'baseline-pin.json')
        after = read_pin(directory / 'pin.json')
        validate_ledger(load(directory / 'baseline-dispositions.json'), before)
        ledger = validate_ledger(load(directory / 'huguesStack-dispositions.json'), after)
        check_destinations(ledger, after, args.root)
        write_output(directory / 'huguesStack-dispositions.csv', render_csv(ledger), check=True)
        name = f"delta-{before['revision'][:8]}-{after['revision'][:8]}.md"
        write_output(directory / name, render_delta(before, after, ledger), check=True)
        print(f"Verified pstack {after['version']}: {after['file_count']} ledger rows; {len(changes(before, after))} historical changes")
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (ValueError, KeyError, TypeError, StopIteration, OSError, subprocess.CalledProcessError) as exc:
        print(f'upstream evidence rejected: {exc}', file=sys.stderr)
        sys.exit(1)
