import hashlib
import json
from pathlib import Path
import tarfile

ROOT = Path(__file__).resolve().parents[1]


def metrics(texts):
    chars = sum(len(s) for s in texts)
    return {'bytes': sum(len(s.encode()) for s in texts), 'characters': chars,
            'estimated_tokens_characters_divided_by_4': round(chars / 4, 2)}


def archive_texts(path):
    with tarfile.open(path) as archive:
        members = [m for m in archive.getmembers() if m.isfile() and
                   (m.name.endswith('.md') or m.name.endswith('/agents/openai.yaml'))]
        if len({m.name for m in members}) != len(members):
            raise ValueError('duplicate context archive path')
        return {m.name: archive.extractfile(m).read().decode() for m in members}


def native_baseline(root):
    receipt = json.loads((root / 'docs/CONTEXT-BASELINE.json').read_text())
    path = root / receipt['archive']
    if hashlib.sha256(path.read_bytes()).hexdigest() != receipt['archive_sha256']:
        raise ValueError('context baseline archive drift')
    texts = archive_texts(path)
    if set(texts) != set(receipt['files']):
        raise ValueError('context baseline inventory drift')
    for name, text in texts.items():
        if hashlib.sha256(text.encode()).hexdigest() != receipt['files'][name]['sha256']:
            raise ValueError('context baseline bytes drift: ' + name)
    return texts, receipt['revision']


def inventory(texts, paths):
    paths = sorted(set(paths))
    if any(path not in texts for path in paths):
        raise ValueError('missing modeled context input')
    return {'paths': paths, 'unique_files': len(paths), **metrics([texts[p] for p in paths]),
            'inputs': {p: {'bytes': len(texts[p].encode()),
                          'sha256': hashlib.sha256(texts[p].encode()).hexdigest()} for p in paths}}


