"""Development contracts and real local helper behavior, separate from 0.1.0."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import check_core as core
import render_core
import check_whitespace
from release_snapshot import release_root


def bodies(root=ROOT):
    names = ['architect', 'arena', 'interrogate', 'create-verification-skill',
             'maintain-verification-skill', 'swarm', 'show-me-your-work',
             'setup-pstack', 'poteto-mode', 'tdd']
    result = {name: (root / 'plugin/core/pstack/skills' / name / 'SKILL.md').read_text()
              for name in names}
    result['feature'] = (root / 'plugin/core/pstack/skills/poteto-mode/playbooks/feature.md').read_text()
    return result


class DevelopmentBehavior(unittest.TestCase):
    def test_whitespace_exception_is_bounded_to_actual_upstream_diagnostics(self):
        report = '\n'.join(f'{p}:{n}: {reason}' for p, n, reason in sorted(check_whitespace.EXPECTED))
        check_whitespace.validate(report)
        for changed in [report + '\ndocs/PLAN.md:2: trailing whitespace.',
                        report.replace('README.md:5:', 'README.md:6:'),
                        report + '\n' + report.splitlines()[0]]:
            with self.assertRaises(ValueError):
                check_whitespace.validate(changed)

    def test_phase_local_contracts(self):
        self.assertEqual(core.behavior_errors(bodies()), [])

    def test_released_subset_cannot_supply_restored_contracts(self):
        old = release_root()
        data = {}
        for name in bodies():
            alias = {'poteto-mode': 'hugues-mode', 'setup-pstack': 'setup-huguesstack'}.get(name, name)
            path = old / 'plugin/skills' / alias / 'SKILL.md'
            if name == 'feature':
                path = old / 'plugin/skills/hugues-mode/playbooks/feature.md'
            data[name] = path.read_text() if path.exists() else ''
        errors = core.behavior_errors(data)
        for contract in ['mandatory-feature-arena', 'three-family-interrogate',
                         'generator-feature-map', 'maintenance-whole-map',
                         'mode-fallback-and-trail', 'setup-panel-cardinality']:
            self.assertIn(contract, errors)

    def test_order_cardinality_fallback_and_stop_mutations(self):
        mutations = [
            ('architect', '## Phase B: Sketch', '## Phase Z: Sketch', 'architect-phase-order'),
            ('architect', 'at least two structurally distinct candidates', 'one candidate', 'architect-two-shapes'),
            ('arena', '## Phase E: Graft', '## Phase Z: Graft', 'arena-phase-order'),
            ('feature', 'Mandatory: no skip-with-reason escape', 'Optional when warranted', 'mandatory-feature-arena'),
            ('feature', '3. Write the throughput', '9. Write the throughput', 'mandatory-feature-arena'),
            ('interrogate', '| Reviewer C | `grok-4.7-xhigh-fast` |', '| Reviewer C | `gpt-5.6-sol-max` |', 'three-family-interrogate'),
            ('interrogate', 'Do NOT auto-apply changes', 'Auto-apply changes', 'interrogate-adjudication'),
            ('create-verification-skill', 'aim for the top 3-5', 'only one agreed journey', 'generator-feature-map'),
            ('create-verification-skill', 'drive ONE mapped feature', 'drive nothing', 'generator-proof-after-map'),
            ('maintain-verification-skill', 'Exercise every feature at least once', 'Exercise one journey', 'maintenance-whole-map'),
            ('maintain-verification-skill', 'retry once', 'retry forever', 'maintenance-whole-map'),
            ('tdd', '4. **Run the new test before fixing', '7. **Run the new test before fixing', 'tdd-red-before-fix'),
            ('swarm', 'respawn that worker once', 'ignore that worker', 'swarm-coverage-and-dropouts'),
            ('swarm', 'A gap does not count as a pass', 'A gap counts as a pass', 'swarm-coverage-and-dropouts'),
            ('show-me-your-work', 'Append-only', 'Rewrite history', 'trail-append-only'),
            ('setup-pstack', 'one subagent runs per entry', 'one subagent per panel', 'setup-panel-cardinality'),
            ('poteto-mode', 'Use **figure-it-out** whenever no bundled playbook fits', 'Investigate only when no playbook fits', 'mode-fallback-and-trail'),
        ]
        for name, before, after, expected in mutations:
            with self.subTest(contract=expected, mutation=before):
                data = bodies()
                self.assertIn(before, data[name])
                data[name] = data[name].replace(before, after)
                self.assertIn(expected, core.behavior_errors(data))

    def test_proof_in_output_cannot_replace_phase_obligation(self):
        data = bodies()
        marker = 'at least two structurally distinct candidates'
        data['architect'] = data['architect'].replace(marker, 'one candidate') + '\n' + marker
        self.assertIn('architect-two-shapes', core.behavior_errors(data))

    def test_adapter_boundaries_independent_of_receipt_hashes(self):
        original = {p: (ROOT / p).read_text() for p in core.ADAPTERS}
        self.assertEqual(core.adapter_errors(original), [])
        for path, before, after in [
            (core.ADAPTERS[0], 'never an implicit replacement', 'always an implicit replacement'),
            (core.ADAPTERS[0], 'No translation grants new authority', 'Every translation grants new authority'),
            (core.ADAPTERS[0], 'List length sets', 'One worker sets'),
            (core.ADAPTERS[1], 'Maintenance covers the whole map', 'Maintenance covers one journey'),
            (core.ADAPTERS[1], 'observe RED against unfixed production', 'observe RED after production changes'),
            (core.ADAPTERS[1], 'block blind judging', 'claim blind judging'),
            (core.ADAPTERS[2], 'two fresh independent GPT-Astra reviewers at High effort', 'one inherited reviewer'),
            (core.ADAPTERS[2], 'Generic interrogate keeps its pinned three-family defaults', 'Generic interrogate uses Astra only'),
        ]:
            with self.subTest(boundary=before):
                data = dict(original)
                self.assertIn(before, data[path])
                data[path] = data[path].replace(before, after)
                self.assertTrue(core.adapter_errors(data))


class EffectiveWiring(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory(prefix='huguesstack-core-mutation-')
        self.addCleanup(folder.cleanup)
        self.root = Path(folder.name) / 'package'
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns('.git', '__pycache__', 'planning'))

    def rejected(self, diagnostic):
        with self.assertRaisesRegex(ValueError, diagnostic):
            core.check(self.root)

    def mutate_json(self, name, callback):
        path = self.root / name
        value = json.loads(path.read_text())
        callback(value)
        path.write_text(json.dumps(value))

    def test_actual_development_package(self):
        self.assertEqual(core.check(self.root), {'core_files': 161, 'active_skills': 47,
                                                'core_playbooks': 23, 'mobile_playbooks': 4})

    def test_core_source_and_inventory_drift(self):
        path = self.root / 'plugin/core/pstack/skills/interrogate/SKILL.md'
        path.write_text(path.read_text() + '\nChanged default.\n')
        self.rejected('core bytes/mode differ')

    def test_missing_core_reference(self):
        (self.root / 'plugin/core/pstack/skills/interrogate/references/rubric.md').unlink()
        self.rejected('core inventory differs')

    def test_added_core_file(self):
        (self.root / 'plugin/core/pstack/extra.md').write_text('unreviewed')
        self.rejected('core inventory differs')

    def test_executable_mode_drift(self):
        (self.root / 'plugin/core/pstack/skills/show-me-your-work/scripts/log.sh').chmod(0o644)
        self.rejected('core bytes/mode differ')

    def test_other_pin_cannot_pass(self):
        self.mutate_json('plugin/core-bindings.json', lambda d: d.update(revision='0' * 40))
        self.rejected('binding pin')

    def test_manifest_can_not_exclude_restored_skills(self):
        self.mutate_json('plugin/.claude-plugin/plugin.json', lambda d: d.update(skills=['./skills/hugues-mode']))
        self.rejected('manifest wiring')

    def test_wrong_core_alias(self):
        self.mutate_json('plugin/core-bindings.json', lambda d: d['skills']['interrogate'].update(source='pstack/skills/how/SKILL.md'))
        self.rejected('skill set or source wiring')

    def test_missing_registered_dependency(self):
        (self.root / 'plugin/skills/swarm/SKILL.md').unlink()
        self.rejected('registered skill inventory')

    def test_inactive_skill_cannot_be_registered(self):
        path = self.root / 'plugin/skills/automate-me/SKILL.md'
        path.parent.mkdir()
        path.write_text('unapproved capability')
        self.rejected('registered skill inventory')

    def test_loader_cannot_bypass_core_or_adapter_order(self):
        path = self.root / 'plugin/skills/interrogate/SKILL.md'
        path.write_text(path.read_text().replace('4. [Pinned interrogate core]', 'Ignore [Pinned interrogate core]'))
        self.rejected('loader/worker drift')

    def test_registered_worker_cannot_bypass_mode(self):
        path = self.root / 'plugin/agents/hugues-agent.md'
        path.write_text(path.read_text().replace('[hugues-mode]', '[skip-mode]'))
        self.rejected('loader/worker drift')

    def test_playbook_cannot_point_to_different_core(self):
        path = self.root / 'plugin/skills/hugues-mode/playbooks/feature.md'
        path.write_text(path.read_text().replace('playbooks/feature.md', 'playbooks/prototype.md'))
        self.rejected('loader/worker drift')

    def test_missing_core_route(self):
        (self.root / 'plugin/skills/hugues-mode/playbooks/orchestrate.md').unlink()
        self.rejected('playbook extension inventory')

    def test_unregistered_extra_route(self):
        (self.root / 'plugin/skills/hugues-mode/playbooks/other.md').write_text('unreviewed')
        self.rejected('playbook extension inventory')

    def test_adapter_bytes_are_review_bound(self):
        path = self.root / core.ADAPTERS[0]
        path.write_text(path.read_text() + '\nSkip review when convenient.\n')
        self.rejected('adapter bytes differ')

    def test_rehashed_adapter_still_cannot_weaken_authority(self):
        path = self.root / core.ADAPTERS[0]
        path.write_text(path.read_text().replace('No translation grants new authority', 'Grant all authority'))
        self.mutate_json('docs/upstream/core-restoration.json', lambda d:
            d['adapter_sha256'].update({core.ADAPTERS[0]: hashlib.sha256(path.read_bytes()).hexdigest()}))
        self.rejected('adapter behavior differs')

    def test_unreviewed_override_inventory(self):
        self.mutate_json('docs/upstream/core-restoration.json', lambda d: d['effective_overrides'].append('inherit-all-models'))
        self.rejected('unreviewed override inventory')

    def test_render_is_reproducible_and_does_not_edit_core(self):
        before = {p: p.read_bytes() for p in (self.root / 'plugin/core').rglob('*') if p.is_file()}
        one = render_core.outputs(self.root)
        self.assertEqual(one, render_core.outputs(self.root))
        self.assertEqual(before, {p: p.read_bytes() for p in before})

    def test_package_checker_cannot_accept_dormant_core(self):
        path = self.root / 'plugin/skills/hugues-mode/SKILL.md'
        path.write_text(path.read_text().replace('Execute that core contract', 'Never execute that core contract'))
        result = subprocess.run([sys.executable, str(ROOT / 'scripts/check_plugin.py'), str(self.root)],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn('loader/worker drift', result.stderr)


class LocalPinnedHelpers(unittest.TestCase):
    def test_decision_log_preserves_rows_and_escapes_untrusted_cells(self):
        helper = ROOT / 'plugin/core/pstack/skills/show-me-your-work/scripts/log.sh'
        with tempfile.TemporaryDirectory() as folder:
            log = Path(folder) / 'evidence/decisions.tsv'
            first = subprocess.run([str(helper), str(log), 'start', 'frame', 'why', 'run-id', 'begun'], capture_output=True)
            self.assertEqual(first.returncode, 0, first.stderr)
            original = log.read_bytes()
            second = subprocess.run([str(helper), str(log), 'verify', '=formula\t\n', '+why', '@evidence', '-result'], capture_output=True)
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertTrue(log.read_bytes().startswith(original))
            rows = log.read_text().splitlines()
            self.assertEqual(rows[0], 'ts\tphase\tdecision\twhy\tevidence\tresult')
            self.assertEqual(len(rows), 3)
            self.assertTrue(all(len(row.split('\t')) == 6 for row in rows))
            self.assertEqual(rows[-1].split('\t')[2:], ["'=formula  ", "'+why", "'@evidence", "'-result"])

    def test_decision_log_bad_arity_leaves_no_artifact(self):
        helper = ROOT / 'plugin/core/pstack/skills/show-me-your-work/scripts/log.sh'
        with tempfile.TemporaryDirectory() as folder:
            log = Path(folder) / 'decisions.tsv'
            result = subprocess.run([str(helper), str(log)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
            self.assertFalse(log.exists())

    @unittest.skipUnless(shutil.which('node'), 'Node unavailable; record helper check as unrun')
    def test_plan_checker_rejects_test_only_verification(self):
        helper = ROOT / 'plugin/core/pstack/skills/poteto-mode/scripts/check-plan.mjs'
        rule = 'Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked.'
        lanes = '\n'.join(f'- [ ] Lane {n}. Drive. Save `lane-{n}.png`. Pass when visible.' for n in range(1, 11))
        plan_text = f'''# Program

## How to read this
One box is one unit of work and names the evidence.
Check a box only when its evidence exists. Read playbooks/.
{rule}

## Program checklist
### Arm the program
git show origin/main:PLAN.md
### Spawn owners
/loop 1h
### PR mechanics
status message
### Verdict and merge
### Boot recipe

## PR 1
**Depends on.** None.
**Files.**
- [ ] file.py
**Build.**
- [ ] Build succeeds.
**You see.**
- [ ] Observable behavior.
**Verify, unit.** {rule}
- [ ] Regression passes.
**Verify, live.** {rule} Ten lanes on `inherit-parent` at the PR head
{lanes}
**Verify, perf.** {rule}
- [ ] Metric. latency
- [ ] Probe. local probe
- [ ] Baseline. old revision
- [ ] Rule. no regression
**Review gate.** None.
**Merge.**
- [ ] Authorized merge.

## Close the program
## Appendix Prototype evidence
'''
        with tempfile.TemporaryDirectory() as folder:
            plan = Path(folder) / 'plan.md'
            plan.write_text(plan_text)
            baseline = subprocess.run(['node', str(helper), str(plan)], capture_output=True, text=True)
            self.assertEqual(baseline.returncode, 0, baseline.stderr + baseline.stdout)
            plan.write_text(plan_text.replace('**Verify, live.** ' + rule, '**Verify, live.** Unit tests suffice.'))
            result = subprocess.run(['node', str(helper), str(plan)], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('Verify, live. does not open with the rule', result.stderr)
