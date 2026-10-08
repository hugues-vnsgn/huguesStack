"""Verify actual pinned bytes, active workflow wiring and bounded policy overrides."""
import hashlib
import ast
import importlib.util
import json
from pathlib import Path
import re
import stat
import sys

import tarfile

ROOT = Path(__file__).resolve().parents[1]
PIN = 'e43c7ee26e0038c6c1fa8380dd34ce86ff94cb2a'
TREE = '54dfdd87fd191ddda7fce01dd354d220adaeeacc'
EXCLUDED = set()
ALIASES = {'poteto-mode': 'hugues-mode', 'setup-pstack': 'setup-huguesstack'}
# Reviewed host invocation table. Upstream marks 49 skills manual-only for Cursor; on
# Claude Code and Codex that blocks every skill-to-skill call, so only entry points that
# mine personal history or expose services stay user-only. Every other skill is a
# model-invocable dependency.
USER_ONLY = {'automate-me', 'make-bot-ui', 'recall', 'reflect'}
AGENTS = {
    'poteto-agent': {'source': 'pstack/agents/poteto-agent.md',
                     'entrypoint': 'plugin/agents/hugues-agent.md'},
    'Comment Sicko': {'source': 'pstack/agents/comment-sicko.md',
                      'entrypoint': 'plugin/agents/hugues-comment-sicko.md'},
}
WORKER_ROLES = {
    'how-explorer': ('how', 'generalPurpose', 'references/explorer-prompt.md'),
    'how-explainer': ('how', 'generalPurpose', 'references/explainer-prompt.md'),
    'why-investigator': ('why', 'generalPurpose', 'references/investigator-prompt.md'),
    'why-synthesizer': ('why', 'generalPurpose', 'references/synthesizer-prompt.md'),
    'reflect-judgment': ('reflect', 'generalPurpose', 'references/judgment-reviewer.md'),
    'reflect-tooling': ('reflect', 'generalPurpose', 'references/tooling-reviewer.md'),
    'reflect-divergent': ('reflect', 'generalPurpose', 'references/divergent-reviewer.md'),
    'reflect-synthesizer': ('reflect', 'generalPurpose', 'references/synthesizer.md'),
    'interrogate-reviewer': ('interrogate', 'generalPurpose', 'references/reviewer-prompt.md'),
    'architect-runner': ('architect', 'core', 'references/runner-prompt.md'),
    'arena-runner': ('arena', 'core', 'SKILL.md'),
    'arena-cross-judge': ('arena', 'core', 'SKILL.md'),
    'swarm-worker': ('swarm', 'generalPurpose', 'SKILL.md'),
    'automate-me-history-miner': ('automate-me', 'core', 'SKILL.md'),
    'show-me-your-work-auditor': ('show-me-your-work', 'core', 'SKILL.md'),
}


def worker_roles():
    return {name: {'skill': skill, 'dispatch': dispatch,
                   'prompt': f'pstack/skills/{skill}/{prompt}'}
            for name, (skill, dispatch, prompt) in WORKER_ROLES.items()}


ADAPTERS = ['plugin/adapters/host.md', 'plugin/adapters/mobile.md']
PHASE_GUIDANCE = {
    'host-workers.md': 'Worker dispatch, worker execution, role selection or setup-huguesstack',
    'host-workflow-tools.md': 'Installed planning or audit commands, workflow ticks, other installed helpers, Bun bootstrap, cloud/loop/forge operations',
    'host-special-skills.md': 'Transcript-dependent skills, optional integrations or consumer skill placement',
    'host-typescript.md': 'Reading or editing TypeScript files',
    'host-publication.md': 'Skill authoring, commits, review, PR preparation/publication or missing control/writing capability reports',
}
ADAPTER_RESOURCES = ['plugin/adapters/' + name for name in PHASE_GUIDANCE] + ['plugin/adapters/mobile-workflows.md']
PROJECT_POLICY = 'plugin/policies/astra-pr-review.md'


def require(value, message):
    if not value:
        raise ValueError(message)


