"""Require clean authored diffs while preserving four byte-exact upstream warnings."""
from pathlib import Path
import re
import subprocess
import sys

from check_core import check

ROOT = Path(__file__).resolve().parents[1]
BASE = '8f9e9fb63b4d2351b20e247762abc74ed2e50b2e'
EXPECTED = {
    ('plugin/core/pstack/README.md', 5, 'trailing whitespace.'),
    ('plugin/core/pstack/README.md', 13, 'trailing whitespace.'),
    ('plugin/core/pstack/README.md', 245, 'trailing whitespace.'),
    ('plugin/core/pstack/skills/automate-me/SKILL.md', 104, 'new blank line at EOF.'),
}


def warnings(report):
    return [(p, int(n), reason) for p, n, reason in
            re.findall(r'^([^\n:]+):(\d+): ([^\n]+)$', report, re.M)]


def validate(report):
    found = warnings(report)
    if len(found) != 4 or set(found) != EXPECTED:
        raise ValueError('unexpected or missing whitespace diagnostics: ' + repr(found))


def main():
    # Exceptions are valid only while all actual source bytes match the pin.
    check(ROOT)
    result = subprocess.run(['git', 'diff', '--check', BASE, '--'], cwd=ROOT,
                            capture_output=True, text=True)
    if result.returncode != 2 or result.stderr:
        raise ValueError('unexpected Git whitespace result: ' + result.stdout + result.stderr)
    validate(result.stdout)
    print('PASS: authored whitespace; four exact pinned-source warnings preserved')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print('whitespace rejected: ' + str(exc), file=sys.stderr)
        sys.exit(1)
