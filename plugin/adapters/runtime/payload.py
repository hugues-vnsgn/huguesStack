"""Resolve the approved installed payload, independent of consumer Git refs."""
import hashlib
import json
from pathlib import Path, PurePosixPath
import shlex
import stat

PIN = 'e43c7ee26e0038c6c1fa8380dd34ce86ff94cb2a'
MANIFEST_SHA256 = 'c42187f44123ed5a6dbdb6bce2f270218c60e515bcec262ebe7315a70d76b364'
ASSETS = ('adapters/host.md', 'adapters/host-tools.md', 'adapters/host_tools.py',
          'adapters/runtime/__init__.py', 'adapters/runtime/payload.py',
          'adapters/runtime/activity.py')


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
    rows = json.loads(manifest.read_text())
    if rows['revision'] != PIN:
        raise ValueError('installed payload revision differs')
    for row in rows['files']:
        path = checked_file(root, 'core/' + row['path'])
        mode = '100755' if stat.S_IMODE(path.stat().st_mode) & 0o111 else '100644'
        if digest(path) != row['sha256'] or mode != row['mode']:
            raise ValueError('installed workflow bytes/mode drift: ' + row['path'])
    return rows


def bind(root):
    verify(root)
    return {'schema_version': 1, 'revision': PIN, 'payload_sha256': MANIFEST_SHA256,
            'plugin_root': str(root),
            'adapter_sha256': {name: digest(checked_file(root, name)) for name in ASSETS}}


def load_binding(root, path):
    recorded = json.loads(path.read_text())
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
    """Translate filled bundled operands; consumer-owned Git reads stay intact."""
    import re
    def replace(match):
        source = match[1]
        workflow(root, source)
        return command(root, binding, 'read-workflow', source)
    text = re.sub(r'git show origin/main:(pstack/[^\s`\"<>]+)', replace, text)
    helper = 'node pstack/skills/poteto-mode/scripts/check-plan.mjs '
    return text.replace(helper, shlex.join(['python3', str(root / 'adapters/host_tools.py'),
                                          'plan-check', '--binding', str(binding)]) + ' ')
