from pathlib import Path
import unittest
ROOT = Path(__file__).resolve().parents[1]
class NativeLayout(unittest.TestCase):
    def test_native_entry_owns_architect_phases_without_runtime_core(self):
        body = (ROOT / 'plugin/skills/architect/SKILL.md').read_text()
        self.assertIn('## Phase A: Ground the problem', body)
        self.assertIn('## Phase E: Scrap when the architecture is wrong', body)
        self.assertFalse((ROOT / 'plugin/core').exists())

from test_host_adapters import InstalledFixture
class NativeInstalled(InstalledFixture, unittest.TestCase):
    def test_installed_playbook_read_and_native_skill_boundary(self):
        result = self.bound('read-workflow', 'skills/hugues-mode/playbooks/feature.md')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('Mandatory: no skip-with-reason escape', result.stdout)
        for path in ['skills/swarm/SKILL.md', 'pstack/skills/swarm/SKILL.md']:
            denied = self.bound('read-workflow', path)
            self.assertEqual(denied.returncode, 2)
            self.assertIn('native skill invocation', denied.stderr)

    def test_translate_does_not_bypass_native_skill_invocation(self):
        for text in ['`pstack/skills/swarm/SKILL.md`',
                     'cat skills/swarm/SKILL.md',
                     'git show origin/main:skills/swarm/SKILL.md']:
            with self.subTest(text=text):
                plan = self.consumer / 'plan.md'
                plan.write_text(text)
                result = self.bound('translate-plan', plan)
                self.assertEqual(result.returncode, 2)
                self.assertIn('native skill invocation', result.stderr)

    def test_initial_binding_rejects_adapter_and_native_metadata_drift(self):
        for name in ['adapters/mobile.md', 'policies/astra-pr-review.md',
                     'skills/swarm/agents/openai.yaml']:
            with self.subTest(name=name):
                path = self.plugin / name
                original = path.read_bytes()
                path.write_bytes(original + b'\nchanged\n')
                self.assertEqual(self.run_tool('bind').returncode, 2)
                path.write_bytes(original)

    def test_legacy_binding_is_not_silently_rebound(self):
        import json
        data = json.loads(self.binding.read_text())
        data['revision'] = 'e43c7ee26e0038c6c1fa8380dd34ce86ff94cb2a'
        self.binding.write_text(json.dumps(data))
        result = self.bound('read-workflow', 'skills/hugues-mode/playbooks/feature.md')
        self.assertEqual(result.returncode, 2)

    def test_initial_bind_rejects_trust_anchor_permission_drift(self):
        for name in ['adapters/host_tools.py', 'adapters/runtime/payload.py',
                     'adapters/runtime/payload.json']:
            with self.subTest(name=name):
                path = self.plugin / name
                mode = path.stat().st_mode & 0o777
                path.chmod(0o600)
                self.assertEqual(self.run_tool('bind').returncode, 2)
                path.chmod(mode)


import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
sys.path.insert(0, str(ROOT / 'scripts'))
import check_core
import seal_payload


