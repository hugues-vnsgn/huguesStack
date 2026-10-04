import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import sys
from urllib.parse import unquote, urlsplit

supplied_root = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]).absolute()
if supplied_root.is_symlink() or not supplied_root.is_dir():
    print('repository-root: expected existing directory, not symlink', file=sys.stderr)
    sys.exit(1)
root = supplied_root.resolve()
errors = []
def fail(message):
    errors.append(message)
def inside(path, boundary):
    return path.resolve().is_relative_to(boundary.resolve())
def local(base, value, label):
    if not isinstance(value, str) or not value.startswith('./'):
        fail(f'{label}: expected ./ relative path')
        return None
    parts = PurePosixPath(value).parts
    if '\\' in value or '..' in parts or '$' in value or '%' in value:
        fail(f'{label}: unsafe relative path')
        return None
    target = base / value
    if not inside(target, base):
        fail(f'{label}: path escapes root')
        return None
    if not target.exists():
        fail(f'{label}: missing path {value}')
        return None
    return target

def no_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f'duplicate JSON key {key}')
        result[key] = value
    return result

def load(path):
    try:
        value = json.loads(path.read_text(), object_pairs_hook=no_duplicate_keys)
        if not isinstance(value, dict):
            raise ValueError('expected JSON object')
        return value
    except (OSError, ValueError) as exc:
        fail(f'{path.relative_to(root)}: {exc}')
        return {}

# Reject links even inside ignored planning snapshots, before following any files.
for directory, dirs, files in os.walk(root, followlinks=False):
    dirs[:] = [name for name in dirs if name not in {'.git', '__pycache__'}]
    for name in dirs + files:
        path = Path(directory) / name
        if path.is_symlink():
            fail(f'{path.relative_to(root)}: symlinks are forbidden')
if errors:
    print('\n'.join(errors), file=sys.stderr)
    sys.exit(1)

market = load(root / '.claude-plugin/marketplace.json')
standard = load(root / 'plugin/.claude-plugin/plugin.json')
slug = re.compile(r'[a-z0-9]+(?:-[a-z0-9]+)*\Z')
for label, data in [('marketplace', market), ('plugin', standard)]:
    if not isinstance(data.get('name'), str) or not slug.fullmatch(data['name']):
        fail(f'{label}: invalid name')
    if not isinstance(data.get('description'), str) or not data['description'].strip():
        fail(f'{label}: missing description')
    person = data.get('owner' if label == 'marketplace' else 'author')
    if not isinstance(person, dict) or not isinstance(person.get('name'), str) or not person['name'].strip():
        fail(f'{label}: missing owner/author name')
if not re.fullmatch(r'\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?', str(standard.get('version', ''))):
    fail('plugin: invalid version')
if standard.get('license') != 'MIT':
    fail('plugin: expected MIT license')
allowed = {'name', 'version', 'description', 'author', 'license', 'keywords', 'skills', 'agents', 'homepage', 'repository'}
if set(standard) - allowed:
    fail('plugin: unsupported WP1 fields ' + ', '.join(sorted(set(standard) - allowed)))
plugins = market.get('plugins')
if not isinstance(plugins, list) or len(plugins) != 1 or not isinstance(plugins[0], dict):
    fail('marketplace: expected one plugin entry')
else:
    entry = plugins[0]
    if entry.get('name') != standard.get('name'):
        fail('marketplace: plugin name mismatch')
    if entry.get('source') != './plugin':
        fail('marketplace: expected source ./plugin')
    local(root, entry.get('source'), 'marketplace source')

skill_dirs = standard.get('skills')
if isinstance(skill_dirs, str):
    skill_dirs = [skill_dirs]
if not isinstance(skill_dirs, list) or not skill_dirs:
    fail('plugin: expected skill paths')
    skill_dirs = []
found = set()
for value in skill_dirs:
    target = local(root / 'plugin', value, 'skills')
    if target:
        if not target.is_dir():
            fail('skills: expected directory')
        else:
            found.update(target.rglob('SKILL.md'))
if not found:
    fail('plugin: no skills found')
