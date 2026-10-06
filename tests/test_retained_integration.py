"""Static integration contracts on shipped files; no simulated host/mobile execution.

Mutation tests exercise real manifest discovery, numbered-step handoffs and the
existing package checker. Passing proves these Markdown relationships only.
"""
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest

from test_wp2_contract import MODE, PLAYBOOKS, routes, section, steps

ROOT = Path(__file__).resolve().parents[1]
RETAINED = {'how', 'why', 'architect', 'arena', 'tdd', 'blast-radius',
            'maintain-verification-skill', 'correct'}
DEFERRED = {'swarm', 'show-me-your-work', 'setup-huguesstack'}
RC1 = '21a82942019292f7212ff1185e9ef187ac96e86d'
RC2_HOST = 'e2ff899f226184e6109029e5bdb3ac19838b80e4'
RC2_LANE = 'dba645fa3adc024487c1137486a81b31e12ec832'
# These contracts relate call sites to shipped tools, not tool-body wording.
CALLS = {
    ('investigation', 1): {'how', 'why'},
    ('bug-fix', 2): {'how', 'why'},
    ('bug-fix', 3): {'architect', 'tdd'},
    ('bug-fix', 5): {'tdd'},
    ('feature', 1): {'how'},
    ('feature', 2): {'architect', 'arena'},
    ('feature', 4): {'arena'},
    ('prototype', 2): {'architect', 'arena'},
    ('refactoring', 1): {'how'},
    ('refactoring', 3): {'architect', 'blast-radius'},
    ('opening-a-pr', 1): {'blast-radius'},
    ('authoring-a-skill', 1): {'create-verification-skill', 'maintain-verification-skill', 'correct'},
    ('kmp-bridge-change', 2): {'tdd'},
    ('kmp-bridge-change', 3): {'how', 'architect', 'blast-radius'},
    ('cmp-two-target-change', 2): {'tdd'},
    ('cmp-two-target-change', 3): {'how', 'architect', 'blast-radius'},
}


def discovered(root):
    manifest = json.loads((root / 'plugin/.claude-plugin/plugin.json').read_text())
    paths = manifest['skills']
    if isinstance(paths, str):
        paths = [paths]
    return {p.resolve() for directory in paths
            for p in (root / 'plugin' / directory).rglob('SKILL.md')}


def integration_errors(root):
    errors = []
    found = discovered(root)
    expected = {root / 'plugin/skills' / name / 'SKILL.md' for name in RETAINED}
    if not {p.resolve() for p in expected} <= found:
        errors.append('retained manifest discovery')
    mode = (root / MODE / 'SKILL.md').read_text()
    # Mode index and call sites must reach files actually discovered by the manifest.
    guidance = section(mode, 'Available guidance')
    for name in RETAINED:
        if f'../{name}/SKILL.md' not in guidance:
            errors.append(f'mode index: {name}')
    table = routes(mode)
    if set(table) != PLAYBOOKS | {'interrogate'}:
        errors.append('existing routes')
    for (route, number), dependencies in CALLS.items():
        path = root / MODE / table[route][1]
        numbered = dict(steps(path.read_text()))
        body = numbered.get(str(number), '')
        linked = { (path.parent / target).resolve()
                  for target in re.findall(r'\[[^]]+\]\(([^)]+)\)', body) }
        for name in dependencies:
            target = (root / 'plugin/skills' / name / 'SKILL.md').resolve()
            if target not in linked or target not in found:
                errors.append(f'{route} step {number}: {name}')
        if 'in full' not in body:
            # Reuse is valid after an earlier mandatory complete read in this checklist.
            for name in dependencies:
                earlier = [text for n, text in numbered.items() if int(n) < number]
                if not any(f'../../{name}/SKILL.md' in text and 'in full' in text for text in earlier):
                    errors.append(f'{route} step {number}: complete read')
    # Observe order inside the actual step copied into the host checklist.
    bug = dict(steps((root / MODE / 'playbooks/bug-fix.md').read_text()))
    gate = bug['3']
    sequence = ['fresh scoped regression-test worker', 'independently run',
                'unfixed production code', 'observed RED',
                'separate fresh production implementation subagent']
    positions = [gate.find(item) for item in sequence]
    if min(positions) < 0 or positions != sorted(positions):
        errors.append('bug regression before production')
    if 'impractical seam' not in gate or 'original runtime failing observation' not in gate:
        errors.append('bug runtime fallback')
    if 'RED evidence from step 3' not in bug['5'] or 'same regression' not in bug['5']:
        errors.append('same-check GREEN handoff')
    for route in ('kmp-bridge-change', 'cmp-two-target-change'):
        numbered = dict(steps((root / MODE / f'playbooks/{route}.md').read_text()))
        body = numbered['2']
        sequence = ['fresh scoped regression-test worker', 'independently run',
                    'unfixed production code', 'observed RED', 'separate fresh production worker in step 3']
        positions = [body.find(item) for item in sequence]
        if min(positions) < 0 or positions != sorted(positions) or 'impractical-seam reason' not in body:
            errors.append(f'{route}: RED before production')
    author = dict(steps((root / MODE / 'playbooks/authoring-a-skill.md').read_text()))
    handoff = author['1']
    required = ['new consumer-local', 'existing bounded recipe', 'hand off to its numbered steps',
                'this playbook ends at that handoff', 'source wave', 'coordinator-owned live proof',
                'clean/changed/blocked', 'clean or blocked produces no PR']
    if not all(part in handoff for part in required) or 'fresh implementation subagent' not in author['2']:
        errors.append('maintenance before generic worker')
    if 'at least two occurrences per class' not in handoff:
        errors.append('recurring class evidence')
    generator = (root / 'plugin/skills/create-verification-skill/SKILL.md').read_text()
    if '../maintain-verification-skill/SKILL.md' not in generator or 'existing bounded recipe' not in generator:
        errors.append('existing generator maintenance handoff')
    # Analysis can delegate or run checks: preview must defer it to execution.
    mode_steps = dict(steps(mode))
    if 'execute that analysis only in step 4' not in mode_steps['2'] or 'reads and plans only' not in mode_steps['2']:
        errors.append('wide preview stop')
    if 'execute the selected blast-radius analysis only here' not in mode_steps['4']:
        errors.append('wide analysis execution scope')
    return errors


