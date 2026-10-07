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
    """Resolve bundled reads and plain operands; preserve consumer-owned paths."""
    import re
    known = {row['path'] for row in verify(root)['files']}
    helper = 'node pstack/skills/poteto-mode/scripts/check-plan.mjs '
    text = text.replace(helper, shlex.join(['python3', str(root / 'adapters/host_tools.py'),
                                          'plan-check', '--binding', str(binding)]) + ' ')
    def replace(match):
        source = match['source']
        if source not in known:
            raise ValueError('plan references unknown bundled path: ' + source)
        if match['git']:
            workflow(root, source)
            return command(root, binding, 'read-workflow', source)
        return str(checked_file(root, 'core/' + source))
    return re.sub(r"(?P<git>git show origin/main:)?(?<![\w/])(?P<source>pstack/[\w./-]+\.[\w]+)",
                  replace, text)