def native_frontmatter(text):
    header = re.match(r'\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)', text, re.S)
    require(header, 'missing native frontmatter')
    fields = {}
    description_block = False
    for line in header[1].splitlines():
        if not line.strip() or line.lstrip().startswith('#'):
            continue
        if description_block and line[0].isspace():
            continue
        pair = re.fullmatch(r'([a-z][a-z-]*):\s+(.+)', line)
        require(pair, 'unsupported native frontmatter scalar')
        key, value = pair.groups()
        require(key not in fields, 'duplicate native frontmatter field: ' + key)
        fields[key] = value
        description_block = key == 'description' and value in {'>', '>-', '>+', '|', '|-', '|+'}
    manual = fields.get('disable-model-invocation', 'false')
    require(manual in {'true', 'false'}, 'invalid native invocation boolean')
    fields['disable-model-invocation'] = manual == 'true'
    return fields


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
    expect('three-seat-interrogate', re.findall(
        r'\| Reviewer [ABC] \| `([^`]+)` \|', bodies['interrogate']) == ['inherit-parent max'] * 3)
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
    host = texts[ADAPTERS[0]]
    for name, trigger in PHASE_GUIDANCE.items():
        if not re.search(r'^\| ' + re.escape(trigger) + r' \| \[[^\]]+\]\(' + re.escape(name) + r'\) \|$', host, re.M):
            errors.append('missing phase prerequisite: ' + name)
    for marker in ['Before the triggering action, read its complete reference',
                   'never use a file read as an invocation fallback', 'never restart task routing',
                   'No translation grants new authority', 'A constraint\ncan block execution',
                   'copy its ordered todos verbatim']:
        if marker.casefold() not in host.casefold():
            errors.append('lost always-loaded boundary: ' + marker)
    mobile = texts[ADAPTERS[1]]
    if not all(marker in mobile for marker in ['explicitly selected mobile task',
               '[mobile workflows](mobile-workflows.md) in full', 'before selecting the route or executing a phase',
               'For all other work, follow the pinned core unchanged']):
        errors.append('lost mobile applicability prerequisite')
    effective = dict(texts)
    effective[ADAPTERS[0]] = '\n'.join([host, *(texts['plugin/adapters/' + name] for name in PHASE_GUIDANCE)])
    effective[ADAPTERS[1]] = mobile + '\n' + texts['plugin/adapters/mobile-workflows.md']
    obligations = {
        ADAPTERS[0]: ['canonical skill owns workflow', 'never use a file read as an invocation fallback',
                     'never restart task routing', 'consumer or external skill', 'List length sets', 'never an implicit replacement', 'effort setting',
                     'project-local `.huguesstack/models.md`', 'No translation grants new authority',
                     'mark the seat blocked', 'Do not execute it without installation authority',
                     'ready-PR and stack/base mechanics', 'Supply absolute paths',
                     '`Comment Sicko` to `hugues-comment-sicko`',
                     'Do not substitute a generic worker without those rules',
                     'All 50 top-level skills are registered',
                     'preserve `generalPurpose`', 'Do not replace these workers with `hugues-agent`',
                     'Registration grants no permission to process personal transcripts',
                     'TypeScript paths remain `**/*.ts` and `**/*.tsx`',
                     'automate-me history mining remains blocked',
                     'Reflect retains the pinned current-session digest fallback',
                     'Preserve Recall\'s\nexplicit state-capsule shortcut'],
        ADAPTERS[1]: ['For all other work, follow the pinned core unchanged', 'For mobile bug fixes',
                     'For mobile arena work', 'Intent before domain', 'Large, cross-cutting, unmatched',
                     'First select\nthe core action playbook',
                     'they never replace core todos or implementation gates',
                     'observe RED against unfixed production', 'separate\nfresh production worker',
                     'same\nregression', 'Keep the rubric', 'block blind judging',
                     'top 3–5', 'Maintenance covers the whole map',
                     'cannot replace or satisfy the core', 'One target does not prove'],
        PROJECT_POLICY: ['does not activate this profile', 'two fresh independent GPT-Astra reviewers at High effort',
                     'exact final candidate commit', 'explicit project addition',
                     'Generic interrogate keeps its three-seat',
                     'report the required review blocked', 'fresh review of the new exact head',
                     'Do not create a draft as an implicit fallback'],
    }
    for path, markers in obligations.items():
        for marker in markers:
            if marker.casefold() not in effective[path].casefold():
                errors.append(path + ': lost override boundary: ' + marker)
    return errors


