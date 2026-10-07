"""Resolve the approved installed payload, independent of consumer Git refs."""
import hashlib
from .json_input import load_json
from pathlib import Path, PurePosixPath
import shlex
import stat

PIN = 'e43c7ee26e0038c6c1fa8380dd34ce86ff94cb2a'
MANIFEST_SHA256 = 'c42187f44123ed5a6dbdb6bce2f270218c60e515bcec262ebe7315a70d76b364'


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
    manifest = checked_file(root, 'adapters/runtime/payload.json')
    if digest(manifest) != MANIFEST_SHA256:
        raise ValueError('installed payload manifest differs from approved revision')
    rows = load_json(manifest.read_text())
    if rows['revision'] != PIN:
        raise ValueError('installed payload revision differs')
    for row in rows['files']:
        path = checked_file(root, 'core/' + row['path'])
        mode = '100' + format(stat.S_IMODE(path.stat().st_mode), '03o')
        if digest(path) != row['sha256'] or mode != row['mode']:
            raise ValueError('installed workflow bytes/mode drift: ' + row['path'])
    if set(inventory(root / 'core')) != {row['path'] for row in rows['files']}:
        raise ValueError('installed core inventory differs')
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


def workflow(root, source):
    rows = verify(root)
    known = {row['path'] for row in rows['files']}
    if source not in known or not source.endswith('.md'):
        raise ValueError('workflow is not in approved pinned payload')
    return checked_file(root, 'core/' + source).read_bytes()


def command(root, binding, verb, operand):
    return shlex.join(['python3', str(root / 'adapters/host_tools.py'), verb,
                       '--binding', str(binding), operand])


def translate(root, binding, text):
    import re
    known = {row['path'] for row in verify(root)['files'] if row['path'].endswith('.md')}
    helper = 'pstack/skills/poteto-mode/scripts/check-plan.mjs'
    operands = [re.compile(r'(?<![\w./:-])(?:origin/main:)?' + re.escape(source) + r'(?![\w./-])')
                for source in known | {helper}]

    def fragment(value):
        try:
            words = shlex.split(value)
        except ValueError:
            if 'pstack/' in value:
                raise ValueError('unresolved quoting in plan reference')
            return value
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
        if len(words) == 3 and words[:2] == ['node', helper]:
            return command(root, binding, 'plan-check', words[2])
        if bundled:
            raise ValueError('unsupported bundled command; use a standalone guarded read')
        return value

    result = []
    for line in text.splitlines(keepends=True):
        if '`' in line:
            inline = r'(?<!`)`([^`\n]+)`(?!`)'
            surrounding = re.sub(inline, '', line).strip()
            if fragment(surrounding) != surrounding:
                raise ValueError('mixed bundled command and inline syntax; use a standalone guarded read')
            result.append(re.sub(inline, lambda match: '`' + fragment(match[1]) + '`', line))
        else:
            content = line.strip()
            translated = fragment(content)
            result.append(line if translated == content else line.replace(content, translated, 1))
    return ''.join(result)
