#!/usr/bin/env python3
"""Read-only host mechanics. No network, package bootstrap or deletion actions."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys

sys.dont_write_bytecode = True
from runtime import activity, payload


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='verb', required=True)
    sub.add_parser('bind', help='Print the installed payload binding for an approved program')
    for verb, operand in [('read-workflow', 'source'), ('plan-check', 'plan'),
                          ('translate-plan', 'plan')]:
        child = sub.add_parser(verb)
        child.add_argument('--binding', type=Path, required=True)
        child.add_argument(operand)
    audit = sub.add_parser('worktree-audit')
    audit.add_argument('--binding', type=Path, required=True)
    audit.add_argument('--repo', type=Path, required=True)
    audit.add_argument('--sources', type=Path, required=True)
    audit.add_argument('--pr-snapshot', type=Path)
    audit.add_argument('--base', default='refs/remotes/origin/main')
    args = parser.parse_args(argv)
    root = Path(__file__).resolve().parents[1]
    try:
        if args.verb == 'bind':
            print(json.dumps(payload.bind(root), indent=2))
            return 0
        payload.load_binding(root, args.binding.resolve())
        if args.verb == 'read-workflow':
            sys.stdout.buffer.write(payload.workflow(root, args.source))
        elif args.verb == 'translate-plan':
            print(payload.translate(root, args.binding.resolve(), Path(args.plan).read_text()), end='')
        elif args.verb == 'plan-check':
            node = shutil.which('node')
            if not node:
                raise ValueError('Node unavailable; plan validation gate blocked')
            helper = payload.checked_file(root, 'core/pstack/skills/poteto-mode/scripts/check-plan.mjs')
            return subprocess.run([node, str(helper), str(Path(args.plan).resolve())], check=False).returncode
        elif args.verb == 'worktree-audit':
            result = activity.audit(args.repo.resolve(), args.sources, args.pr_snapshot, args.base)
            print(json.dumps(result, indent=2))
            return 0 if result['coverage'] == 'complete' else 2
        return 0
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print('host adapter blocked: ' + str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
