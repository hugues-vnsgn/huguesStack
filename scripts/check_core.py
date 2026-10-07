"""Verify actual pinned bytes, active workflow wiring and bounded policy overrides."""
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import stat
import sys

from render_core import outputs

ROOT = Path(__file__).resolve().parents[1]
PIN = 'e43c7ee26e0038c6c1fa8380dd34ce86ff94cb2a'
TREE = '54dfdd87fd191ddda7fce01dd354d220adaeeacc'
EXCLUDED = {'automate-me', 'make-bot-ui', 'typescript-best-practices'}
ALIASES = {'poteto-mode': 'hugues-mode', 'setup-pstack': 'setup-huguesstack'}
AGENTS = {
    'poteto-agent': {'source': 'pstack/agents/poteto-agent.md',
                     'entrypoint': 'plugin/agents/hugues-agent.md'},
    'Comment Sicko': {'source': 'pstack/agents/comment-sicko.md',
                      'entrypoint': 'plugin/agents/hugues-comment-sicko.md'},
}
ADAPTERS = ['plugin/adapters/host.md', 'plugin/adapters/mobile.md',
            'plugin/policies/astra-pr-review.md']
OVERRIDES = ['native-host-tools', 'project-local-model-rule', 'authority-boundaries',
             'mobile-routing-and-proof', 'fresh-regression-worker',
             'arena-context-isolation', 'bounded-mobile-opt-in', 'astra-high-pr-panel']


def require(value, message):
    if not value:
        raise ValueError(message)


def section(text, heading):
    match = re.search(r'^## ' + re.escape(heading) + r'\n(.*?)(?=^## |\Z)',
                      text, re.M | re.S)
    return match.group(1) if match else ''


def ordered(text, markers):
    positions = [text.find(marker) for marker in markers]
    return all(p >= 0 for p in positions) and positions == sorted(set(positions))


def behavior_errors(bodies):
    """Check phase-local obligations independently of the source fingerprints."""
    errors = []
    def expect(name, value):
        if not value:
            errors.append(name)
    for name, headings in {
        'architect': ['Ground the problem', 'Sketch', 'Agree (opt-in)',
                      'Implement against the sketch', 'Scrap when the architecture is wrong'],
        'arena': ['Frame', 'Fan out', 'Cross-judge', 'Pick a base', 'Graft', 'Verify'],
        'swarm': ['Frame', 'Fan out', 'Aggregate', 'Report'],
    }.items():
        actual = re.findall(r'^## Phase [A-F]: (.+)$', bodies[name], re.M)
        expect(name + '-phase-order', actual == headings)
    expect('architect-two-shapes', 'at least two structurally distinct candidates' in
           section(bodies['architect'], 'Phase B: Sketch'))
    expect('mandatory-feature-arena', 'Mandatory: no skip-with-reason escape' in bodies['feature']
           and ordered(bodies['feature'], ['1. `how`', '2. `architect`',
                                          '3. Write the throughput', '4. Delegate code-writing',
                                          '5. Verify', '6. Rebase', '7. If the design', '8. Run']))
    expect('three-family-interrogate', re.findall(
        r'\| Reviewer [ABC] \| `([^`]+)` \|', bodies['interrogate']) ==
        ['claude-opus-5-5-max', 'gpt-5.6-sol-max', 'grok-4.7-xhigh-fast'])
    expect('interrogate-adjudication', ordered(bodies['interrogate'],
        ['## Step 1,', '## Step 2,', '## Step 3,', '## Step 4,', '## Step 5,'])
        and 'Do NOT auto-apply changes' in bodies['interrogate'])
    expect('generator-feature-map', 'aim for the top 3-5' in
        section(bodies['create-verification-skill'], '3. Seed the feature map')
        and 'features/README.md' in bodies['create-verification-skill'])
    expect('generator-proof-after-map', ordered(bodies['create-verification-skill'],
        ['## 1.', '## 2.', '## 3.', '## 4.', '## 5.'])
        and 'drive ONE mapped feature' in section(bodies['create-verification-skill'],
                                                '4. Prove the generated skill before handing it over')
        and 'evidence still exists' in bodies['create-verification-skill'])
    maintenance = section(bodies['maintain-verification-skill'], 'Pass')
    expect('maintenance-whole-map', ordered(maintenance, ['0. **Locate', '1. **Index',
        '2. **Source', '3. **Reconcile', '4. **Live', '5. **Triage', '6. **Ship'])
        and 'Exercise every feature at least once' in maintenance
        and 'retry once' in maintenance and 'source path' in maintenance)
    expect('tdd-red-before-fix', ordered(section(bodies['tdd'], 'Workflow'),
        ['3. **Write', '4. **Run the new test before fixing', '5. **Fix', '6. **Rerun']))
    expect('swarm-coverage-and-dropouts', all(marker in section(bodies['swarm'], 'Phase C: Aggregate')
        for marker in ['SHAs and method', 'respawn that worker once',
                       'A gap does not count as a pass', 'every required slice']))
    expect('trail-append-only', all(marker in bodies['show-me-your-work'] for marker in
        ['Append-only', 'ts', 'phase', 'decision', 'why', 'evidence', 'result',
         'phase `start`', 'Cross-model review', 'Audit the log against the transcript']))
    expect('setup-panel-cardinality', all(marker in bodies['setup-pstack'] for marker in
        ['one subagent runs per entry', 'list length sets the count',
         'Never write a real slug you have not confirmed', 'Every real slug written',
         'unlimited — keep max', 'large — xhigh reasoning',
         'medium — high reasoning', 'small — medium reasoning']))
    mode = bodies['poteto-mode']
    expect('mode-fallback-and-trail', all(marker in mode for marker in
        ['Use **figure-it-out** whenever no bundled playbook fits',
         'routes to **Orchestrate** instead', '**show-me-your-work**',
         '**swarm**', '**benchmark-checklist**', '**no-comments**', '**technical-writing**']))
    return errors


