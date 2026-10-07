"""Conservative local audit of owner-selected Claude Code and Codex sources."""
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import shlex
import stat
import subprocess

PROVIDERS = {'claude', 'codex'}
PATH_KEYS = {'cwd', 'workdir', 'file_path', 'path', 'absolute_path', 'directory'}
RECENT_SECONDS = 4 * 86400
SIMPLE_COMMANDS = {'cat', 'ls', 'head', 'tail', 'wc', 'stat', 'rg', 'grep',
                   'sed', 'find', 'git', 'pwd', 'readlink', 'realpath'}
PATH_TOOLS = {'Read', 'Write', 'Edit', 'MultiEdit', 'Glob', 'Grep',
              'read_file', 'write_file', 'list_directory'}


def strings(value):
    if isinstance(value, dict):
        for key, child in value.items():
            if key == 'arguments' and isinstance(child, str):
                try:
                    child = json.loads(child)
                except ValueError as exc:
                    raise ValueError('unreadable encoded function arguments') from exc
            yield from strings(child)
    elif isinstance(value, list):
        for child in value:
            yield from strings(child)
    elif isinstance(value, str):
        yield value


def contexts(value, keys=PATH_KEYS):
    if isinstance(value, dict):
        for key, child in value.items():
            if key in keys:
                if child is not None and not isinstance(child, str):
                    raise ValueError('invalid operation path field')
                if child:
                    yield child
            if key == 'arguments' and isinstance(child, str):
                child = json.loads(child)
            yield from contexts(child, keys)
    elif isinstance(value, list):
        for child in value:
            yield from contexts(child, keys)


def shell_paths(command):
    if not isinstance(command, str) or not command.strip():
        raise ValueError('missing shell command')
    # Expansions, compound commands and arbitrary programs cannot be resolved
    # reliably from a transcript. Hold coverage rather than guess their paths.
    if any(char in command for char in '$`*?[]{};|&<>\n\r'):
        raise ValueError('unsupported shell expansion or compound command')
    tokens = shlex.split(command)
    if not tokens or Path(tokens[0]).name not in SIMPLE_COMMANDS:
        raise ValueError('unsupported shell program; activity coverage unavailable')
    paths = []
    directory = Path('.')
    index = 1
    while index < len(tokens):
        token = tokens[index]
        index += 1
        if Path(tokens[0]).name == 'git' and (token == '-C' or token.startswith('-C')):
            if token == '-C':
                if index >= len(tokens):
                    raise ValueError('git -C lacks a directory')
                target = tokens[index]
                index += 1
            else:
                target = token[2:]
            if not target or target.startswith('~'):
                raise ValueError('unsupported git working directory')
            directory = Path(target) if Path(target).is_absolute() else directory / target
            paths.append(str(directory))
            continue
        if token.startswith('-'):
            if token.startswith('-C') and len(token) > 2:
                token = token[2:]
            elif '=' in token:
                token = token.split('=', 1)[1]
            elif '/' in token:
                raise ValueError('unsupported attached shell path option')
            else:
                continue
        if token.startswith('~'):
            raise ValueError('unsupported shell home expansion')
        if token:
            paths.append(str(Path(token) if Path(token).is_absolute() else directory / token))
    return paths


def patch_paths(text):
    if not isinstance(text, str) or not text.startswith('*** Begin Patch\n') or not text.rstrip().endswith('*** End Patch'):
        raise ValueError('unsupported patch envelope')
    paths = re.findall(r'^\*\*\* (?:Add File|Update File|Delete File|Move to): (.+)$', text, re.M)
    if not paths:
        raise ValueError('patch has no operation paths')
    return paths


def local_context(value, inherited):
    result = inherited
    for key in ('cwd', 'workdir'):
        if key not in value or value[key] is None:
            continue
        path = value[key]
        if not isinstance(path, str) or not path:
            raise ValueError('invalid operation working directory')
        if not Path(path).is_absolute() and not result:
            raise ValueError('relative working directory lacks parent context')
        result = str((Path(path) if Path(path).is_absolute() else Path(result) / path).resolve())
    return result


