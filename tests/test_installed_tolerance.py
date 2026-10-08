"""Installed-payload regressions from the PR 17 review: host files, modes and raw skill reads."""
import os
import shlex
import subprocess
import unittest
from unittest.mock import patch

from test_host_adapters import InstalledFixture

FEATURE = 'skills/hugues-mode/playbooks/feature.md'


class InstalledTolerance(InstalledFixture, unittest.TestCase):
    def test_bootstrap_dependencies_do_not_block_bound_helpers(self):
        modules = self.plugin / 'skills/hugues-mode/scripts/node_modules'
        (modules / 'commander').mkdir(parents=True)
        (modules / 'commander/package.json').write_text('{}\n')
        (modules / '.bin').mkdir()
        (modules / '.bin/commander').symlink_to('../commander/package.json')
        result = self.bound('read-workflow', FEATURE)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_host_metadata_files_do_not_block_bound_helpers(self):
        for name in ['.DS_Store', 'skills/hugues-mode/.DS_Store']:
            with self.subTest(name=name):
                (self.plugin / name).write_bytes(b'')
                result = self.bound('read-workflow', FEATURE)
                self.assertEqual(result.returncode, 0, result.stderr)

    def test_extra_file_beside_bootstrap_dependencies_is_still_rejected(self):
        for name in ['skills/hugues-mode/scripts/extra.md', 'skills/hugues-mode/node_modules/x.js']:
            with self.subTest(name=name):
                path = self.plugin / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text('extra\n')
                result = self.bound('read-workflow', FEATURE)
                self.assertEqual(result.returncode, 2)
                self.assertIn('inventory differs', result.stderr)
                path.unlink()

    def test_unreadable_directory_holds_instead_of_shrinking_the_inventory(self):
        # Injected, because chmod 000 does not deny reads when the suite runs as root.
        from runtime import payload
        folder = str(self.plugin / 'skills/hugues-mode/references')
        scandir = os.scandir
        def denied(path='.'):
            if os.fspath(path) == folder:
                raise PermissionError(13, 'Permission denied', folder)
            return scandir(path)
        with patch('os.scandir', denied), self.assertRaises(PermissionError):
            payload.inventory(self.plugin, allow_runtime_cache=True)

    def test_metadata_name_cannot_hide_a_directory_or_symlink(self):
        path = self.plugin / 'skills/.DS_Store'
        path.symlink_to('hugues-mode/SKILL.md')
        result = self.bound('read-workflow', FEATURE)
        self.assertEqual(result.returncode, 2)

    def test_group_writable_install_binds_and_runs(self):
        # umask 002 (user private groups) and git-archive extraction both give 664/775.
        for path in self.plugin.rglob('*'):
            path.chmod(path.stat().st_mode | 0o020)
        bound = self.run_tool('bind')
        self.assertEqual(bound.returncode, 0, bound.stderr)
        self.binding.write_text(bound.stdout)
        result = self.bound('read-workflow', FEATURE)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_world_writable_or_executable_drift_is_still_rejected(self):
        cases = [('adapters/host_tools.py', 0o646), ('adapters/runtime/payload.json', 0o666),
                 ('adapters/runtime/activity.py', 0o646), ('adapters/runtime/payload.py', 0o755),
                 ('skills/hugues-mode/scripts/watch-pr/watch-pr', 0o644), (FEATURE, 0o755),
                 (FEATURE, 0o646)]
        for name, mode in cases:
            with self.subTest(name=name, mode=oct(mode)):
                path = self.plugin / name
                original = path.stat().st_mode & 0o777
                path.chmod(mode)
                self.assertEqual(self.run_tool('bind').returncode, 2)
                path.chmod(original)

    def test_translate_refuses_every_malformed_spelling_of_a_raw_skill_read(self):
        # None of these spell the exact, literal bundled path `skills/tdd/SKILL.md`, so none
        # resolves to an approved installed payload entry; native invocation is still required.
        for text in ['cat /abs/plugin/skills/tdd/SKILL.md',
                     'cat plugin/skills/tdd/SKILL.md',
                     "`cat 'plugin/skills/tdd/SKILL.md'`",
                     'Read (plugin/skills/tdd/SKILL.md) first.']:
            with self.subTest(text=text):
                plan = self.consumer / 'plan.md'
                plan.write_text(text + '\n')
                result = self.bound('translate-plan', plan)
                self.assertEqual(result.returncode, 2, result.stdout)
                self.assertIn('native skill invocation', result.stderr)
        plan = self.consumer / 'plan.md'
        plan.write_text('Each public skill keeps one SKILL.md body.\n')
        prose = self.bound('translate-plan', plan)
        self.assertEqual((prose.returncode, prose.stdout), (0, plan.read_text()), prose.stderr)

    def test_translate_allows_a_bundled_skill_body_spelled_exactly(self):
        # A bundled user-only skill's own SKILL.md, spelled as the exact literal payload path
        # (however quoted), is the mode's reference and translates to a guarded read-workflow.
        for text in ["cat skills/tdd/SK''ILL.md", 'cat "skills/tdd/SKILL.md"']:
            with self.subTest(text=text):
                plan = self.consumer / 'plan.md'
                plan.write_text(text + '\n')
                result = self.bound('translate-plan', plan)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn('read-workflow', result.stdout)
                command = result.stdout.strip('`\n')
                reread = subprocess.run(shlex.split(command), cwd=self.consumer, capture_output=True, text=True)
                self.assertEqual(reread.returncode, 0, reread.stderr)
                self.assertEqual(reread.stdout, (self.plugin / 'skills/tdd/SKILL.md').read_text())

    def test_read_workflow_refuses_every_malformed_spelling_of_a_skill_body(self):
        for source in ['skills/tdd//SKILL.md', './skills/tdd/SKILL.md', 'SKILL.md']:
            with self.subTest(source=source):
                result = self.bound('read-workflow', source)
                self.assertEqual(result.returncode, 2)
                self.assertIn('native skill invocation', result.stderr)

    def test_read_workflow_allows_a_bundled_user_only_skill_body(self):
        # The exact literal path of a bundled, user-only skill's SKILL.md is the mode's
        # reference once it is in the approved installed payload: a guarded read, not a
        # native invocation.
        result = self.bound('read-workflow', 'skills/tdd/SKILL.md')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, (self.plugin / 'skills/tdd/SKILL.md').read_text())

    def test_translate_rejects_a_skill_body_at_any_revision_other_than_origin_main(self):
        # PR 1 fix round 2 security regression: `git show <rev>:<path>/SKILL.md` returned
        # the literal plan text unchanged for every revision other than `origin/main`,
        # skipping the skill-body guard entirely. That held for a consumer path
        # (`.claude/skills/...`) and even for a bundled, approved path
        # (`skills/tdd/SKILL.md`) read at the wrong revision -- both must still require
        # native invocation, exactly as the pre-regression `a67df90` translator did.
        for text in ['git show HEAD:.claude/skills/mine/SKILL.md',
                     'git show HEAD:.agents/skills/mine/SKILL.md',
                     'git show HEAD:skills/tdd/SKILL.md',
                     'git show feature-branch:plugin/skills/other-plugin/SKILL.md']:
            with self.subTest(text=text):
                plan = self.consumer / 'plan.md'
                plan.write_text(text + '\n')
                result = self.bound('translate-plan', plan)
                self.assertEqual(result.returncode, 2, result.stdout)
                self.assertIn('native skill invocation', result.stderr)

    def test_translate_rejects_consumer_and_external_skill_body_paths(self):
        # A consumer's own `.claude/skills/...` or `.agents/skills/...` convention, and an
        # external plugin's skill, are never bundled references: no guarded read ever
        # substitutes for their native invocation.
        for text in ['cat .claude/skills/mine/SKILL.md',
                     'cat .agents/skills/mine/SKILL.md',
                     '`other-plugin/skills/foo/SKILL.md`']:
            with self.subTest(text=text):
                plan = self.consumer / 'plan.md'
                plan.write_text(text + '\n')
                result = self.bound('translate-plan', plan)
                self.assertEqual(result.returncode, 2, result.stdout)
                self.assertIn('native skill invocation', result.stderr)

    def test_translate_distinguishes_unsupported_syntax_on_a_bundled_body_from_native_only(self):
        # `sed`/other unsupported shell forms naming a KNOWN, approved bundled SKILL.md are
        # a syntax problem, not a permission problem: the author can fix it by using one of
        # the supported literal forms (a plain reference, `cat`, or `git show origin/main:`).
        # That is a different, more specific failure than "native skill invocation
        # required", which means no guarded read could ever satisfy the reference.
        for text in ['sed -n 1,5p skills/tdd/SKILL.md', 'head skills/tdd/SKILL.md']:
            with self.subTest(text=text):
                plan = self.consumer / 'plan.md'
                plan.write_text(text + '\n')
                result = self.bound('translate-plan', plan)
                self.assertEqual(result.returncode, 2, result.stdout)
                self.assertIn('standalone guarded read', result.stderr)
                self.assertNotIn('native skill invocation', result.stderr)

    def test_read_workflow_and_translate_keep_model_invocable_skills_native_only(self):
        # `hugues-mode` and `setup-huguesstack` stay model-invocable; their own SKILL.md is
        # never a guarded bundled reference, even though it sits in the approved installed
        # payload like every user-only skill's body does. Allowing it would let the router
        # read -- and so effectively invoke -- the two skills a host's native denial is
        # actually meant to gate.
        for source in ['skills/hugues-mode/SKILL.md', 'skills/setup-huguesstack/SKILL.md',
                       'pstack/skills/poteto-mode/SKILL.md', 'pstack/skills/setup-pstack/SKILL.md']:
            with self.subTest(source=source):
                result = self.bound('read-workflow', source)
                self.assertEqual(result.returncode, 2)
                self.assertIn('native skill invocation', result.stderr)
        for text in ['cat skills/hugues-mode/SKILL.md', 'cat skills/setup-huguesstack/SKILL.md',
                     'git show origin/main:skills/hugues-mode/SKILL.md',
                     '`skills/setup-huguesstack/SKILL.md`']:
            with self.subTest(text=text):
                plan = self.consumer / 'plan.md'
                plan.write_text(text + '\n')
                result = self.bound('translate-plan', plan)
                self.assertEqual(result.returncode, 2, result.stdout)
                self.assertIn('native skill invocation', result.stderr)


if __name__ == '__main__':
    unittest.main()