def measure(root=ROOT):
    release = archive_texts(root / 'tests/fixtures/release-0.2.0.tar.gz')
    before, before_revision = native_baseline(root)
    current = {p.relative_to(root).as_posix(): p.read_text()
               for p in (root / 'plugin').rglob('*') if p.is_file() and
               (p.suffix == '.md' or p.name == 'openai.yaml')}
    declaration_paths = sorted(p for p in current if p.startswith('plugin/skills/') and p.endswith('/SKILL.md'))
    original_declarations = sorted(p for p in release if p.startswith('plugin/skills/') and p.endswith('/SKILL.md'))
    if declaration_paths != original_declarations or len(declaration_paths) != 50:
        raise ValueError('context declaration inventory changed')
    receipt = json.loads((root / 'docs/upstream/consolidation.json').read_text())
    source_by_destination = {r['destination']: r['source'] for r in receipt['files'] if r['destination']}

    def release_paths(paths):
        selected = set()
        for path in paths:
            source = source_by_destination.get(path)
            core = 'plugin/core/' + source if source else None
            if core in release:
                if (path.endswith('/SKILL.md') and '/principle-' not in path) or path.startswith('plugin/agents/'):
                    selected.add(path)
                selected.add(path if '/principle-' in path else core)
            elif path in release:
                selected.add(path)
            else:
                raise ValueError('missing historical context mapping: ' + path)
        return selected

    always = {'plugin/adapters/host.md', 'plugin/adapters/mobile.md'}
    spec = json.loads((root / 'docs/CONTEXT-SCENARIOS.json').read_text())
    scenarios = {}
    for name, profile in spec['profiles'].items():
        required = {row['path'] for row in profile['required']}
        if len(required) != len(profile['required']) or not {
                'plugin/skills/hugues-mode/SKILL.md', 'plugin/skills/unslop/SKILL.md'} <= required:
            raise ValueError('incomplete or duplicate routing/reply inputs')
        phases = {'plugin/adapters/' + p for p in profile['phase_guidance']}
        for phase in phases:
            if '(' + Path(phase).name + ')' not in current['plugin/adapters/host.md']:
                raise ValueError('phase reference not reachable from mandatory host guidance')
        paths = required | always
        mode_workers = sum(row['count'] for row in profile['workers'] if row['mode_context'])
        worker_floor = {'plugin/skills/hugues-mode/SKILL.md', 'plugin/agents/hugues-agent.md', *always}
        worker_after = worker_floor | {'plugin/adapters/host-workers.md'}
        floor = {}
        for version, texts, names in [('published_0_2', release, release_paths(worker_floor)),
                                     ('native_before', before, worker_floor),
                                     ('candidate', current, worker_after)]:
            item = inventory(texts, names)
            floor[version] = {**item, 'mode_workers': mode_workers,
                'repeated_bytes_floor': item['bytes'] * mode_workers,
                'repeated_estimated_tokens_floor': item['estimated_tokens_characters_divided_by_4'] * mode_workers}
        scenarios[name] = {'scenario': profile['scenario'],
            'published_0_2': inventory(release, release_paths(paths)),
            'native_before': inventory(before, paths),
            'candidate': inventory(current, paths | phases),
            'workers': profile['workers'], 'fresh_mode_worker_floor': floor,
            'complete_execution_tokens': None,
            'unknown_inputs': spec['unknown_inputs']}

    old_paths = ['plugin/skills/hugues-mode/SKILL.md', 'plugin/adapters/host.md',
                 'plugin/adapters/mobile.md', 'plugin/core/pstack/skills/poteto-mode/SKILL.md']
    new_paths = old_paths[:3]
    frontmatter = lambda texts, paths: metrics([texts[p].split('---', 2)[1] for p in paths])
    return {'method': 'UTF-8 bytes; Unicode characters; characters/4 estimate. Deterministic source accounting, not runtime latency or observed host context.',
        'baseline_revision': '509cbec0486c23bb76a943ffec1ea7c7fb553c0f',
        'native_before_revision': before_revision,
        'mode_initial_read_set': {'scope': 'Mode entry and unconditional adapters only, before reply or task-dependent reads. See initial_mode_routing for the route announcement closure.',
            'baseline_paths': old_paths, 'candidate_paths': new_paths,
            'baseline': metrics([release[p] for p in old_paths]),
            'native_before': metrics([before[p] for p in new_paths]),
            'candidate': metrics([current[p] for p in new_paths])},
        'native_frontmatter': {'scope': 'All 50 declared frontmatter blocks, an upper bound; actual native startup exposure is unknown.',
            'baseline': frontmatter(release, original_declarations),
            'native_before': frontmatter(before, declaration_paths),
            'candidate': frontmatter(current, declaration_paths),
            'paths': declaration_paths},
        'codex_policy_metadata': {'scope': 'Additional policy-file bytes, not a claim these files enter model context.',
            'native_before': inventory(before, [p for p in before if p.endswith('/agents/openai.yaml')]),
            'candidate': inventory(current, [p for p in current if p.endswith('/agents/openai.yaml')])},
        'canonical_skill_bodies': {'scope': 'Whole native SKILL.md files, metadata included; separate from invocation closure.',
            'native_before': inventory(before, declaration_paths), 'candidate': inventory(current, declaration_paths),
            'workflow_body_only_before': metrics([before[p].split('---', 2)[2] for p in declaration_paths]),
            'workflow_body_only_candidate': metrics([current[p].split('---', 2)[2] for p in declaration_paths]),
            'mode_full_file': inventory(current, ['plugin/skills/hugues-mode/SKILL.md']),
            'mode_workflow_body_only': metrics([current['plugin/skills/hugues-mode/SKILL.md'].split('---', 2)[2]]),
            'unchanged_files': sum(before[p] == current[p] for p in declaration_paths)},
        'scenarios': scenarios, 'worker_accounting': spec['worker_accounting'],
        'public_skills': len(declaration_paths),
        'limits': ['No runtime host, tokenizer, prompt framing, cache or native invocation observation.',
                   'Required transitive bundled reads are included for the stated scenarios even if invocation would hold.',
                   'External skills, consumer inputs and generated evidence have unknown size; no complete workflow token total is claimed.',
                   'Unique inventories do not count repeated loads in fresh workers; the separate floor is partial and not additive.',
                   'Mobile, investigation categories, retries and task-designed large programs require different closures.',
                   'Static scenario accounting needs review when instructions or assumptions change.']}


if __name__ == '__main__':
    print(json.dumps(measure(), indent=2))