def adapter_errors(texts):
    errors = []
    obligations = {
        ADAPTERS[0]: ['core owns workflow', 'List length sets', 'never an implicit replacement',
                     'project-local `.huguesstack/models.md`', 'No translation grants new authority',
                     'mark the seat blocked', 'Do not execute it without installation authority',
                     'ready-PR and stack/base mechanics', 'Supply absolute paths',
                     '`Comment Sicko` to `hugues-comment-sicko`',
                     'Do not substitute a generic worker without those rules'],
        ADAPTERS[1]: ['Intent before domain', 'Large, cross-cutting, unmatched',
                     'First select\nthe core action playbook',
                     'they never replace core todos or implementation gates',
                     'observe RED against unfixed production', 'separate\nfresh production worker',
                     'same\nregression', 'Keep the rubric', 'block blind judging',
                     'top 3–5', 'Maintenance covers the whole map',
                     'cannot replace or satisfy the core', 'One target does not prove'],
        ADAPTERS[2]: ['two fresh independent GPT-Astra reviewers at High effort',
                     'exact final candidate commit', 'explicit project addition',
                     'Generic interrogate keeps its pinned three-family defaults',
                     'report the required review blocked', 'fresh review of the new exact head',
                     'Do not create a draft as an implicit fallback'],
    }
    for path, markers in obligations.items():
        for marker in markers:
            if marker.casefold() not in texts[path].casefold():
                errors.append(path + ': lost override boundary: ' + marker)
    return errors


def mobile_route_errors(texts):
    errors = []
    for name, text in texts.items():
        before_steps = text.split('## Steps', 1)[0]
        if not all(marker in before_steps for marker in
                   ['selected core action playbook', 'ordered todos verbatim',
                    'Do not execute this extension in place of the core procedure']):
            errors.append(name + '-core-composition')
        match = re.search(r'^3\. (.*?)(?=^4\. |\Z)', text, re.M | re.S)
        implementation = match.group(1) if match else ''
        if not all(marker in implementation for marker in
                   ['selected core implementation gate', 'configured role models',
                    '[arena](../../arena/SKILL.md) in full', 'complete the implementation arena',
                    'Mandatory: no skip-with-reason escape',
                    'Design-only synthesis cannot satisfy this implementation gate',
                    'even within one function', 'core scoped-worker exception']):
            errors.append(name + '-implementation-arena')
    return errors