class NativeIntegrity(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix='huguesstack-native-contract-')
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name) / 'package'
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns('.git', '__pycache__', 'planning'))

    def rejected(self):
        with self.assertRaises((ValueError, OSError, KeyError, TypeError)):
            check_core.check(self.root)

    def test_current_package_and_public_inventory(self):
        result = check_core.check(self.root)
        self.assertEqual(result['active_skills'], 50)
        self.assertEqual(result['upstream_archive_files'], 161)

    def test_missing_receipt_cannot_disable_integrity(self):
        (self.root / 'docs/upstream/consolidation.json').unlink()
        result = subprocess.run([sys.executable, str(self.root / 'scripts/check_plugin.py')],
                                capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)

    def test_extra_skill_cannot_become_a_second_canonical_declaration(self):
        folder = self.root / 'plugin/skills/extra'
        folder.mkdir()
        (folder / 'SKILL.md').write_text((self.root / 'plugin/skills/arena/SKILL.md').read_text())
        self.rejected()

    def test_removed_required_reference_is_rejected(self):
        (self.root / 'plugin/skills/architect/references/runner-prompt.md').unlink()
        self.rejected()

    def test_extra_file_is_rejected(self):
        (self.root / 'plugin/unapproved.md').write_text('unreviewed')
        self.rejected()

    def test_non_executable_permission_drift_is_rejected(self):
        (self.root / 'plugin/skills/arena/SKILL.md').chmod(0o600)
        self.rejected()

    def test_symlink_shadow_is_rejected(self):
        path = self.root / 'plugin/skills/arena/SKILL.md'
        path.unlink()
        path.symlink_to('../architect/SKILL.md')
        self.rejected()

    def test_corrupt_source_archive_is_rejected(self):
        path = self.root / 'provenance/upstream/pstack-0.15.9.tar.gz'
        path.write_bytes(path.read_bytes() + b'changed')
        self.rejected()

    def test_sealing_does_not_approve_lost_workflow_gates(self):
        path = self.root / 'plugin/skills/architect/SKILL.md'
        path.write_text(path.read_text().replace('at least two structurally distinct candidates', 'one candidate'))
        seal_payload.seal(self.root)
        self.rejected()

    def test_sealing_does_not_approve_lost_invocation_boundary(self):
        path = self.root / 'plugin/skills/architect/SKILL.md'
        self.assertIn('The host contract supersedes inherited sibling-body reads.', path.read_text())
        path.write_text(path.read_text().replace('The host contract supersedes inherited sibling-body reads.', 'read any skill body'))
        seal_payload.seal(self.root)
        self.rejected()

    def test_native_policy_mutation_is_rejected_even_after_sealing(self):
        path = self.root / 'plugin/skills/architect/agents/openai.yaml'
        path.write_text('policy:\n  allow_implicit_invocation: true\n')
        seal_payload.seal(self.root)
        self.rejected()

    def test_public_name_cannot_change_after_sealing(self):
        path = self.root / 'plugin/skills/hugues-mode/SKILL.md'
        path.write_text(path.read_text().replace('name: hugues-mode', 'name: poteto-mode'))
        seal_payload.seal(self.root)
        self.rejected()

    def test_role_prompt_mapping_cannot_change_after_sealing(self):
        path = self.root / 'docs/upstream/consolidation.json'
        data = json.loads(path.read_text())
        data['worker_roles']['reflect-tooling']['prompt'] = 'plugin/skills/reflect/references/judgment-reviewer.md'
        path.write_text(json.dumps(data))
        seal_payload.seal(self.root)
        self.rejected()

    def test_source_identity_cannot_be_swapped_by_resealing(self):
        path = self.root / 'docs/upstream/consolidation.json'
        data = json.loads(path.read_text())
        rows = {row['source']: row for row in data['files']}
        a, b = rows['pstack/skills/bro/SKILL.md'], rows['pstack/skills/benchmark-checklist/SKILL.md']
        a['destination'], b['destination'] = b['destination'], a['destination']
        path.write_text(json.dumps(data))
        seal_payload.seal(self.root)
        self.rejected()

    def test_manual_only_cannot_be_removed_from_both_native_metadata_files(self):
        path = self.root / 'plugin/skills/architect/SKILL.md'
        path.write_text(path.read_text().replace('disable-model-invocation: true\n', ''))
        (path.parent / 'agents/openai.yaml').write_text('policy:\n  allow_implicit_invocation: true\n')
        seal_payload.seal(self.root)
        self.rejected()

    def test_seal_rejects_escaping_destination_before_any_write(self):
        path = self.root / 'docs/upstream/consolidation.json'
        data = json.loads(path.read_text())
        data['files'][0]['destination'] = '../outside.md'
        path.write_text(json.dumps(data))
        before = {name: (self.root / 'plugin' / name).read_bytes() for name in seal_payload.ANCHORS}
        with self.assertRaises(ValueError):
            seal_payload.seal(self.root)
        self.assertEqual(before, {name: (self.root / 'plugin' / name).read_bytes() for name in before})

    def test_standalone_checker_and_seal_reject_ancestor_symlink(self):
        source = self.root / 'provenance/upstream'
        target = self.root / 'provenance/original'
        source.rename(target)
        source.symlink_to('original', target_is_directory=True)
        self.rejected()
        with self.assertRaises(ValueError):
            seal_payload.seal(self.root)

    def test_mode_principles_consultation_cannot_restart_routing(self):
        path = self.root / 'plugin/adapters/host.md'
        path.write_text(path.read_text().replace('never restart task routing', 'restart task routing'))
        seal_payload.seal(self.root)
        self.rejected()

    def test_measured_context_budget_is_current_and_bounded(self):
        import measure_context
        measured = measure_context.measure(self.root)
        self.assertEqual(json.loads((self.root / 'docs/CONTEXT-BUDGET.json').read_text()), measured)
        self.assertEqual(measured['public_skills'], 50)
        self.assertLessEqual(measured['mode_initial_read_set']['candidate']['bytes'], 38000)
        self.assertLessEqual(measured['native_frontmatter']['candidate']['bytes'], 16000)

    def test_phase_contracts_reject_order_cardinality_and_fallback_mutations(self):
        names = ['architect', 'arena', 'interrogate', 'create-verification-skill',
                 'maintain-verification-skill', 'swarm', 'show-me-your-work', 'setup-pstack', 'poteto-mode', 'tdd']
        bodies = {name: (self.root / 'plugin/skills' / check_core.ALIASES.get(name, name) / 'SKILL.md').read_text()
                  for name in names}
        bodies['feature'] = (self.root / 'plugin/skills/hugues-mode/playbooks/feature.md').read_text()
        self.assertEqual(check_core.behavior_errors(bodies), [])
        for name, before, after in [('arena', '## Phase E: Graft', '## Phase Z: Graft'),
            ('interrogate', '| Reviewer C | `grok-4.7-xhigh-fast` |', '| Reviewer C | `gpt-5.6-sol-max` |'),
            ('swarm', 'A gap does not count as a pass', 'A gap counts as a pass'),
            ('tdd', '4. **Run the new test before fixing', '7. **Run the new test before fixing'),
            ('maintain-verification-skill', 'Exercise every feature at least once', 'Exercise one feature'),
            ('poteto-mode', 'Use **figure-it-out** whenever no bundled playbook fits', 'Skip unmatched work')]:
            with self.subTest(name=name):
                self.assertIn(before, bodies[name])
                changed = dict(bodies)
                changed[name] = changed[name].replace(before, after)
                self.assertTrue(check_core.behavior_errors(changed))
