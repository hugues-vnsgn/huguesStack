"""Resolve the approved installed payload, independent of consumer Git refs."""
import hashlib
from .json_input import load_json
from pathlib import Path, PurePosixPath
import shlex
import stat

PIN = 'huguesstack-native-v1'
ANCHORS = {'adapters/runtime/payload.json', 'adapters/runtime/payload.py', 'adapters/host_tools.py'}
MANIFEST_SHA256 = '0854902ed2f3d02758bafd878bfd4f8f211025f16862b4a130429ba71f18ddaa'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def checked_file(root, relative):
    parts = PurePosixPath(relative).parts
    if not parts or '..' in parts or '\\' in relative or PurePosixPath(relative).is_absolute():
        raise ValueError('unsafe payload path')
    path = root
    for part in parts:
        path = path / part
        if path.is_symlink():
            raise ValueError('symlink in installed payload')
    if not path.is_file() or not path.resolve().is_relative_to(root):
        raise ValueError('missing installed payload file: ' + relative)
    return path


def verify(root):
    for name in ANCHORS:
        if stat.S_IMODE(checked_file(root, name).stat().st_mode) != 0o644:
            raise ValueError('installed trust anchor mode drift: ' + name)
    manifest = checked_file(root, 'adapters/runtime/payload.json')
    if digest(manifest) != MANIFEST_SHA256:
        raise ValueError('installed payload manifest differs from approved revision')
    rows = load_json(manifest.read_text())
    if rows['schema_version'] != 2 or rows['revision'] != PIN:
        raise ValueError('installed payload revision differs')
    for row in rows['files']:
        path = checked_file(root, row['path'])
        mode = '100' + format(stat.S_IMODE(path.stat().st_mode), '03o')
        if digest(path) != row['sha256'] or mode != row['mode']:
            raise ValueError('installed workflow bytes/mode drift: ' + row['path'])
    if set(inventory(root, allow_runtime_cache=True)) != {row['path'] for row in rows['files']} | ANCHORS:
        raise ValueError('installed payload inventory differs')
    return rows


def inventory(root, allow_runtime_cache=False):
    files = []
    for path in root.rglob('*'):
        relative = path.relative_to(root).as_posix()
        # Interpreter caches are generated, never workflow inputs.
        if (allow_runtime_cache and relative.startswith('adapters/runtime/__pycache__/')
                and path.suffix == '.pyc' and path.is_file() and not path.is_symlink()):
            continue
        if path.is_symlink() or not (path.is_dir() or path.is_file()):
            raise ValueError('unsafe installed payload entry: ' + relative)
        if path.is_file():
            files.append(relative)
    return sorted(files)


def bind(root):
    verify(root)
    assets = [name for name in inventory(root, allow_runtime_cache=True) if not name.startswith('core/')]
    return {'schema_version': 1, 'revision': PIN, 'payload_sha256': MANIFEST_SHA256,
            'plugin_root': str(root),
            'adapter_sha256': {name: digest(checked_file(root, name)) for name in assets},
            'adapter_modes': {name: stat.S_IMODE(checked_file(root, name).stat().st_mode)
                              for name in assets}}


def load_binding(root, path):
    recorded = load_json(path.read_text())
    if recorded != bind(root):
        raise ValueError('approved installed binding changed; stop and reconcile the program')
    return recorded


def resolve_source(rows, source):
    return rows['legacy_paths'].get(source, source)


def workflow(root, source):
    rows = verify(root)
    source = resolve_source(rows, source)
    if source.endswith('/SKILL.md'):
        raise ValueError('native skill invocation required; a guarded file read grants no invocation permission')
    known = {row['path'] for row in rows['files']}
    if source not in known or not source.endswith('.md'):
        raise ValueError('workflow is not in approved installed payload')
    return checked_file(root, source).read_bytes()


def command(root, binding, verb, operand):
    return shlex.join(['python3', str(root / 'adapters/host_tools.py'), verb,
                       '--binding', str(binding), '--', operand])


def translate(root, binding, text):
    import re
    rows = verify(root)
    known = {row['path'] for row in rows['files'] if row['path'].endswith('.md')}
    known |= {old for old, new in rows['legacy_paths'].items() if new in known}
    helpers = {'pstack/skills/poteto-mode/scripts/check-plan.mjs', 'skills/hugues-mode/scripts/check-plan.mjs'}
    operands = [re.compile(r'(?<![\w./:-])(?:origin/main:)?' + re.escape(source) + r'(?![\w./-])')
                for source in known | helpers]

    joined = re.sub(r'\\\r?\n', '', text)
    if joined != text or '<<' in text:
        raise ValueError('continued commands and heredocs are not supported in bundled plans')

    def fragment(value):
        try:
            words = shlex.split(value)
        except ValueError:
            if 'pstack/' in value or 'skills/' in value:
                raise ValueError('unresolved quoting in plan reference')
            return value
        if any(pattern.search(value) for name in known if name.endswith('/SKILL.md')
               for pattern in [re.compile(r'(?<![\w./:-])(?:origin/main:)?' + re.escape(name) + r'(?![\w./-])')]):
            raise ValueError('native skill invocation required; plan cannot substitute raw skill reads')
        if words and words[-1] in known and words == shlex.split(command(root, binding, 'read-workflow', words[-1])):
            return value
        bundled = any(pattern.search(content) for pattern in operands
                      for content in (value, ' '.join(words)))
        if bundled and re.search(r'[;&|<>$`(){}\[\]*?~]', value):
            raise ValueError('shell syntax is not supported in bundled commands; use a literal standalone command')
        if len(words) == 1 and words[0] in known:
            return command(root, binding, 'read-workflow', words[0])
        if len(words) == 3 and words[:2] == ['git', 'show']:
            revision, separator, source = words[2].partition(':')
            if separator and revision == 'origin/main':
                if source in known:
                    return command(root, binding, 'read-workflow', source)
            else:
                return value
        if len(words) == 2 and words[0] == 'cat' and words[1] in known:
            return command(root, binding, 'read-workflow', words[1])
        if len(words) == 3 and words[0] == 'node' and words[1] in helpers:
            return command(root, binding, 'plan-check', words[2])
        if bundled:
            raise ValueError('unsupported bundled command; use a standalone guarded read')
        return value

    result = []
    standalone = 0
    nonempty = 0
    for line in text.splitlines(keepends=True):
        nonempty += bool(line.strip())
        if '`' in line:
            inline = r'(?<!`)`([^`\n]+)`(?!`)'
            surrounding = re.sub(inline, '', line).strip()
            if fragment(surrounding) != surrounding:
                raise ValueError('mixed bundled command and inline syntax; use a standalone guarded read')
            result.append(re.sub(inline, lambda match: '`' + fragment(match[1]) + '`', line))
        else:
            content = line.strip()
            translated = fragment(content)
            standalone += translated != content
            result.append(line if translated == content else line.replace(content, translated, 1))
    if standalone and standalone != nonempty:
        raise ValueError('standalone command input must contain only supported standalone commands; use inline references in Markdown plans')
    return ''.join(result)