def operation_paths(value, inherited=None):
    """Resolve each native operation in its own enclosing context."""
    if isinstance(value, list):
        for child in value:
            yield from operation_paths(child, inherited)
        return
    if not isinstance(value, dict):
        return
    cwd = local_context(value, inherited)
    kind = value.get('type')
    if kind in {'tool_call', 'tool-call'} or any(key in value for key in ('tool_calls', 'function_call')):
        raise ValueError('unsupported native tool envelope')
    if kind not in {'function_call', 'custom_tool_call', 'tool_use'}:
        for child in value.values():
            yield from operation_paths(child, cwd)
        return
    name = value.get('name')
    if not isinstance(name, str):
        raise ValueError('tool operation lacks a name')
    name = name.rsplit('.', 1)[-1]
    if kind == 'function_call':
        if not isinstance(value.get('arguments'), str):
            raise ValueError('function call lacks encoded arguments')
        args = json.loads(value['arguments'])
        if not isinstance(args, dict):
            raise ValueError('function arguments must decode to an object')
    elif kind == 'tool_use':
        args = value.get('input')
        if not isinstance(args, dict):
            raise ValueError('malformed Claude tool operation')
    else:
        args = {'input': value.get('input')}
        if name != 'apply_patch':
            raise ValueError('unsupported custom tool operation')
    cwd = local_context(args, cwd)
    if name in {'Bash', 'exec_command'}:
        paths = shell_paths(args.get('command') if name == 'Bash' else args.get('cmd'))
    elif name == 'apply_patch':
        paths = patch_paths(args.get('patch') or args.get('input'))
    elif name in PATH_TOOLS:
        paths = list(contexts(args, PATH_KEYS - {'cwd', 'workdir'}))
        if not paths:
            raise ValueError('file operation lacks paths')
    else:
        raise ValueError('unsupported native operation')
    if cwd:
        yield cwd
    for path in paths:
        if not Path(path).is_absolute() and not cwd:
            raise ValueError('relative operation path lacks working-directory context')
        yield str((Path(path) if Path(path).is_absolute() else Path(cwd) / path).resolve())


def touches(value, worktree):
    variants = {str(worktree)}
    # macOS Git canonicalizes /tmp and /var to /private/...; native records may
    # retain those system aliases. Do not miss activity because of spelling.
    for alias in ('/tmp', '/var'):
        canonical = str(Path(alias).resolve())
        if str(worktree).startswith(canonical + '/'):
            variants.add(alias + str(worktree)[len(canonical):])
    patterns = [re.compile(re.escape(path) + r'(?=$|[/\s\"\'`,;:)\]}])') for path in variants]
    return any(pattern.search(text) for text in strings(value) for pattern in patterns)


def timestamp(record, fallback):
    value = record.get('timestamp')
    if value is None:
        return fallback, 'file-mtime-conservative'
    if isinstance(value, bool):
        raise ValueError('invalid transcript timestamp')
    if isinstance(value, (int, float)):
        result = float(value)
    elif isinstance(value, str):
        parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
        if parsed.tzinfo is None:
            raise ValueError('timestamp lacks timezone')
        result = parsed.timestamp()
    else:
        raise ValueError('invalid transcript timestamp')
    if not (0 <= result < 253402300800):
        raise ValueError('invalid transcript timestamp')
    return result, 'record-timestamp'


def records(provider, path, body, mtime):
    if path.suffix != '.jsonl':
        raise ValueError('unsupported transcript format')
    for line in body.splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        if not isinstance(row, dict):
            raise ValueError('transcript record is not an object')
        kind = row.get('type')
        if provider == 'claude':
            supported = kind in {'user', 'assistant', 'system', 'summary',
                                'file-history-snapshot', 'queue-operation'}
            if kind in {'user', 'assistant'}:
                supported = isinstance(row.get('message'), dict) and isinstance(row['message'].get('content'), (str, list))
                content = row['message'].get('content') if isinstance(row.get('message'), dict) else None
                if isinstance(content, list):
                    supported = all(isinstance(item, dict) and item.get('type') in
                                    {'text', 'tool_use', 'tool_result', 'thinking', 'redacted_thinking'}
                                    for item in content)
        elif provider == 'codex':
            supported = kind in {'session_meta', 'response_item', 'event_msg', 'turn_context'} and isinstance(row.get('payload'), dict)
            if kind == 'response_item':
                supported = isinstance(row.get('payload'), dict) and row['payload'].get('type') in {
                    'message', 'function_call', 'function_call_output', 'reasoning',
                    'custom_tool_call', 'custom_tool_call_output', 'web_search_call'}
            if kind == 'event_msg':
                supported = isinstance(row.get('payload'), dict) and row['payload'].get('type') in {
                    'agent_message', 'agent_reasoning', 'user_message', 'task_started',
                    'task_complete', 'token_count', 'turn_aborted', 'context_compacted'}
        else:
            supported = False
        if not supported:
            raise ValueError('unsupported ' + provider + ' record envelope')
        ts, origin = timestamp(row, mtime)
        yield row, ts, origin