# Every skill shipped under the default location must also be validated.
found.update((root / 'plugin/skills').rglob('SKILL.md'))
for value in standard.get('agents', []) if isinstance(standard.get('agents', []), list) else [standard['agents']]:
    target = local(root / 'plugin', value, 'agents')
    if target and (not target.is_file() or target.suffix != '.md'):
        fail('agents: expected Markdown file')

names, descriptions = set(), set()
for path in sorted(found):
    text = path.read_text(encoding='utf-8')
    match = re.match(r'\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)', text, re.S)
    if not match:
        fail(f'{path.relative_to(root)}: missing frontmatter')
        continue
    fields = {}
    for line in match[1].splitlines():
        if not line.strip() or line.lstrip().startswith('#'):
            continue
        pair = re.fullmatch(r'([a-z][a-z-]*):\s+(.+)', line)
        if not pair:
            fail(f'{path.relative_to(root)}: unsupported frontmatter line; WP1 accepts single-line "key: value" scalars')
            continue
        if pair[1] in fields:
            fail(f'{path.relative_to(root)}: invalid or duplicate frontmatter field')
            continue
        key, value = pair.groups()
        if value.startswith('"'):
            try:
                value = json.loads(value)
            except ValueError:
                fail(f'{path.relative_to(root)}: invalid quoted scalar')
                continue
        elif value.startswith("'"):
            # YAML single quotes escape an apostrophe by doubling it.
            if not re.fullmatch(r"'(?:[^']|'')*'", value):
                fail(f'{path.relative_to(root)}: invalid quoted scalar')
                continue
            value = value[1:-1].replace("''", "'")
        elif value[0] in '|>[{&*!' or ': ' in value or ' #' in value:
            fail(f'{path.relative_to(root)}: unsupported scalar; use quotes')
            continue
        if pair[2] == value:
            if value in {'true', 'false'}:
                value = value == 'true'
            elif value in {'null', '~'}:
                value = None
            elif re.fullmatch(r'[+-]?\d+(?:\.\d+)?', value):
                value = float(value)
        fields[key] = value
    name, description = fields.get('name'), fields.get('description')
    if not isinstance(name, str) or not slug.fullmatch(name) or len(name) > 64 or name != path.parent.name:
        fail(f'{path.relative_to(root)}: name must match skill folder')
    if name in names:
        fail(f'{path.relative_to(root)}: duplicate skill name')
    names.add(name)
    if not isinstance(description, str) or not description.strip() or len(description) > 1024 or description in {'null', 'true', 'false', '~'}:
        fail(f'{path.relative_to(root)}: missing or invalid description')
    elif description.strip().casefold() in descriptions:
        fail(f'{path.relative_to(root)}: duplicate skill description')
    else:
        descriptions.add(description.strip().casefold())
    if 'disable-model-invocation' in fields and not isinstance(fields['disable-model-invocation'], bool):
        fail(f'{path.relative_to(root)}: expected boolean disable-model-invocation')

# Preserve one verbatim upstream reference to a deliberately deferred helper.
# This receipt is bounded to known bytes and cannot allow arbitrary broken links.
deferred_links, deferred_warnings = set(), []
receipt_path = root / 'docs/upstream/wp2-provenance.json'
if receipt_path.exists():
    receipt = load(receipt_path)
    deferred = receipt.get('deferred_links', [])
    expected_source = 'plugin/skills/principle-explain-the-number/SKILL.md'
    expected_target = '../benchmark-checklist/SKILL.md'
    expected_sha256 = '5aac99e7ce0bb1b37e2579acf4fe88c32a1456d9d46afd4a57cfe1df9092e89c'
    expected_pin = 'e43c7ee26e0038c6c1fa8380dd34ce86ff94cb2a'
    if not isinstance(deferred, list) or len(deferred) != 1:
        fail('WP2 deferred link: expected exactly one bounded receipt')
    else:
        row = deferred[0]
        if (not isinstance(row, dict) or
                set(row) != {'source', 'target', 'source_sha256', 'reason'} or
                row.get('source') != expected_source or
                row.get('target') != expected_target or
                row.get('source_sha256') != expected_sha256 or
                not isinstance(row.get('reason'), str) or not row['reason'].strip()):
            fail('WP2 deferred link: invalid source, target, hash or reason')
        elif (receipt.get('repository') != 'https://github.com/cursor/plugins' or
                receipt.get('revision') != expected_pin or
                receipt.get('upstream_version') != '0.15.9'):
            fail('WP2 deferred link: upstream pin mismatch')
        else:
            files = receipt.get('files')
            matches = [item for item in files if isinstance(item, dict) and
                       item.get('destination') == expected_source] if isinstance(files, list) else []
            source = root / expected_source
            if (len(matches) != 1 or matches[0].get('source') !=
                    'pstack/skills/principle-explain-the-number/SKILL.md' or
                    matches[0].get('disposition') != 'verbatim' or
                    matches[0].get('sha256') != expected_sha256):
                fail('WP2 deferred link: missing matching verbatim provenance')
            elif not source.is_file() or hashlib.sha256(source.read_bytes()).hexdigest() != expected_sha256:
                fail('WP2 deferred link: source bytes differ from pinned upstream')
            elif (source.parent / expected_target).exists():
                fail('WP2 deferred link: target is present; remove stale deferral')
            else:
                deferred_links.add((expected_source, expected_target))

