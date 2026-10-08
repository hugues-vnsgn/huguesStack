from pathlib import Path
import shutil
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
    @unittest.skipUnless(shutil.which('node'), 'Node unavailable; plan gate unrun')
    def test_translated_plan_without_consumer_git_read_passes_bound_gate(self):
        plan = self.consumer / 'plan with spaces.md'
        plan.write_text((ROOT / 'tests/fixtures/adapter-plan.md').read_text().replace(
            '`git show origin/main:PLAN.md`\n', ''))
        self.assertEqual(self.bound('plan-check', plan).returncode, 0)
        translated = self.bound('translate-plan', plan)
        self.assertEqual(translated.returncode, 0, translated.stderr)
        self.assertNotIn('git show origin/main:', translated.stdout)
        plan.write_text(translated.stdout)
        checked = self.bound('plan-check', plan)
        self.assertEqual(checked.returncode, 0, checked.stderr)
        plan.write_text(translated.stdout.replace('read-workflow --binding', 'read-workflow'))
        rejected = self.bound('plan-check', plan)
        self.assertEqual(rejected.returncode, 1)
        self.assertIn('bound read-workflow', rejected.stderr)

    def test_installed_playbook_read_and_bundled_skill_body_boundary(self):
        result = self.bound('read-workflow', 'skills/hugues-mode/playbooks/feature.md')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('Mandatory: no skip-with-reason escape', result.stdout)
        # `swarm` is a bundled user-only skill: its own SKILL.md is the mode's reference
        # once it resolves, including through its legacy pstack-relative alias, to the
        # approved installed payload. A guarded read, not a native invocation.
        for path in ['skills/swarm/SKILL.md', 'pstack/skills/swarm/SKILL.md']:
            with self.subTest(path=path):
                allowed = self.bound('read-workflow', path)
                self.assertEqual(allowed.returncode, 0, allowed.stderr)
                self.assertEqual(allowed.stdout, (self.plugin / 'skills/swarm/SKILL.md').read_text())
        # An unknown skill name never resolves into the approved payload, bundled or not.
        for path in ['skills/nope/SKILL.md', 'pstack/skills/nope/SKILL.md']:
            with self.subTest(path=path):
                denied = self.bound('read-workflow', path)
                self.assertEqual(denied.returncode, 2)
                self.assertIn('native skill invocation', denied.stderr)

    def test_translate_turns_a_bundled_skill_body_into_a_guarded_read(self):
        for text in ['`pstack/skills/swarm/SKILL.md`',
                     'cat skills/swarm/SKILL.md',
                     'git show origin/main:skills/swarm/SKILL.md']:
            with self.subTest(text=text):
                plan = self.consumer / 'plan.md'
                plan.write_text(text)
                result = self.bound('translate-plan', plan)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn('read-workflow', result.stdout)

    def test_translate_still_refuses_an_unknown_skill_body(self):
        for text in ['`pstack/skills/nope/SKILL.md`', 'cat skills/nope/SKILL.md',
                     'git show origin/main:skills/nope/SKILL.md']:
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
                path.chmod(0o646)
                self.assertEqual(self.run_tool('bind').returncode, 2)
                path.chmod(mode)