def selected_files(source):
    if not isinstance(source, dict):
        raise ValueError('source entry must be an object')
    if set(source) - {'provider', 'root', 'files', 'authorization', 'coverage'}:
        raise ValueError('unknown source fields')
    if source.get('provider') not in PROVIDERS or not isinstance(source.get('authorization'), str) or not source['authorization'].strip():
        raise ValueError('provider and explicit source authorization required')
    if ('root' in source) == ('files' in source):
        raise ValueError('select one source root or explicit file list')
    if 'root' in source:
        root = Path(source['root'])
        if not root.is_absolute() or root.is_symlink() or not root.is_dir():
            raise ValueError('source root unavailable or unsafe')
        files = []
        def failed(exc):
            raise exc
        for directory, dirs, names in os.walk(root, followlinks=False, onerror=failed):
            for name in dirs + names:
                if (Path(directory) / name).is_symlink():
                    raise ValueError('symlink in selected transcript root')
            files.extend(Path(directory) / name for name in names)
        return sorted(files)
    if not isinstance(source['files'], list) or not all(isinstance(p, str) for p in source['files']):
        raise ValueError('source files must be an explicit absolute list')
    files = [Path(p) for p in source['files']]
    if any(not p.is_absolute() for p in files):
        raise ValueError('source files must be absolute')
    return files


def read_selected(path):
    if any(parent.is_symlink() for parent in [path, *path.parents]):
        raise ValueError('symlink in selected transcript path')
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(fd, 'r', encoding='utf-8') as stream:
        before = os.fstat(stream.fileno())
        if not stat.S_ISREG(before.st_mode) or before.st_size > 64 * 1024 * 1024:
            raise ValueError('source must be a regular transcript of at most 64 MiB')
        body = stream.read()
        after = os.fstat(stream.fileno())
        if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
            raise ValueError('transcript changed during scan')
        return body, after.st_mtime


def scan(manifest, worktrees, now):
    activity = {str(p): [] for p in worktrees}
    reports = []
    complete = manifest.get('coverage') == 'complete'
    sources = manifest.get('sources')
    if not isinstance(sources, list) or not sources:
        return activity, [{'coverage': 'unavailable', 'error': 'no authorized transcript sources'}], False
    supported_sources = 0
    for source in sources:
        report = {'provider': source.get('provider') if isinstance(source, dict) else None,
                  'coverage': 'unavailable', 'files_scanned': 0}
        reports.append(report)
        if isinstance(source, dict) and source.get('provider') == 'cursor':
            report.update(coverage='ignored', reason='unsupported host; contributes no Claude/Codex evidence')
            continue
        try:
            files = selected_files(source)
            supported_sources += 1
            for path in files:
                body, mtime = read_selected(path)
                cwd = None
                for row, ts, origin in records(source['provider'], path, body, mtime):
                    # Decode tool arguments even if the record has no direct path.
                    list(strings(row))
                    if row.get('cwd'):
                        cwd = row['cwd']
                    payload = row.get('payload', {})
                    if isinstance(payload, dict) and payload.get('cwd'):
                        cwd = payload['cwd']
                    if cwd and (not isinstance(cwd, str) or not Path(cwd).is_absolute()):
                        raise ValueError('invalid session working directory')
                    normalized = list(operation_paths(row, cwd))
                    for location in contexts(row):
                        if Path(location).is_absolute():
                            normalized.append(str(Path(location).resolve()))
                    for wt in worktrees:
                        hit = (touches(row, wt) or touches(normalized, wt) or
                               any(wt.is_relative_to(Path(p)) for p in normalized) or
                               bool(cwd and touches({'cwd': str(Path(cwd).resolve())}, wt)))
                        if hit:
                            activity[str(wt)].append({'provider': source['provider'], 'source': str(path),
                                                     'timestamp': ts, 'timestamp_basis': origin,
                                                     'recent': now - ts <= RECENT_SECONDS})
                report['files_scanned'] += 1
            report['coverage'] = 'complete' if source.get('coverage') == 'complete' else 'partial'
        except (ValueError, OSError, TypeError, KeyError, UnicodeError) as exc:
            report['error'] = str(exc)
        complete = complete and report['coverage'] == 'complete'
    return activity, reports, complete and supported_sources > 0