def current_document_errors(texts):
    errors = []
    plan = texts['docs/PLAN.md']
    guide = texts['docs/upstream/README.md'].split('# Upstream sync', 1)[0]
    for name, text in [('docs/PLAN.md', plan), ('docs/upstream/README.md', guide)]:
        if not all(marker in text for marker in ['all 50 top-level skills', 'both upstream agents']):
            errors.append(name + ': incomplete current inventory')
        if re.search(r'(?:47|three excluded|families inactive)', text, re.I):
            errors.append(name + ': stale current exclusions')
    if '9 October, GMT+7' not in plan:
        errors.append('docs/PLAN.md: changed original deadline')
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
    require(not root.is_symlink(), 'unsafe repository root')
    root = root.resolve()
    require(not any(p.is_symlink() for p in root.rglob('*') if '.git' not in p.parts),
            'unsafe repository symlink')
    spec = importlib.util.spec_from_file_location('native_upstream', root / 'scripts/upstream-diff.py')
    upstream = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(upstream)
    snapshot = upstream.read_pin(root / 'docs/upstream/pin.json')
    require(snapshot['revision'] == PIN and snapshot['file_count'] == 161, 'upstream pin differs')
    receipt = upstream.load(root / 'docs/upstream/consolidation.json')
    require(receipt['schema_version'] == 1 and receipt['upstream_revision'] == PIN,
            'consolidation pin differs')
    require(not (root / 'plugin/core').exists() and not (root / 'plugin/core-bindings.json').exists(),
            'retired runtime core or registry present')
    archive = root / 'provenance/upstream/pstack-0.15.9.tar.gz'
    require(receipt['archive'] == archive.relative_to(root).as_posix() and not archive.is_symlink()
            and hashlib.sha256(archive.read_bytes()).hexdigest() == receipt['archive_sha256'],
            'upstream archive differs')
    expected = {r['path']: r for r in snapshot['files']}
    original_bodies = {}
    with tarfile.open(archive) as tar:
        members = tar.getmembers()
        require(len(members) == len(expected) and {m.name for m in members} == set(expected),
                'upstream archive inventory differs')
        for member in members:
            require(member.isfile(), 'unsafe upstream archive entry')
            body = tar.extractfile(member).read()
            original_bodies[member.name] = body
            row = expected[member.name]
            require(member.mode == int(row['mode'][-3:], 8) and len(body) == row['size']
                    and hashlib.sha256(body).hexdigest() == row['sha256']
                    and upstream.oid('blob', body) == row['blob_sha'], 'upstream archive bytes/mode differ')
    rows = receipt['files']
    require(len(rows) == len(expected) and {r['source'] for r in rows} == set(expected),
            'consolidation source coverage differs')
    destinations = [r['destination'] for r in rows if r['destination']]
    require(len(destinations) == len(set(destinations)), 'duplicate canonical destination')
    for row in rows:
        original = expected[row['source']]
        source = row['source'].removeprefix('pstack/')
        if source.startswith('skills/'):
            parts = source.split('/')
            parts[1] = ALIASES.get(parts[1], parts[1])
            destination = 'plugin/' + '/'.join(parts)
            if source.endswith('/scripts/worktree-audit.sh'):
                destination = None
        elif source.startswith('agents/'):
            destination = next(v['entrypoint'] for v in AGENTS.values() if v['source'] == row['source'])
        elif source.startswith('docs/'):
            destination = 'docs/pstack/' + source.removeprefix('docs/')
        elif source == 'LICENSE':
            destination = 'plugin/PSTACK-LICENSE'
        else:
            destination = None
        require(row['destination'] == destination and row['disposition'] ==
                ('canonical' if destination else 'provenance-only'), 'canonical source identity differs')
        require(row['source_sha256'] == original['sha256']
                and row['source_mode'] == int(original['mode'][-3:], 8), 'source provenance differs')
        if row['destination']:
            path = root / upstream.destination_path(row['destination'])
            require(path.is_file() and not path.is_symlink() and path.resolve().is_relative_to(root),
                    'missing/unsafe canonical destination')
            require(hashlib.sha256(path.read_bytes()).hexdigest() == row['destination_sha256'],
                    'canonical destination bytes differ: ' + row['destination'])
            require(stat.S_IMODE(path.stat().st_mode) == row['source_mode'], 'canonical source mode differs')
    names = {ALIASES.get(Path(name).parts[2], Path(name).parts[2]) for name in expected
             if len(Path(name).parts) == 4 and name.endswith('/SKILL.md')}
    require(set(receipt['public_skills']) == names and len(names) == 50, 'public skill inventory differs')
    require(receipt.get('host_invocation', {}).get('user_only') == sorted(USER_ONLY),
            'host invocation receipt differs')
    declarations = list((root / 'plugin').rglob('SKILL.md'))
    require({p.relative_to(root).as_posix() for p in declarations} ==
            {f'plugin/skills/{name}/SKILL.md' for name in names}, 'registered skill inventory differs')
    for path in declarations:
        text = path.read_text()
        name = path.parent.name
        fields = native_frontmatter(text)
        require(fields.get('name') == name, 'native name differs: ' + name)
        manual = fields['disable-model-invocation']
        upstream_name = next((old for old, new in ALIASES.items() if new == name), name)
        original_fields = native_frontmatter(original_bodies[f'pstack/skills/{upstream_name}/SKILL.md'].decode())
        require(manual == (name in USER_ONLY), 'host invocation table differs: ' + name)
        require(fields.get('paths') == original_fields.get('paths'), 'native path scope differs: ' + name)
        require((path.parent / 'agents/openai.yaml').read_text() ==
                'policy:\n  allow_implicit_invocation: ' + str(not manual).lower() + '\n',
                'native invocation policy differs: ' + name)
        if not name.startswith('principle-'):
            require('The host contract supersedes inherited sibling-body reads.' in text
                    and '[host contract](../../adapters/host.md)' in text,
                    'native dependency boundary missing: ' + name)
    for relative in ['skills/hugues-mode/playbooks/mobile-proof.md',
                     'skills/hugues-mode/references/mobile-lanes.md',
                     'skills/hugues-mode/references/jev-drive.md']:
        text = (root / 'plugin' / relative).read_text()
        require(not re.search(r'(?:read|Read)[^\n]*directly[^\n]*(?:invocation|disabled)', text),
                'consumer skill invocation bypass: ' + relative)
    manifest = upstream.load(root / 'plugin/.claude-plugin/plugin.json')
    require(manifest['skills'] == ['./skills'] and manifest['agents'] ==
            ['./agents/hugues-agent.md', './agents/hugues-comment-sicko.md'], 'manifest wiring differs')
    require({p.name for p in (root / 'plugin/agents').glob('*.md')} ==
            {'hugues-agent.md', 'hugues-comment-sicko.md'}, 'registered agent inventory differs')
    require(receipt['agents'] == AGENTS, 'specialized agent binding differs')
    source_map = {r['source']: r['destination'] for r in rows}
    require(receipt['worker_roles'] == {role: {**row, 'prompt': source_map[row['prompt']]}
            for role, row in worker_roles().items()}, 'worker role wiring differs')
    playbooks = {p.stem for p in (root / 'plugin/skills/hugues-mode/playbooks').glob('*.md')}
    original_playbooks = {Path(p).stem for p in expected
                         if p.startswith('pstack/skills/poteto-mode/playbooks/')}
    require(playbooks == original_playbooks | {'build-doctor', 'mobile-proof', 'kmp-bridge-change',
                                              'cmp-two-target-change'}, 'playbook inventory differs')
    bodies = {name: (root / 'plugin/skills' / ALIASES.get(name, name) / 'SKILL.md').read_text()
              for name in ['architect', 'arena', 'interrogate', 'create-verification-skill',
                           'maintain-verification-skill', 'swarm', 'show-me-your-work',
                           'setup-pstack', 'poteto-mode', 'tdd']}
    bodies['feature'] = (root / 'plugin/skills/hugues-mode/playbooks/feature.md').read_text()
    require(not behavior_errors(bodies), 'workflow behavior differs: ' + ', '.join(behavior_errors(bodies)))
    cursor_models = sorted(p.relative_to(root).as_posix() for p in (root / 'plugin').rglob('*.md')
                           if re.search(r'pstack-models\.mdc|\.cursor/rules|grok-\d|claude-opus-\d-\d-max|gpt-\d\.\d-sol-max',
                                        p.read_text()))
    require(not cursor_models, 'Cursor model wiring in installed skills: ' + ', '.join(cursor_models))
    texts = {p: (root / p).read_text() for p in [*ADAPTERS, *ADAPTER_RESOURCES, PROJECT_POLICY]}
    require(not adapter_errors(texts), 'adapter behavior differs: ' + '; '.join(adapter_errors(texts)))
    mobile = {name: (root / f'plugin/skills/hugues-mode/playbooks/{name}.md').read_text()
              for name in ['kmp-bridge-change', 'cmp-two-target-change']}
    require(not mobile_route_errors(mobile), 'mobile workflow gates differ')
    installed = {}
    for path in (root / 'plugin').rglob('*'):
        relative = path.relative_to(root / 'plugin').as_posix()
        if relative.startswith('adapters/runtime/__pycache__/') and path.suffix == '.pyc' and not path.is_symlink():
            continue
        require(not path.is_symlink() and (path.is_file() or path.is_dir()), 'unsafe installed path')
        if path.is_file():
            installed[relative] = {'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                                   'mode': stat.S_IMODE(path.stat().st_mode)}
    require(installed == receipt['installed_files'], 'installed inventory/bytes/mode differs')
    helpers = upstream.load(root / 'docs/HELPER-INPUTS.json')
    require(helpers['source_revision'] == PIN and {r['source'] for r in helpers['files']} ==
            {p for p in expected if p.startswith('pstack/skills/poteto-mode/scripts/')},
            'helper input coverage differs')
    for row in helpers['files']:
        require(row['source_sha256'] == expected[row['source']]['sha256'], 'helper source differs: ' + row['source'])
        if row['installed'] is None:
            require(row['candidate_sha256'] is None and source_map[row['source']] is None,
                    'provenance-only helper differs: ' + row['source'])
            continue
        require(row['installed'] == source_map[row['source']], 'helper destination differs: ' + row['source'])
        actual = installed[row['installed'].removeprefix('plugin/')]['sha256']
        require(actual == row['candidate_sha256'] and row['same_bytes_as_upstream'] ==
                (actual == row['source_sha256']), 'helper input receipt is stale: ' + row['installed'])
    bootstrap = ast.parse((root / 'plugin/adapters/host_tools.py').read_text())
    anchor = next(ast.literal_eval(n.value) for n in bootstrap.body if isinstance(n, ast.Assign)
                  and any(isinstance(t, ast.Name) and t.id == 'RUNTIME_SHA256' for t in n.targets))
    require(anchor == {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                       for p in (root / 'plugin/adapters/runtime').glob('*.py')}, 'runtime anchor differs')
    payload_path = root / 'plugin/adapters/runtime/payload.json'
    payload = upstream.load(payload_path)
    anchors = {'adapters/runtime/payload.json', 'adapters/runtime/payload.py', 'adapters/host_tools.py'}
    require(payload == {'schema_version': 2, 'revision': 'huguesstack-native-v1',
        'upstream_revision': PIN,
        'legacy_paths': {s: d.removeprefix('plugin/') for s, d in source_map.items() if d and d.startswith('plugin/')},
        'files': [{'path': p, 'sha256': row['sha256'], 'mode': '100'+format(row['mode'], '03o')}
                  for p, row in sorted(installed.items()) if p not in anchors]}, 'installed payload manifest differs')
    require("MANIFEST_SHA256 = '" + hashlib.sha256(payload_path.read_bytes()).hexdigest() + "'" in
            (root / 'plugin/adapters/runtime/payload.py').read_text(), 'payload anchor differs')
    return {'upstream_archive_files': 161, 'active_skills': 50, 'core_playbooks': 23,
            'mobile_playbooks': 4, 'core_agents': 2, 'worker_roles': 15}


if __name__ == '__main__':
    try:
        print('PASS: source provenance + canonical workflows + installed integrity',
              check(Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT))
    except (ValueError, OSError, KeyError, TypeError, tarfile.TarError) as exc:
        print('native distribution rejected: ' + str(exc), file=sys.stderr)
        sys.exit(1)