def check(root=ROOT):
    root = root.resolve()
    spec = importlib.util.spec_from_file_location('upstream_diff', ROOT / 'scripts/upstream-diff.py')
    upstream = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(upstream)
    snapshot = upstream.read_pin(root / 'docs/upstream/pin.json')
    require(snapshot['revision'] == PIN and snapshot['pstack_tree_sha'] == TREE
            and snapshot['version'] == '0.15.9' and snapshot['file_count'] == 161,
            'restoration must retain the approved pinned core')
    core = root / 'plugin/core'
    actual = set()
    for path in core.rglob('*'):
        require(not path.is_symlink(), 'symlink in immutable core')
        if path.is_file():
            actual.add(path.relative_to(core).as_posix())
    require(actual == {row['path'] for row in snapshot['files']}, 'core inventory differs')
    for row in snapshot['files']:
        path = core / row['path']
        body = path.read_bytes()
        mode = '100755' if stat.S_IMODE(path.stat().st_mode) & 0o111 else '100644'
        require(mode == row['mode'] and upstream.oid('blob', body) == row['blob_sha']
                and hashlib.sha256(body).hexdigest() == row['sha256']
                and len(body) == row['size'], 'pinned core bytes/mode differ: ' + row['path'])
    binding = upstream.load(root / 'plugin/core-bindings.json')
    require(set(binding) == {'schema_version', 'revision', 'upstream_version', 'core_directory',
                            'excluded_skills', 'skills', 'playbooks', 'agents', 'adapters'}, 'unknown binding fields')
    require(binding['schema_version'] == 1 and binding['revision'] == PIN and
            binding['upstream_version'] == '0.15.9' and binding['core_directory'] == 'plugin/core'
            and binding['excluded_skills'] == sorted(EXCLUDED) and binding['adapters'] == ADAPTERS,
            'binding pin, scope or adapter order differs')
    expected_skills = {}
    expected_playbooks = {}
    for row in snapshot['files']:
        parts = Path(row['path']).parts
        if len(parts) == 4 and parts[1] == 'skills' and parts[-1] == 'SKILL.md' and parts[2] not in EXCLUDED:
            name = ALIASES.get(parts[2], parts[2])
            expected_skills[name] = {'source': row['path'],
                'entrypoint': f'plugin/skills/{name}/SKILL.md',
                'kind': 'verbatim' if name.startswith('principle-') else 'loader'}
        if parts[:4] == ('pstack', 'skills', 'poteto-mode', 'playbooks'):
            name = Path(row['path']).stem
            expected_playbooks[name] = {'source': row['path'],
                'entrypoint': f'plugin/skills/hugues-mode/playbooks/{name}.md'}
    require(binding['skills'] == expected_skills and len(expected_skills) == 47,
            'active skill set or source wiring differs')
    require(binding['playbooks'] == expected_playbooks and len(expected_playbooks) == 23,
            'active playbook set or source wiring differs')
    require(binding['agents'] == AGENTS, 'specialized agent binding differs')
    manifest = upstream.load(root / 'plugin/.claude-plugin/plugin.json')
    require(manifest['skills'] == ['./skills'] and manifest['agents'] ==
            ['./agents/hugues-agent.md', './agents/hugues-comment-sicko.md'],
            'active manifest wiring differs')
    require({p.relative_to(root).as_posix() for p in (root / 'plugin/agents').glob('*.md')} ==
            {row['entrypoint'] for row in AGENTS.values()}, 'registered agent inventory differs')
    discovered = {p.relative_to(root).as_posix() for p in (root / 'plugin/skills').rglob('SKILL.md')}
    require(discovered == {row['entrypoint'] for row in expected_skills.values()},
            'registered skill inventory differs')
    playbooks = {p.stem for p in (root / 'plugin/skills/hugues-mode/playbooks').glob('*.md')}
    require(playbooks == set(expected_playbooks) | {'build-doctor', 'mobile-proof',
                'kmp-bridge-change', 'cmp-two-target-change'}, 'playbook extension inventory differs')
    for destination, content in outputs(root).items():
        path = root / destination
        require(path.is_file() and not path.is_symlink() and path.read_text() == content,
                'active loader/worker drift: ' + destination)
    bodies = {name: (core / f'pstack/skills/{name}/SKILL.md').read_text() for name in
              ['architect', 'arena', 'interrogate', 'create-verification-skill',
               'maintain-verification-skill', 'swarm', 'show-me-your-work', 'setup-pstack',
               'poteto-mode', 'tdd']}
    bodies['feature'] = (core / 'pstack/skills/poteto-mode/playbooks/feature.md').read_text()
    require(not behavior_errors(bodies), 'core behavior contracts differ: ' + ', '.join(behavior_errors(bodies)))
    texts = {path: (root / path).read_text() for path in ADAPTERS}
    require(not adapter_errors(texts), 'adapter behavior differs: ' + '; '.join(adapter_errors(texts)))
    mobile_routes = {name: (root / f'plugin/skills/hugues-mode/playbooks/{name}.md').read_text()
                     for name in ['kmp-bridge-change', 'cmp-two-target-change']}
    require(not mobile_route_errors(mobile_routes),
            'mobile core gates differ: ' + ', '.join(mobile_route_errors(mobile_routes)))
    receipt = upstream.load(root / 'docs/upstream/core-restoration.json')
    require(receipt['revision'] == PIN and receipt['effective_overrides'] == OVERRIDES,
            'unreviewed override inventory')
    require(receipt['adapter_sha256'] == {p: hashlib.sha256((root / p).read_bytes()).hexdigest()
                                        for p in ADAPTERS}, 'adapter bytes differ from reviewed receipt')
    # Core-relative dependency closure for explicit local Markdown links. External
    # tool names are capabilities, never counted as bundled or observed support.
    for path in (core / 'pstack/skills').rglob('*.md'):
        prose = re.sub(r'^(`{3,}|~{3,}).*?^\1[^\n]*$', '', path.read_text(), flags=re.M | re.S)
        prose = re.sub(r'`[^`\n]*`', '', prose)
        for target in re.findall(r'\]\(([^\s)]+)\)', prose):
            if '://' in target or target.startswith('#'):
                continue
            # Literal citation-template example in the verified upstream bytes.
            if (path.relative_to(core).as_posix(), target) == (
                    'pstack/skills/why/references/synthesizer-prompt.md', 'url'):
                continue
            resolved = path.parent / target.split('#')[0]
            require(resolved.resolve().is_relative_to(core.resolve()) and resolved.exists(),
                    f'core dependency missing/escaping: {path.relative_to(core)} -> {target}')
    return {'core_files': 161, 'active_skills': 47, 'core_playbooks': 23, 'mobile_playbooks': 4}


if __name__ == '__main__':
    try:
        print('PASS: pinned source + behavior + active wiring + override checks',
              check(Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT))
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print('core parity rejected: ' + str(exc), file=sys.stderr)
        sys.exit(1)