def git(repo, *args):
    env = dict(os.environ, GIT_OPTIONAL_LOCKS='0', GIT_TERMINAL_PROMPT='0')
    return subprocess.run(['git', '-c', 'core.fsmonitor=false', '-C', str(repo), *args],
                          env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)


def classify(dirty, pr, merged, coverage, recent):
    if dirty.startswith('wip:'):
        return 'hold-wip'
    if pr == 'OPEN':
        return 'hold-open-pr'
    if not coverage:
        return 'hold-activity-unavailable'
    if recent:
        return 'verify-recent-chat'
    if dirty != 'clean':
        return 'review-scratch' if dirty.startswith('scratch:') else 'hold-metadata-unavailable'
    if pr == 'UNKNOWN' or merged is None:
        return 'hold-metadata-unavailable'
    return 'verify-active-pinned' if merged or pr == 'MERGED' else 'review'


def audit(repo, source_path, pr_path=None, base='refs/remotes/origin/main'):
    listing = git(repo, 'worktree', 'list', '--porcelain', '-z')
    if listing.returncode:
        raise ValueError('consumer worktree list unavailable')
    trees = []
    for block in listing.stdout.decode().split('\0\0'):
        fields = dict(line.split(' ', 1) for line in block.split('\0') if ' ' in line)
        if 'worktree' in fields:
            trees.append((Path(fields['worktree']), fields.get('branch', '').removeprefix('refs/heads/')))
    paths = [p for p, _ in trees]
    try:
        manifest = json.loads(source_path.read_text())
        if not isinstance(manifest, dict) or set(manifest) != {'schema_version', 'coverage', 'sources'} or manifest['schema_version'] != 1:
            raise ValueError('invalid source manifest')
        hits, reports, complete = scan(manifest, paths, datetime.now(timezone.utc).timestamp())
    except (ValueError, OSError, TypeError, UnicodeError) as exc:
        hits, reports, complete = {str(p): [] for p in paths}, [{'coverage': 'unavailable', 'error': str(exc)}], False
    prs = {}
    if pr_path:
        try:
            snapshot = json.loads(pr_path.read_text())
            if snapshot['coverage'] == 'complete' and isinstance(snapshot['states'], dict):
                prs = snapshot['states']
        except (ValueError, OSError, KeyError, TypeError):
            pass
    rows = []
    for index, (wt, branch) in enumerate(trees):
        status = git(wt, 'status', '--porcelain=v1', '-z', '--untracked-files=all')
        entries = [e for e in status.stdout.split(b'\0') if e]
        tracked = sum(not e.startswith(b'?? ') for e in entries)
        dirty = ('unavailable' if status.returncode else 'clean' if not entries else
                 f'wip:{tracked}' if tracked else f'scratch:{len(entries)}')
        merge = git(wt, 'merge-base', '--is-ancestor', 'HEAD', base)
        merged = None if merge.returncode not in (0, 1) else merge.returncode == 0
        pr = prs.get(branch, 'UNKNOWN')
        if pr not in {'OPEN', 'CLOSED', 'MERGED', 'NONE'}:
            pr = 'UNKNOWN'
        evidence = hits[str(wt)]
        recent = any(row['recent'] for row in evidence)
        rows.append({'worktree': str(wt), 'branch': branch, 'main_worktree': index == 0,
                     'dirty': dirty, 'merged_into_local_base': merged, 'pr': pr,
                     'activity': 'recent' if recent else 'no-recent-evidence' if complete else 'unavailable',
                     'evidence': evidence, 'bucket': 'hold-main-worktree' if index == 0 else
                     classify(dirty, pr, merged, complete, recent),
                     'active_pinned_gate': 'required-separately', 'deletion_authorized': False})
    return {'schema_version': 1, 'coverage': 'complete' if complete else 'unavailable',
            'sources': reports, 'local_base': base, 'base_freshness': 'not-fetched',
            'network_used': False, 'deletion_performed': False, 'worktrees': rows}