def host_binding_errors(root):
    errors = []
    receipt = (root / 'docs/rc-validation.md').read_text()
    intro = receipt.split('Recorded **6 October', 1)[0]
    if RC1 not in intro or '54 plugin-file fingerprints' not in intro:
        errors.append('historical RC1 fingerprint binding')
    if 'no RC2 loading, routing, delegation' not in intro:
        errors.append('RC2 coverage boundary')
    support = (root / 'docs/support.md').read_text()
    # New observations have their own revision-bound receipt. The historical
    # RC1 packet cannot cover them, and bounded observations cannot promote
    # the full workflow/mobile acceptance cell.
    rows = [tuple(part.strip() for part in row.strip('|').split('|'))
            for row in support.splitlines() if row.startswith('| RC2')]
    by_cell = {row[0]: row[1:] for row in rows if len(row) == 3}
    if len(by_cell) != len(rows):
        errors.append('RC2 unique evidence cells')
    full = by_cell.get('RC2 full eight-workflow adherence/mobile execution', ())
    if (len(full) != 2 or full[0] != 'blocked' or
            'remain unrun' not in full[1] or 'native Swift/Kotlin/KMP/CMP' not in full[1]):
        errors.append('RC2 full execution unrun')
    observed_cells = {'RC2 host loading and route previews',
                      'RC2 bounded retained workflow observations',
                      'RC2 static recipe/cold pickup'}
    actual_observed = {row[0] for row in rows if len(row) == 3 and row[1] == 'observed-pass'}
    optional_observed = {'RC2 repaired lane previews'}
    if not observed_cells <= actual_observed <= observed_cells | optional_observed:
        errors.append('RC2 bounded observation scope')
    loading = by_cell.get('RC2 host loading and route previews', ())
    if (len(loading) != 2 or loading[0] != 'observed-pass' or
            f'`{RC2_HOST[:7]}`' not in loading[1] or
            '(rc2-host-validation.md)' not in loading[1] or
            not all(item in loading[1] for item in ('35 skills', '16 routes', '87 steps',
                                                   'unsupported Kotlin'))):
        errors.append('RC2 loading receipt binding')
    bounded = by_cell.get('RC2 bounded retained workflow observations', ())
    if (len(bounded) != 2 or bounded[0] != 'observed-pass' or
            '(rc2-host-validation.md#bounded-workflow-observations)' not in bounded[1] or
            'runtime unrun' not in bounded[1]):
        errors.append('RC2 bounded workflow receipt binding')
    pickup = by_cell.get('RC2 static recipe/cold pickup', ())
    if (len(pickup) != 2 or pickup[0] != 'observed-pass' or
            '(rc2-host-validation.md#bounded-workflow-observations)' not in pickup[1] or
            not all(item in pickup[1] for item in
                    ('static Kotlin recipe', 'read-only Codex pickup',
                     'No mobile cycle, actual pause/compaction or resumed GREEN'))):
        errors.append('RC2 static recipe pickup limits')
    lane = by_cell.get('RC2 lane evidence', ())
    if (len(lane) != 2 or lane[0] != 'observed-fail' or
            f'`{RC2_LANE[:7]}`' not in lane[1] or
            'strict fixture comparisons FAIL' not in lane[1] or 'No full fixture PASS' not in lane[1]):
        errors.append('RC2 strict lane failures retained')
    host_receipt = (root / 'docs/rc2-host-validation.md').read_text()
    binding = host_receipt.split('## Original RC2 loading and routing', 1)[0]
    if (RC2_HOST not in binding or RC2_LANE not in binding or RC1 in binding or
            '79 plugin files' not in binding or 'distinct snapshots' not in binding):
        errors.append('separate RC2 revision binding')
    if not all(item in host_receipt for item in
               ('## Bounded workflow observations', '## Lane-evidence probes',
                'no full six-case fixture PASS is claimed',
                'Native Codex recipe invocation and a mobile recipe cycle remain',
                'actual pause, compaction, resumed GREEN and persistent native todos',
                'Full adherence of all eight retained workflows',
                'consumer implementation/build/drive under RC2', 'remain unrun')):
        errors.append('RC2 receipt acceptance limits')
    repaired = by_cell.get('RC2 repaired lane previews')
    if repaired is not None:
        # A later small sample can pass independently without rewriting the
        # earlier strict failures. Require its own scoped receipt and limits;
        # it supplies no full-workflow/native-mobile acceptance evidence.
        if ('(rc2-host-validation.md#repaired-schema-probes)' not in repaired[1] or
                'full workflow' not in repaired[1].lower() or
                not any(limit in repaired[1].lower() for limit in ('unproven', 'unrun'))):
            errors.append('RC2 repaired preview scope')
        repaired_receipt = section(host_receipt, 'Repaired schema probes')
        if (not re.search(r'\b[0-9a-f]{40}\b', repaired_receipt) or
                RC1 in repaired_receipt or
                'six' not in repaired_receipt.lower() or
                'full workflow' not in repaired_receipt.lower() or
                not any(limit in repaired_receipt.lower() for limit in ('unproven', 'unrun'))):
            errors.append('RC2 repaired preview receipt binding')
    return errors