# This small link checker covers authored inline and full/collapsed references.
def prose(text):
    text = re.sub(r'^(`{3,}|~{3,}).*?^\1[^\n]*$', '', text, flags=re.M | re.S)
    return re.sub(r'`[^`\n]*`', '', text)
def headings(path):
    counts, anchors = {}, set()
    for title in re.findall(r'^#{1,6}\s+(.+?)\s*#*\s*$', re.sub(r'^(`{3,}|~{3,}).*?^\1[^\n]*$', '', path.read_text(), flags=re.M | re.S), re.M):
        base = re.sub(r'[^\w\- ]', '', title.lower()).replace(' ', '-')
        count = counts.get(base, 0)
        anchors.add(base if count == 0 else f'{base}-{count}')
        counts[base] = count + 1
    return anchors
for path in sorted(root.rglob('*.md')):
    relative = path.relative_to(root)
    if '.git' in relative.parts or relative.parts[:2] == ('docs', 'planning'):
        continue
    text = prose(path.read_text(encoding='utf-8'))
    definitions = dict(re.findall(r'^\s*\[([^\]]+)\]:\s*(\S+)', text, re.M))
    definitions = {key.casefold(): value for key, value in definitions.items()}
    links = re.findall(r'!?\[[^\]\n]*\]\((<[^>]+>|[^\s)]+)(?:\s+"[^"]*")?\)', text)
    links += list(definitions.values())
    for label, reference in re.findall(r'!?\[([^\]\n]+)\]\[([^\]\n]*)\]', text):
        reference = (reference or label).casefold()
        if reference not in definitions:
            fail(f'{relative}: undefined link reference {reference}')
        else:
            links.append(definitions[reference])
    for value in links:
        value = value.removeprefix('<').removesuffix('>')
        parsed = urlsplit(value)
        if parsed.scheme or parsed.netloc:
            if parsed.scheme not in {'https', 'http', 'mailto'} or (not parsed.scheme and parsed.netloc):
                fail(f'{relative}: unsupported link {value}')
            continue
        decoded = unquote(parsed.path)
        if decoded.startswith('/') or '\\' in decoded:
            fail(f'{relative}: absolute local link {value}')
            continue
        target = path.parent / decoded if decoded else path
        if not inside(target, root):
            fail(f'{relative}: link escapes root {value}')
        elif not target.exists():
            if (str(relative), value) in deferred_links:
                deferred_warnings.append(f'DEFERRED: {relative} -> {value} (pstack 0.15.9 helper deferred to 0.2; source bytes verified)')
            else:
                fail(f'{relative}: broken local link {value}')
        elif parsed.fragment and target.suffix == '.md' and unquote(parsed.fragment) not in headings(target):
            fail(f'{relative}: missing heading {value}')
if errors:
    print('\n'.join(errors), file=sys.stderr)
    sys.exit(1)
for warning in sorted(set(deferred_warnings)):
    print(warning)
print(f'PASS: manifests, {len(found)} skill(s), paths and authored Markdown links')
