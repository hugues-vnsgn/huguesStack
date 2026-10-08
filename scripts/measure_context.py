import json
from pathlib import Path
import tarfile

ROOT = Path(__file__).resolve().parents[1]


def measure(root=ROOT):
    with tarfile.open(root / 'tests/fixtures/release-0.2.0.tar.gz') as archive:
        baseline = {m.name: archive.extractfile(m).read().decode()
                    for m in archive.getmembers() if m.isfile() and m.name.endswith('.md')}
    old_paths = ['plugin/skills/hugues-mode/SKILL.md', 'plugin/adapters/host.md',
                 'plugin/adapters/mobile.md', 'plugin/core/pstack/skills/poteto-mode/SKILL.md']
    new_paths = old_paths[:3]
    def metrics(texts):
        chars = sum(len(s) for s in texts)
        return {'bytes': sum(len(s.encode()) for s in texts), 'characters': chars,
                'estimated_tokens_characters_divided_by_4': round(chars / 4, 2)}
    old_entries = [text for name, text in baseline.items()
                   if name.startswith('plugin/skills/') and name.endswith('/SKILL.md')]
    new_entries = [p.read_text() for p in sorted((root / 'plugin/skills').glob('*/SKILL.md'))]
    return {'method': 'UTF-8 bytes; Unicode characters; characters/4 token estimate; no native context observed',
        'baseline_revision': '509cbec0486c23bb76a943ffec1ea7c7fb553c0f',
        'mode_initial_read_set': {'baseline_paths': old_paths, 'candidate_paths': new_paths,
            'baseline': metrics([baseline[p] for p in old_paths]),
            'candidate': metrics([(root / p).read_text() for p in new_paths])},
        'native_frontmatter': {'baseline': metrics([s.split('---', 2)[1] for s in old_entries]),
                               'candidate': metrics([s.split('---', 2)[1] for s in new_entries])},
        'public_skills': len(new_entries),
        'limits': ['All frontmatter is an upper-bound source measure, not observed startup context.',
                   'Includes full mobile adapter for a conservative comparable read set.',
                   'Phase-specific reference and dependency invocation costs are not included.',
                   'Moving bodies does not itself promise runtime context savings.']}


if __name__ == '__main__':
    print(json.dumps(measure(), indent=2))