class RetainedIntegration(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='huguesstack-retained-integration-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'package'
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns('.git', '__pycache__', 'planning'))

    def test_real_registered_call_sites_and_order(self):
        self.assertEqual(integration_errors(self.root), [])
        self.assertEqual(len(discovered(self.root)), 35)

    def test_manifest_removal_excludes_real_call_targets(self):
        path = self.root / 'plugin/.claude-plugin/plugin.json'
        manifest = json.loads(path.read_text())
        manifest['skills'] = ['./skills/hugues-mode']
        path.write_text(json.dumps(manifest))
        errors = integration_errors(self.root)
        self.assertIn('retained manifest discovery', errors)
        self.assertIn('feature step 2: architect', errors)

    def test_every_leaf_link_required_in_numbered_steps(self):
        for (route, number), dependencies in CALLS.items():
            path = self.root / MODE / f'playbooks/{route}.md'
            original = path.read_text()
            numbered = dict(steps(original))
            for name in dependencies:
                with self.subTest(route=route, step=number, dependency=name):
                    changed = numbered[str(number)].replace(f'../../{name}/SKILL.md', '../../interrogate/SKILL.md')
                    self.assertNotEqual(changed, numbered[str(number)])
                    path.write_text(original.replace(numbered[str(number)], changed))
                    self.assertIn(f'{route} step {number}: {name}', integration_errors(self.root))
                    path.write_text(original)

    def test_prose_link_outside_numbered_step_cannot_replace_handoff(self):
        path = self.root / MODE / 'playbooks/feature.md'
        original = path.read_text()
        step = dict(steps(original))['2']
        path.write_text(original.replace(step, step.replace('../../architect/SKILL.md', '../../interrogate/SKILL.md'))
                        + '\nRead [architect](../../architect/SKILL.md) in full.\n')
        self.assertIn('feature step 2: architect', integration_errors(self.root))

    def test_missing_actual_leaf_rejected_by_package_checker(self):
        (self.root / 'plugin/skills/tdd/SKILL.md').unlink()
        result = subprocess.run(['sh', str(self.root / 'scripts/check-plugin.sh'), str(self.root)],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn('playbooks/bug-fix.md: broken local link', result.stderr)
        self.assertIn('../../tdd/SKILL.md', result.stderr)

    def test_RED_moved_after_production_worker_rejected(self):
        path = self.root / MODE / 'playbooks/bug-fix.md'
        text = path.read_text()
        path.write_text(text.replace('observed RED', 'a planned check', 1)
                        .replace('separate fresh production implementation subagent.',
                                 'separate fresh production implementation subagent, then observe observed RED.', 1))
        self.assertIn('bug regression before production', integration_errors(self.root))

    def test_shared_bug_RED_missing_rejected(self):
        for route in ('kmp-bridge-change', 'cmp-two-target-change'):
            path = self.root / MODE / f'playbooks/{route}.md'
            original = path.read_text()
            with self.subTest(route=route):
                path.write_text(original.replace('observed RED', 'planned RED'))
                self.assertIn(f'{route}: RED before production', integration_errors(self.root))
                path.write_text(original)

    def test_maintenance_moved_after_generic_worker_rejected(self):
        path = self.root / MODE / 'playbooks/authoring-a-skill.md'
        text = path.read_text()
        first = dict(steps(text))['1']
        maintenance = re.search(r'For auditing.*?produces no PR\.', first)[0]
        path.write_text(text.replace(maintenance, '') + '\n' + maintenance + '\n')
        self.assertIn('maintenance before generic worker', integration_errors(self.root))

    def test_recurring_single_mistake_is_not_correct_workflow(self):
        path = self.root / MODE / 'playbooks/authoring-a-skill.md'
        path.write_text(path.read_text().replace('at least two occurrences per class', 'one observed mistake'))
        self.assertIn('recurring class evidence', integration_errors(self.root))

    def test_wide_preview_analysis_execution_rejected(self):
        path = self.root / MODE / 'SKILL.md'
        path.write_text(path.read_text().replace('execute that analysis only in step 4', 'execute the analysis now'))
        self.assertIn('wide preview stop', integration_errors(self.root))

    def test_approved_deferred_files_are_absent_and_ledger_preserves_scope(self):
        ledger = json.loads((self.root / 'docs/upstream/huguesStack-dispositions.json').read_text())
        deferred_rows = [row for row in ledger['items']
                         if row['path'].split('/')[2:3] and row['path'].split('/')[2] in
                         {'swarm', 'show-me-your-work', 'setup-pstack'}]
        self.assertTrue(deferred_rows)
        for row in deferred_rows:
            self.assertEqual((row['disposition'], row['implementation_state'], row['destinations']),
                             ('ignore with reason', 'deferred', []), row['path'])
        for name in DEFERRED:
            self.assertFalse((self.root / 'plugin/skills' / name).exists())
        # A deferred directory cannot masquerade as one of the retained tools.
        self.assertTrue(RETAINED.isdisjoint(DEFERRED))

    def test_RC_versions_match_without_native_execution_claim(self):
        plugin = json.loads((self.root / 'plugin/.claude-plugin/plugin.json').read_text())
        market = json.loads((self.root / '.claude-plugin/marketplace.json').read_text())
        self.assertEqual(plugin['version'], '0.1.0-rc.2')
        self.assertEqual(market['plugins'][0]['version'], plugin['version'])
        self.assertEqual(market['plugins'][0]['source'], './plugin')
        self.assertEqual(plugin['skills'], ['./skills'])

    def test_historical_host_evidence_stays_separate_from_RC2(self):
        self.assertEqual(host_binding_errors(self.root), [])

    def test_historical_fingerprints_cannot_be_promoted_to_RC2(self):
        path = self.root / 'docs/rc-validation.md'
        path.write_text(path.read_text().replace(RC1, 'f126656d2718084de8292cda0cb40b81333e4d6e'))
        self.assertIn('historical RC1 fingerprint binding', host_binding_errors(self.root))

    def test_full_workflow_mobile_cell_cannot_be_promoted_by_bounded_observations(self):
        path = self.root / 'docs/support.md'
        text = path.read_text()
        row = next(line for line in text.splitlines()
                   if line.startswith('| RC2 full eight-workflow adherence/mobile execution |'))
        path.write_text(text.replace(row, row.replace('| blocked |', '| observed-pass |')))
        errors = host_binding_errors(self.root)
        self.assertIn('RC2 full execution unrun', errors)
        self.assertIn('RC2 bounded observation scope', errors)

    def test_RC2_observations_require_separate_revision_bound_receipt(self):
        path = self.root / 'docs/rc2-host-validation.md'
        original = path.read_text()
        for revision in (RC2_HOST, RC2_LANE):
            with self.subTest(revision=revision):
                path.write_text(original.replace(revision, RC1))
                self.assertIn('separate RC2 revision binding', host_binding_errors(self.root))
        path.write_text(original)
        path = self.root / 'docs/support.md'
        original = path.read_text()
        for old, new, error in (
                (f'`{RC2_HOST[:7]}`', f'`{RC1[:7]}`', 'RC2 loading receipt binding'),
                ('(rc2-host-validation.md)', '(rc-validation.md)', 'RC2 loading receipt binding'),
                ('(rc2-host-validation.md#bounded-workflow-observations)',
                 '(rc-validation.md)', 'RC2 bounded workflow receipt binding'),
                ('No mobile cycle, actual pause/compaction or resumed GREEN',
                 'Mobile cycle and resumed GREEN passed', 'RC2 static recipe pickup limits')):
            with self.subTest(binding=old):
                self.assertIn(old, original)
                path.write_text(original.replace(old, new))
                self.assertIn(error, host_binding_errors(self.root))

    def test_semantic_lane_observations_cannot_hide_strict_fixture_failures(self):
        path = self.root / 'docs/support.md'
        original = path.read_text()
        row = next(line for line in original.splitlines() if line.startswith('| RC2 lane evidence |'))
        path.write_text(original.replace(row, row.replace('| observed-fail |', '| observed-pass |')))
        self.assertIn('RC2 strict lane failures retained', host_binding_errors(self.root))

    def test_later_bounded_previews_need_their_own_receipt_and_preserve_full_gate(self):
        support = self.root / 'docs/support.md'
        receipt = self.root / 'docs/rc2-host-validation.md'
        support_text = support.read_text()
        receipt_text = receipt.read_text()
        # Isolate the optional cell whether or not a later packet is present.
        support_text = '\n'.join(line for line in support_text.splitlines()
                                 if not line.startswith('| RC2 repaired lane previews |'))
        receipt_text = re.sub(r'^## Repaired schema probes\s*\n.*?(?=^## |\Z)', '',
                              receipt_text, flags=re.M | re.S)
        row = ('| RC2 repaired lane previews | observed-pass | Six scoped read-only cases. '
               '[Receipt](rc2-host-validation.md#repaired-schema-probes); '
               'full workflow and native mobile execution unproven |\n')
        support.write_text(support_text + '\n' + row)
        receipt.write_text(receipt_text)
        self.assertIn('RC2 repaired preview receipt binding', host_binding_errors(self.root))
        scoped = ('\n## Repaired schema probes\n\n'
                  'Six scoped cases bind revision `aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa`. '
                  'Full workflow and native mobile execution remain unproven.\n')
        receipt.write_text(receipt_text + scoped)
        self.assertEqual(host_binding_errors(self.root), [])
        receipt.write_text(receipt_text + scoped.replace('a' * 40, RC1))
        self.assertIn('RC2 repaired preview receipt binding', host_binding_errors(self.root))
        receipt.write_text(receipt_text + scoped)
        support.write_text(support_text + '\n' + row.replace('#repaired-schema-probes', ''))
        self.assertIn('RC2 repaired preview scope', host_binding_errors(self.root))
        support.write_text(support_text + '\n' + row.replace('execution unproven', 'execution passed'))
        self.assertIn('RC2 repaired preview scope', host_binding_errors(self.root))


if __name__ == '__main__':
    unittest.main()
