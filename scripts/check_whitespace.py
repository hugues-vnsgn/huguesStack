from pathlib import Path
import subprocess
import sys
ROOT = Path(__file__).resolve().parents[1]
BASE = '4ae13bbfa81f305cd9ab432bed6cfce8f078f95c'
def main():
    result = subprocess.run(['git', 'diff', '--check', BASE, '--'], cwd=ROOT,
                            capture_output=True, text=True)
    if result.returncode or result.stderr:
        raise ValueError(result.stdout + result.stderr)
    print('PASS: authored whitespace, no exceptions')
if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError) as exc:
        print('whitespace rejected: ' + str(exc), file=sys.stderr)
        sys.exit(1)