import hashlib
import json
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
        seal_payload.seal(self.root, accept=['plugin/skills/architect/SKILL.md'])
        self.rejected()

    def test_sealing_does_not_approve_lost_invocation_boundary(self):
        path = self.root / 'plugin/skills/architect/SKILL.md'
        self.assertIn('The host contract governs how this skill reaches any sibling dependency.', path.read_text())
        path.write_text(path.read_text().replace('The host contract governs how this skill reaches any sibling dependency.', 'read any skill body'))
        seal_payload.seal(self.root, accept=['plugin/skills/architect/SKILL.md'])
        self.rejected()

    def test_native_policy_mutation_is_rejected_even_after_sealing(self):
        path = self.root / 'plugin/skills/setup-huguesstack/agents/openai.yaml'
        path.write_text('policy:\n  allow_implicit_invocation: false\n')
        seal_payload.seal(self.root)
        self.rejected()

    def test_public_name_cannot_change_after_sealing(self):
        path = self.root / 'plugin/skills/hugues-mode/SKILL.md'
        path.write_text(path.read_text().replace('name: hugues-mode', 'name: poteto-mode'))
        seal_payload.seal(self.root, accept=['plugin/skills/hugues-mode/SKILL.md'])
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
        seal_payload.seal(self.root, accept=['plugin/skills/bro/SKILL.md', 'plugin/skills/benchmark-checklist/SKILL.md'])
        self.rejected()

    def test_manual_only_cannot_be_removed_from_both_native_metadata_files(self):
        path = self.root / 'plugin/skills/reflect/SKILL.md'
        path.write_text(path.read_text().replace('disable-model-invocation: true\n', ''))
        (path.parent / 'agents/openai.yaml').write_text('policy:\n  allow_implicit_invocation: true\n')
        seal_payload.seal(self.root, accept=['plugin/skills/reflect/SKILL.md'])
        self.rejected()

    def test_dependency_skill_cannot_become_manual_only(self):
        path = self.root / 'plugin/skills/setup-huguesstack/SKILL.md'
        path.write_text(path.read_text().replace('\n---\n', '\ndisable-model-invocation: true\n---\n', 1))
        (path.parent / 'agents/openai.yaml').write_text('policy:\n  allow_implicit_invocation: false\n')
        seal_payload.seal(self.root, accept=['plugin/skills/setup-huguesstack/SKILL.md'])
        self.rejected()

    def test_verbatim_port_may_only_drop_the_inherited_manual_only_line(self):
        path = self.root / 'plugin/skills/principle-fix-root-causes/SKILL.md'
        path.write_text(path.read_text() + 'Extra rule.\n')
        seal_payload.seal(self.root, accept=['plugin/skills/principle-fix-root-causes/SKILL.md'])
        result = subprocess.run([sys.executable, str(self.root / 'scripts/upstream-diff.py'), 'check',
                                 '--root', str(self.root)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn('verbatim destination differs', result.stderr)

    def test_host_invocation_receipt_cannot_add_a_user_only_entry(self):
        path = self.root / 'docs/upstream/consolidation.json'
        data = json.loads(path.read_text())
        data['host_invocation']['user_only'] = sorted(data['host_invocation']['user_only'] + ['architect'])
        path.write_text(json.dumps(data))
        self.rejected()

    def test_manual_only_comment_cannot_override_effective_false(self):
        path = self.root / 'plugin/skills/reflect/SKILL.md'
        path.write_text(path.read_text().replace('disable-model-invocation: true\n',
            'disable-model-invocation: false\n# Previous setting: disable-model-invocation: true\n'))
        seal_payload.seal(self.root, accept=['plugin/skills/reflect/SKILL.md'])
        self.rejected()

    def test_duplicate_native_invocation_field_is_rejected(self):
        path = self.root / 'plugin/skills/reflect/SKILL.md'
        path.write_text(path.read_text().replace('disable-model-invocation: true\n',
            'disable-model-invocation: true\ndisable-model-invocation: false\n'))
        seal_payload.seal(self.root, accept=['plugin/skills/reflect/SKILL.md'])
        self.rejected()

    def test_seal_refuses_unaccepted_canonical_change_before_any_write(self):
        path = self.root / 'plugin/skills/hugues-mode/scripts/check-plan.mjs'
        path.write_text(path.read_text() + '\n// appended\n')
        receipt = (self.root / 'docs/upstream/consolidation.json').read_bytes()
        with self.assertRaisesRegex(ValueError, 'check-plan.mjs'):
            seal_payload.seal(self.root)
        self.assertEqual((self.root / 'docs/upstream/consolidation.json').read_bytes(), receipt)
        self.rejected()
        seal_payload.seal(self.root, accept=['plugin/skills/hugues-mode/scripts/check-plan.mjs'])
        self.rejected()

    def test_helper_input_receipt_cannot_go_stale(self):
        path = self.root / 'docs/HELPER-INPUTS.json'
        data = json.loads(path.read_text())
        row = next(r for r in data['files'] if r['installed'] and r['installed'].endswith('/bun.lock'))
        row['same_bytes_as_upstream'] = False
        path.write_text(json.dumps(data))
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
            ('interrogate', '| Reviewer C | `inherit-parent max` |', '| Reviewer C | `opus max` |'),
            ('swarm', 'A gap does not count as a pass', 'A gap counts as a pass'),
            ('tdd', '4. **Run the new test before fixing', '7. **Run the new test before fixing'),
            ('maintain-verification-skill', 'Exercise every feature at least once', 'Exercise one feature'),
            ('poteto-mode', 'Use **figure-it-out** whenever no bundled playbook fits', 'Skip unmatched work')]:
            with self.subTest(name=name):
                self.assertIn(before, bodies[name])
                changed = dict(bodies)
                changed[name] = changed[name].replace(before, after)
                self.assertTrue(check_core.behavior_errors(changed))
