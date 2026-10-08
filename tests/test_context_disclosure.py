from pathlib import Path
import hashlib
import json
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import check_core
import measure_context
from test_host_adapters import InstalledFixture


class ContextDisclosure(unittest.TestCase):
    def test_initial_adapters_do_not_eagerly_load_unrelated_phase_guidance(self):
        host = (ROOT / 'plugin/adapters/host.md').read_text()
        mobile = (ROOT / 'plugin/adapters/mobile.md').read_text()
        self.assertLess(len(host.encode()) + len(mobile.encode()), 6000)
        self.assertIn('never use a file read as an invocation fallback', host)
        self.assertIn('never restart task routing', host)
        self.assertIn('No translation grants new authority', host)
        self.assertIn('For all other work, follow the pinned core unchanged', mobile)

    def test_adapter_partition_preserves_every_original_rule(self):
        baseline, _ = measure_context.native_baseline(ROOT)
        receipt = json.loads((ROOT / 'docs/ADAPTER-DISCLOSURE.json').read_text())
        paragraphs = baseline[receipt['host_source']].strip().split('\n\n')
        restored = {}
        for row in receipt['host_fragments']:
            fragment = paragraphs[row['paragraph']]
            if row['slice']:
                fragment = fragment[slice(*row['slice'])].rstrip()
            self.assertEqual(hashlib.sha256(fragment.encode()).hexdigest(), row['sha256'])
            self.assertEqual((ROOT / row['destination']).read_text().count(fragment), 1)
            restored.setdefault(row['paragraph'], []).append(fragment)
        self.assertEqual(set(restored), set(range(len(paragraphs))))
        for index, pieces in restored.items():
            self.assertEqual(' '.join(' '.join(pieces).split()), ' '.join(paragraphs[index].split()))
        mobile = (ROOT / receipt['mobile_destination']).read_bytes()
        self.assertEqual(mobile, baseline[receipt['mobile_source']].encode())
        self.assertEqual(hashlib.sha256(mobile).hexdigest(), receipt['mobile_sha256'])

    def adapter_texts(self):
        return {p: (ROOT / p).read_text() for p in
                [*check_core.ADAPTERS, *check_core.ADAPTER_RESOURCES, check_core.PROJECT_POLICY]}

    def test_each_phase_reference_is_a_required_prerequisite(self):
        original = self.adapter_texts()
        self.assertEqual(check_core.adapter_errors(original), [])
        for name in check_core.PHASE_GUIDANCE:
            with self.subTest(name=name):
                changed = dict(original)
                changed[check_core.ADAPTERS[0]] = changed[check_core.ADAPTERS[0]].replace('(' + name + ')', '(missing.md)')
                self.assertTrue(check_core.adapter_errors(changed))

    def test_mobile_and_worker_rules_cannot_disappear_after_deferral(self):
        original = self.adapter_texts()
        for name, marker in [('plugin/adapters/mobile.md', '[mobile workflows](mobile-workflows.md) in full'),
                             ('plugin/adapters/mobile-workflows.md', 'separate\nfresh production worker'),
                             ('plugin/adapters/host-workers.md', 'List length sets')]:
            with self.subTest(name=name):
                changed = dict(original)
                self.assertIn(marker, changed[name])
                changed[name] = changed[name].replace(marker, 'omitted')
                self.assertTrue(check_core.adapter_errors(changed))

    def test_scenarios_count_required_dependencies_and_expose_unknown_totals(self):
        scenarios = measure_context.measure(ROOT)['scenarios']
        expected = {
            'initial_mode_routing': ['plugin/skills/unslop/SKILL.md',
                                    'plugin/skills/hugues-mode/playbooks/bug-fix.md'],
            'bug_fix': ['plugin/skills/tdd/SKILL.md', 'plugin/skills/why/references/epistemics.md',
                        'plugin/skills/why/references/sources/code-archaeology.md',
                        'plugin/agents/hugues-comment-sicko.md', 'plugin/adapters/host-workers.md',
                        'plugin/skills/principle-subtract-before-you-add/SKILL.md'],
            'larger_feature': ['plugin/skills/architect/references/design-red-flags.md',
                               'plugin/skills/arena/SKILL.md', 'plugin/skills/swarm/SKILL.md',
                               'plugin/skills/typescript-best-practices/references/patterns.md',
                               'plugin/adapters/host-typescript.md',
                               'plugin/skills/principle-subtract-before-you-add/SKILL.md'],
        }
        for name, paths in expected.items():
            profile = scenarios[name]
            self.assertTrue(set(paths) <= set(profile['candidate']['paths']))
            self.assertIsNone(profile['complete_execution_tokens'])
            self.assertTrue(profile['unknown_inputs'])
            self.assertNotIn('plugin/adapters/mobile-workflows.md', profile['candidate']['paths'])
        self.assertEqual(scenarios['bug_fix']['fresh_mode_worker_floor']['candidate']['mode_workers'], 1)
        self.assertEqual(scenarios['larger_feature']['fresh_mode_worker_floor']['candidate']['mode_workers'], 8)

    def test_source_budgets_recompute_without_changing_canonical_bodies(self):
        measured = measure_context.measure(ROOT)
        self.assertEqual(measured, json.loads((ROOT / 'docs/CONTEXT-BUDGET.json').read_text()))
        # The host invocation table drops inherited manual-only metadata from 45 skill bodies;
        # the four user-only entries and setup-huguesstack stay byte-identical.
        self.assertEqual(measured['canonical_skill_bodies']['unchanged_files'], 5)
        self.assertLess(measured['native_frontmatter']['candidate']['bytes'],
                        measured['native_frontmatter']['native_before']['bytes'])
        for profile in measured['scenarios'].values():
            self.assertLess(profile['candidate']['bytes'], profile['native_before']['bytes'])
        routing = measured['scenarios']['initial_mode_routing']
        self.assertLess(routing['candidate']['bytes'], routing['native_before']['bytes'] * .8)

    def test_context_baseline_drift_is_rejected(self):
        with tempfile.TemporaryDirectory(prefix='context-baseline-') as directory:
            root = Path(directory)
            (root / 'docs').mkdir()
            receipt = ROOT / 'docs/CONTEXT-BASELINE.json'
            shutil.copyfile(receipt, root / 'docs/CONTEXT-BASELINE.json')
            name = json.loads(receipt.read_text())['archive']
            (root / name).parent.mkdir(parents=True)
            (root / name).write_bytes((ROOT / name).read_bytes() + b'drift')
            with self.assertRaisesRegex(ValueError, 'baseline archive drift'):
                measure_context.native_baseline(root)


class InstalledPhaseGuidance(InstalledFixture, unittest.TestCase):
    def test_deferred_guidance_is_readable_and_integrity_bound(self):
        for relative in check_core.ADAPTER_RESOURCES:
            name = relative.removeprefix('plugin/')
            with self.subTest(name=name):
                result = self.bound('read-workflow', name)
                self.assertEqual(result.returncode, 0, result.stderr)
                path = self.plugin / name
                original = path.read_bytes()
                self.assertEqual(result.stdout, original.decode())
                path.write_bytes(original + b'\ndrift\n')
                self.assertEqual(self.bound('read-workflow', name).returncode, 2)
                path.write_bytes(original)
