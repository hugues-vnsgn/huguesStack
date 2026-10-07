"""Actual installed entrypoints in external consumer repos; synthetic history only."""
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'plugin/adapters'))
from runtime import activity


class InstalledFixture:
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='huguesstack-consumer-')
        self.addCleanup(self.temp.cleanup)
        self.area = Path(self.temp.name).resolve()
        self.plugin = self.area / 'installed plugin with spaces'
        shutil.copytree(ROOT / 'plugin', self.plugin, ignore=shutil.ignore_patterns('__pycache__'))
        self.consumer = self.area / 'consumer with spaces'
        self.consumer.mkdir()
        self.helper = self.plugin / 'adapters/host_tools.py'
        self.binding = self.area / 'binding.json'
        self.binding.write_text(self.run_tool('bind').stdout)

    def run_tool(self, *args, **kwargs):
        return subprocess.run([sys.executable, str(self.helper), *map(str, args)],
                              cwd=self.consumer, capture_output=True, text=True, **kwargs)

    def bound(self, verb, *args, **kwargs):
        return self.run_tool(verb, '--binding', self.binding, *args, **kwargs)


class InstalledAdapters(InstalledFixture, unittest.TestCase):
    def test_installed_read_outside_plugin_without_git(self):
        source = 'pstack/skills/swarm/SKILL.md'
        self.assertFalse((self.plugin / '.git').exists())
        self.assertFalse((self.consumer / 'pstack').exists())
        result = self.bound('read-workflow', source)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, (self.plugin / 'core' / source).read_text())

    def test_binding_is_revision_and_adapter_bound(self):
        data = json.loads(self.binding.read_text())
        self.assertEqual(data['revision'], 'e43c7ee26e0038c6c1fa8380dd34ce86ff94cb2a')
        self.assertIn('adapters/runtime/activity.py', data['adapter_sha256'])
        self.assertEqual(data['plugin_root'], str(self.plugin))

    def test_workflow_drift_blocks_tick(self):
        path = self.plugin / 'core/pstack/skills/swarm/SKILL.md'
        path.write_text(path.read_text() + '\nchanged\n')
        result = self.bound('read-workflow', 'pstack/skills/swarm/SKILL.md')
        self.assertEqual(result.returncode, 2)
        self.assertIn('workflow bytes/mode drift', result.stderr)

    def test_adapter_drift_blocks_tick(self):
        path = self.plugin / 'adapters/host.md'
        path.write_text(path.read_text() + '\nchanged\n')
        self.assertIn('binding changed', self.bound('read-workflow', 'pstack/skills/swarm/SKILL.md').stderr)

    def test_mode_drift_blocks_tick(self):
        path = self.plugin / 'core/pstack/skills/poteto-mode/scripts/worktree-audit.sh'
        path.chmod(0o644)
        self.assertEqual(self.bound('read-workflow', 'pstack/skills/swarm/SKILL.md').returncode, 2)

    def test_missing_installed_helper_blocks_validation(self):
        (self.plugin / 'core/pstack/skills/poteto-mode/scripts/check-plan.mjs').unlink()
        result = self.bound('plan-check', self.consumer / 'plan.md')
        self.assertEqual(result.returncode, 2)
        self.assertIn('missing installed payload', result.stderr)

    def test_manifest_drift_blocks_binding(self):
        (self.plugin / 'adapters/runtime/payload.json').write_text('{}')
        self.assertEqual(self.run_tool('bind').returncode, 2)

    def test_unknown_or_escaping_workflow_rejected(self):
        for path in ['../private.md', '/etc/passwd', 'pstack/skills/nope/SKILL.md', 'pstack/skills/swarm/../../private.md']:
            with self.subTest(path=path):
                self.assertEqual(self.bound('read-workflow', path).returncode, 2)

    def test_binding_does_not_follow_moved_installation(self):
        moved = self.area / 'replacement plugin'
        self.plugin.rename(moved)
        self.helper = moved / 'adapters/host_tools.py'
        self.assertEqual(self.bound('read-workflow', 'pstack/skills/swarm/SKILL.md').returncode, 2)

    def test_symlink_payload_rejected(self):
        source = self.plugin / 'core/pstack/skills/swarm/SKILL.md'
        saved = self.area / 'saved.md'
        source.rename(saved)
        source.symlink_to(saved)
        self.assertEqual(self.bound('read-workflow', 'pstack/skills/swarm/SKILL.md').returncode, 2)

    def test_translation_executes_bound_workflow_and_keeps_consumer_trunk(self):
        draft = self.consumer / 'draft.md'
        draft.write_text((ROOT / 'tests/fixtures/adapter-plan.md').read_text())
        result = self.bound('translate-plan', draft)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('git show origin/main:PLAN.md', result.stdout)
        self.assertNotIn('git show origin/main:pstack/', result.stdout)
        self.assertNotIn('node pstack/', result.stdout)
        command = next(line for line in result.stdout.splitlines() if 'read-workflow --binding' in line)
        reread = subprocess.run(shlex.split(command), cwd=self.consumer, capture_output=True, text=True)
        self.assertEqual(reread.returncode, 0, reread.stderr)
        self.assertEqual(reread.stdout, (self.plugin / 'core/pstack/skills/swarm/SKILL.md').read_text())

    @unittest.skipUnless(shutil.which('node'), 'Node unavailable; plan gate unrun')
    def test_translated_plan_passes_and_invalid_live_gate_fails(self):
        plan = self.consumer / 'plan with spaces.md'
        plan.write_text((ROOT / 'tests/fixtures/adapter-plan.md').read_text())
        translated = self.bound('translate-plan', plan)
        self.assertEqual(translated.returncode, 0, translated.stderr)
        plan.write_text(translated.stdout)
        valid = self.bound('plan-check', plan)
        self.assertEqual(valid.returncode, 0, valid.stderr + valid.stdout)
        plan.write_text(plan.read_text().replace('**Verify, live.** Tests alone', '**Verify, live.** Tests suffice. Tests alone'))
        bad = self.bound('plan-check', plan)
        self.assertEqual(bad.returncode, 1)
        self.assertIn('Verify, live. does not open with the rule', bad.stderr)

    def test_missing_node_is_explicit_block(self):
        result = self.bound('plan-check', self.consumer / 'plan.md', env=dict(os.environ, PATH=''))
        self.assertEqual(result.returncode, 2)
        self.assertIn('Node unavailable', result.stderr)

    def test_public_bridges_route_actual_adapter(self):
        for name in ['multi-phase-plan', 'autopilot-full', 'autopilot-stack']:
            self.assertIn('read-workflow', (self.plugin / f'skills/hugues-mode/playbooks/{name}.md').read_text())
        cleanup = (self.plugin / 'skills/hugues-mode/playbooks/worktree-cleanup.md').read_text()
        self.assertIn('host_tools.py worktree-audit', cleanup)
        self.assertIn('separate active/pinned-chat gate', cleanup)


class SyntheticActivity(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix='huguesstack-synthetic-history-')
        self.addCleanup(temp.cleanup)
        self.area = Path(temp.name).resolve()
        self.wt = self.area / 'worktree with spaces'
        self.other = Path(str(self.wt) + '-sibling')
        self.now = datetime.now(timezone.utc).timestamp()
        self.stamp = datetime.fromtimestamp(self.now, timezone.utc).isoformat()

    def scan(self, provider, rows, **kwargs):
        source = self.area / (provider + '.jsonl')
        source.write_text('\n'.join(json.dumps(r) for r in rows) + '\n')
        manifest = {'coverage': 'complete', 'sources': [{'provider': provider, 'files': [str(source)],
                    'authorization': 'task-owned synthetic fixtures only', 'coverage': 'complete'}]}
        manifest.update(kwargs)
        return activity.scan(manifest, [self.wt, self.other], self.now)

    def claude(self, **kwargs):
        row = {'type': 'assistant', 'timestamp': self.stamp, 'cwd': str(self.wt),
               'message': {'content': [{'type': 'tool_use', 'name': 'Read', 'input': {'file_path': 'README.md'}}]}}
        row.update(kwargs)
        return row

    def codex(self, **kwargs):
        row = {'type': 'response_item', 'timestamp': self.stamp,
               'payload': {'type': 'function_call', 'name': 'exec_command',
                           'arguments': json.dumps({'cmd': 'cat README.md', 'workdir': str(self.wt)})}}
        row.update(kwargs)
        return row

    def test_claude_native_cwd_and_relative_read(self):
        hits, _, complete = self.scan('claude', [self.claude()])
        self.assertTrue(complete)
        self.assertTrue(hits[str(self.wt)][0]['recent'])

    def test_codex_function_arguments_without_session_meta(self):
        hits, _, complete = self.scan('codex', [self.codex()])
        self.assertTrue(complete)
        self.assertTrue(hits[str(self.wt)][0]['recent'])

    def test_codex_session_context_relative_operation(self):
        row = self.codex(payload={'type': 'function_call', 'name': 'exec_command', 'arguments': json.dumps({'cmd': 'cat README.md'})})
        meta = {'type': 'session_meta', 'timestamp': self.stamp, 'payload': {'cwd': str(self.wt)}}
        hits, _, complete = self.scan('codex', [meta, row])
        self.assertTrue(complete)
        self.assertEqual(len(hits[str(self.wt)]), 2)



    def test_exact_boundary_excludes_sibling_prefix(self):
        hits, _, complete = self.scan('codex', [self.codex(payload={'type': 'function_call', 'name': 'exec_command', 'arguments': json.dumps({'cmd': 'cat README.md', 'workdir': str(self.other)})})])
        self.assertTrue(complete)
        self.assertFalse(hits[str(self.wt)])
        self.assertTrue(hits[str(self.other)])

    def test_old_record_not_overridden_by_fresh_file_mtime(self):
        old = datetime.fromtimestamp(self.now - 6 * 86400, timezone.utc).isoformat()
        hits, _, complete = self.scan('claude', [self.claude(timestamp=old)])
        self.assertTrue(complete)
        self.assertFalse(hits[str(self.wt)][0]['recent'])

    def test_future_timestamp_is_conservative_recent(self):
        hits, _, complete = self.scan('claude', [self.claude(timestamp=self.now + 86400)])
        self.assertTrue(complete)
        self.assertTrue(hits[str(self.wt)][0]['recent'])

    def test_missing_sources_and_partial_coverage_hold(self):
        self.assertFalse(activity.scan({'coverage': 'complete', 'sources': []}, [self.wt], self.now)[2])
        self.assertFalse(self.scan('claude', [self.claude()], coverage='partial')[2])

    def test_unsupported_envelope_and_bad_timestamp_hold(self):
        for row in [self.claude(type='unknown'), self.claude(timestamp='not-a-time'),
                    self.claude(timestamp=[]), self.claude(cwd=['bad']), self.claude(message='bad')]:
            with self.subTest(row=row):
                self.assertFalse(self.scan('claude', [row])[2])

    def test_relative_operation_without_context_holds(self):
        row = self.codex(payload={'type': 'function_call', 'name': 'exec_command', 'arguments': json.dumps({'cmd': 'cat README.md'})})
        self.assertFalse(self.scan('codex', [row])[2])
        row = self.claude(cwd=None)
        self.assertFalse(self.scan('claude', [row])[2])
        for cmd in ['pwd', 'ls', 'cat']:
            row = self.codex(payload={'type': 'function_call', 'name': 'exec_command', 'arguments': json.dumps({'cmd': cmd})})
            self.assertFalse(self.scan('codex', [row])[2])

    def test_malformed_encoded_arguments_hold(self):
        row = self.codex(payload={'type': 'function_call', 'name': 'exec_command', 'arguments': '{unfinished'})
        self.assertFalse(self.scan('codex', [row])[2])

    def test_supported_hosts_and_nested_subagents_are_scanned(self):
        sources = []
        for provider, row in [('claude', self.claude()), ('codex', self.codex())]:
            root = self.area / provider
            child = root / 'subagents' / 'nested.jsonl'
            child.parent.mkdir(parents=True)
            child.write_text(json.dumps(row) + '\n')
            sources.append({'provider': provider, 'root': str(root), 'authorization': 'synthetic only', 'coverage': 'complete'})
        hits, reports, complete = activity.scan({'coverage': 'complete', 'sources': sources}, [self.wt], self.now)
        self.assertTrue(complete)
        self.assertEqual({r['provider'] for r in hits[str(self.wt)]}, {'claude', 'codex'})
        self.assertEqual(sum(r['files_scanned'] for r in reports), 2)

    def test_empty_existing_root_differs_from_missing_root(self):
        root = self.area / 'empty'
        root.mkdir()
        manifest = {'coverage': 'complete', 'sources': [{'provider': 'claude', 'root': str(root), 'authorization': 'synthetic', 'coverage': 'complete'}]}
        self.assertTrue(activity.scan(manifest, [self.wt], self.now)[2])
        root.rmdir()
        self.assertFalse(activity.scan(manifest, [self.wt], self.now)[2])

    def test_permission_error_and_malformed_json_hold(self):
        with patch.object(activity, 'read_selected', side_effect=PermissionError('synthetic denied')):
            self.assertFalse(self.scan('claude', [self.claude()])[2])
        path = self.area / 'malformed.jsonl'
        path.write_text('{unfinished')
        manifest = {'coverage': 'complete', 'sources': [{'provider': 'claude', 'files': [str(path)], 'authorization': 'synthetic', 'coverage': 'complete'}]}
        self.assertFalse(activity.scan(manifest, [self.wt], self.now)[2])

    def test_symlink_source_cannot_escape_authorized_root(self):
        root = self.area / 'root'
        root.mkdir()
        (root / 'escape.jsonl').symlink_to(self.area / 'outside.jsonl')
        manifest = {'coverage': 'complete', 'sources': [{'provider': 'claude', 'root': str(root), 'authorization': 'synthetic', 'coverage': 'complete'}]}
        self.assertFalse(activity.scan(manifest, [self.wt], self.now)[2])

    def test_missing_selected_file_and_partial_source_hold(self):
        manifest = {'coverage': 'complete', 'sources': [{'provider': 'codex', 'files': [str(self.area / 'missing.jsonl')], 'authorization': 'synthetic', 'coverage': 'complete'}]}
        self.assertFalse(activity.scan(manifest, [self.wt], self.now)[2])
        root = self.area / 'partial'
        root.mkdir()
        manifest['sources'][0] = {'provider': 'codex', 'root': str(root), 'authorization': 'synthetic', 'coverage': 'partial'}
        self.assertFalse(activity.scan(manifest, [self.wt], self.now)[2])

    def test_absolute_alias_context_is_normalized(self):
        self.wt.mkdir()
        alias = self.area / 'alias'
        alias.symlink_to(self.wt, target_is_directory=True)
        row = self.codex(payload={'type': 'function_call', 'name': 'exec_command', 'arguments': json.dumps({'cmd': 'cat README.md', 'workdir': str(alias)})})
        hits, _, complete = self.scan('codex', [row])
        self.assertTrue(complete)
        self.assertTrue(hits[str(self.wt)])

    def test_incomplete_record_after_recent_activity_still_holds(self):
        hits, _, complete = self.scan('claude', [self.claude(), {'type': 'new-unknown-format'}])
        self.assertTrue(hits[str(self.wt)])
        self.assertFalse(complete)
        self.assertEqual(activity.classify('clean', 'NONE', True, complete, True), 'hold-activity-unavailable')

    def test_codex_shell_relative_sibling_path(self):
        cmd = shlex.join(['cat', '../' + self.other.name + '/README.md'])
        row = self.codex(payload={'type': 'function_call', 'name': 'exec_command', 'arguments': json.dumps({'cmd': cmd, 'workdir': str(self.wt)})})
        hits, _, complete = self.scan('codex', [row])
        self.assertTrue(complete)
        self.assertTrue(hits[str(self.other)])

    def test_claude_shell_relative_sibling_path(self):
        cmd = shlex.join(['cat', '../' + self.other.name + '/README.md'])
        row = self.claude(message={'content': [{'type': 'tool_use', 'name': 'Bash', 'input': {'command': cmd}}]})
        hits, _, complete = self.scan('claude', [row])
        self.assertTrue(complete)
        self.assertTrue(hits[str(self.other)])

    def test_native_patch_relative_sibling_path(self):
        patch_text = '*** Begin Patch\n*** Update File: ../' + self.other.name + '/README.md\n@@\n-old\n+new\n*** End Patch'
        meta = {'type': 'session_meta', 'timestamp': self.stamp, 'payload': {'cwd': str(self.wt)}}
        row = {'type': 'response_item', 'timestamp': self.stamp, 'payload': {'type': 'custom_tool_call', 'name': 'apply_patch', 'input': patch_text}}
        hits, _, complete = self.scan('codex', [meta, row])
        self.assertTrue(complete)
        self.assertTrue(hits[str(self.other)])

    def test_missing_or_nonobject_function_arguments_hold_with_session_context(self):
        meta = {'type': 'session_meta', 'timestamp': self.stamp, 'payload': {'cwd': str(self.wt)}}
        for payload in [{'type': 'function_call', 'name': 'exec_command'},
                        {'type': 'function_call', 'name': 'exec_command', 'arguments': '[]'},
                        {'type': 'function_call', 'name': 'exec_command', 'arguments': '{}'}]:
            self.assertFalse(self.scan('codex', [meta, self.codex(payload=payload)])[2])

    def test_opaque_shell_commands_hold(self):
        for cmd in ['cat "$TARGET"', 'cat ../*', 'cat README.md && cat elsewhere', 'python arbitrary.py']:
            row = self.codex(payload={'type': 'function_call', 'name': 'exec_command', 'arguments': json.dumps({'cmd': cmd, 'workdir': str(self.wt)})})
            self.assertFalse(self.scan('codex', [row])[2])

    def test_shell_parent_directory_and_attached_git_path(self):
        for cmd in ['ls ..', shlex.join(['git', '-C../' + self.other.name, 'status'])]:
            row = self.codex(payload={'type': 'function_call', 'name': 'exec_command', 'arguments': json.dumps({'cmd': cmd, 'workdir': str(self.wt)})})
            hits, _, complete = self.scan('codex', [row])
            self.assertTrue(complete)
            self.assertTrue(hits[str(self.other)])

    def test_malformed_source_members_return_unavailable(self):
        for entry in [[], None, 'invalid', 3]:
            manifest = {'coverage': 'complete', 'sources': [entry]}
            _, reports, complete = activity.scan(manifest, [self.wt], self.now)
            self.assertFalse(complete)
            self.assertIn('source entry must be an object', reports[0]['error'])

    def test_missing_claude_tool_input_holds(self):
        row = self.claude(message={'content': [{'type': 'tool_use', 'name': 'Read'}]})
        self.assertFalse(self.scan('claude', [row])[2])

    def test_unsupported_host_is_ignored_without_reading_or_coverage(self):
        ignored = {'provider': 'cursor', 'root': '/not-authorized/not-read', 'coverage': 'complete'}
        with patch.object(activity, 'read_selected', side_effect=AssertionError('must not read unsupported host')):
            hits, reports, complete = activity.scan({'coverage': 'complete', 'sources': [ignored]}, [self.wt], self.now)
        self.assertFalse(complete)
        self.assertFalse(hits[str(self.wt)])
        self.assertEqual(reports[0]['coverage'], 'ignored')
        root = self.area / 'authorized empty host'
        root.mkdir()
        supported = {'provider': 'claude', 'root': str(root), 'authorization': 'synthetic', 'coverage': 'complete'}
        with patch.object(activity, 'read_selected', side_effect=AssertionError('empty root has no file reads')):
            self.assertTrue(activity.scan({'coverage': 'complete', 'sources': [ignored, supported]}, [self.wt], self.now)[2])

    def test_nested_progress_and_unknown_claude_blocks_hold(self):
        nested = self.claude(type='progress', data={'type': 'agent_progress', 'message': self.claude()})
        self.assertFalse(self.scan('claude', [nested])[2])
        unknown = self.claude(message={'content': [{'type': 'tool_call', 'name': 'Bash', 'input': {'command': 'cat ../sibling/README.md'}}]})
        self.assertFalse(self.scan('claude', [unknown])[2])

    def test_relative_workdir_and_each_claude_tool_context(self):
        deep = self.area / 'tools/deep'
        relative_target = '../../' + self.other.name + '/README.md'
        meta = {'type': 'session_meta', 'payload': {'cwd': str(self.wt)}, 'timestamp': self.stamp}
        call = self.codex(payload={'type': 'function_call', 'name': 'exec_command', 'arguments': json.dumps({'cmd': shlex.join(['cat', relative_target]), 'workdir': '../tools/deep'})})
        hits, _, complete = self.scan('codex', [meta, call])
        self.assertTrue(complete)
        self.assertTrue(hits[str(self.other)])
        row = self.claude(message={'content': [
            {'type': 'tool_use', 'name': 'Bash', 'input': {'command': shlex.join(['cat', relative_target]), 'cwd': str(deep)}},
            {'type': 'tool_use', 'name': 'Read', 'input': {'file_path': 'README.md', 'cwd': str(self.wt)}}]})
        hits, _, complete = self.scan('claude', [row])
        self.assertTrue(complete)
        self.assertTrue(hits[str(self.other)])

    def test_chained_git_directories_use_effective_context(self):
        deep = self.area / 'tools/deep'
        cmd = shlex.join(['git', '-C', str(deep), '-C', '../../' + self.other.name, 'status'])
        row = self.codex(payload={'type': 'function_call', 'name': 'exec_command', 'arguments': json.dumps({'cmd': cmd, 'workdir': str(self.wt)})})
        hits, _, complete = self.scan('codex', [row])
        self.assertTrue(complete)
        self.assertTrue(hits[str(self.other)])

    def test_codex_message_blocks_require_supported_content_schema(self):
        payloads = [
            {'type': 'message', 'role': 'assistant'},
            {'type': 'message', 'role': 'assistant', 'content': 'malformed'},
            {'type': 'message', 'role': 'assistant', 'content': [{'type': 'tool_call', 'path': '../sibling'}]},
            {'type': 'message', 'role': 'assistant', 'content': [{'type': 'output_text'}]}]
        meta = {'type': 'session_meta', 'timestamp': self.stamp, 'payload': {'cwd': str(self.wt)}}
        for payload in payloads:
            self.assertFalse(self.scan('codex', [meta, self.codex(payload=payload)])[2])
        row = self.codex(payload={'type': 'message', 'role': 'assistant', 'content': [{'type': 'output_text', 'text': str(self.other)}]})
        self.assertTrue(self.scan('codex', [meta, row])[2])
        self.assertFalse(self.scan('codex', [{'type': 'session_meta', 'payload': {}}])[2])

    def test_claude_file_inputs_require_real_tool_fields_and_types(self):
        cases = [('Read', {'path': str(self.wt)}), ('Read', {'file_path': str(self.wt), 'offset': 'bad'}),
                 ('Glob', {'path': str(self.wt), 'pattern': 123}), ('Write', {'file_path': str(self.wt), 'content': 123}),
                 ('Edit', {'file_path': str(self.wt)}), ('Read', {'file_path': str(self.wt), 'extra': 'unknown'})]
        for name, args in cases:
            row = self.claude(message={'content': [{'type': 'tool_use', 'name': name, 'input': args}]})
            self.assertFalse(self.scan('claude', [row])[2])
        self.assertFalse(self.scan('claude', [self.claude(message={'content': [{'type': 'text'}]})])[2])

    def test_embedded_sed_program_is_opaque_and_holds(self):
        cmd = shlex.join(['sed', '-n', '1r ../' + self.other.name + '/README.md', 'README.md'])
        row = self.codex(payload={'type': 'function_call', 'name': 'exec_command', 'arguments': json.dumps({'cmd': cmd, 'workdir': str(self.wt)})})
        self.assertFalse(self.scan('codex', [row])[2])



    def test_no_recent_evidence_is_distinct_from_unavailable(self):
        hits, _, complete = self.scan('claude', [self.claude(cwd=str(self.other))])
        self.assertTrue(complete)
        self.assertFalse(hits[str(self.wt)])

    def test_classification_retains_wip_pr_and_active_pinned_gates(self):
        expected = [
            ('wip:1', 'NONE', True, True, False, 'hold-wip'),
            ('clean', 'OPEN', True, True, False, 'hold-open-pr'),
            ('clean', 'NONE', True, False, False, 'hold-activity-unavailable'),
            ('clean', 'NONE', True, True, True, 'verify-recent-chat'),
            ('clean', 'NONE', True, True, False, 'verify-active-pinned'),
            ('clean', 'UNKNOWN', True, True, False, 'hold-metadata-unavailable'),
            ('clean', 'NONE', None, True, False, 'hold-metadata-unavailable'),
            ('scratch:1', 'NONE', True, True, False, 'review-scratch')]
        for *args, bucket in expected:
            self.assertEqual(activity.classify(*args), bucket)


class ConsumerAudit(InstalledFixture, unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.git('init', '-b', 'main')
        self.git('config', 'user.name', 'Synthetic Fixture')
        self.git('config', 'user.email', 'fixture@example.invalid')
        (self.consumer / 'README.md').write_text('fixture\n')
        self.git('add', 'README.md')
        self.git('commit', '-m', 'fixture')
        self.wt = self.area / 'scratch worktree with spaces'
        self.git('worktree', 'add', '-b', 'scratch', str(self.wt))
        self.sources = self.area / 'sources.json'
        self.prs = self.area / 'prs.json'
        self.prs.write_text(json.dumps({'coverage': 'complete', 'states': {'main': 'NONE', 'scratch': 'NONE'}}))

    def git(self, *args):
        result = subprocess.run(['git', '-C', str(self.consumer), *args], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout

    def audit(self, manifest, *args):
        self.sources.write_text(json.dumps(manifest))
        result = self.bound('worktree-audit', '--repo', self.consumer, '--sources', self.sources,
                            '--pr-snapshot', self.prs, '--base', 'main', *args)
        return result, json.loads(result.stdout)

    def test_cli_missing_source_holds_clean_merged_worktree(self):
        result, report = self.audit({'schema_version': 1, 'coverage': 'complete', 'sources': []})
        self.assertEqual(result.returncode, 2)
        row = next(r for r in report['worktrees'] if r['worktree'] == str(self.wt))
        self.assertEqual(row['bucket'], 'hold-activity-unavailable')
        self.assertFalse(row['deletion_authorized'])

    def test_cli_each_native_provider_recent_activity(self):
        stamp = datetime.now(timezone.utc).isoformat()
        rows = {'claude': {'type': 'assistant', 'timestamp': stamp, 'cwd': str(self.wt), 'message': {'content': []}},
                'codex': {'type': 'response_item', 'timestamp': stamp, 'payload': {'type': 'function_call', 'name': 'exec_command', 'arguments': json.dumps({'cmd': 'cat README.md', 'workdir': str(self.wt)})}}}
        for provider, record in rows.items():
            with self.subTest(provider=provider):
                path = self.area / (provider + '.jsonl')
                path.write_text(json.dumps(record) + '\n')
                manifest = {'schema_version': 1, 'coverage': 'complete', 'sources': [{'provider': provider, 'files': [str(path)], 'authorization': 'synthetic only', 'coverage': 'complete'}]}
                result, report = self.audit(manifest)
                self.assertEqual(result.returncode, 0, result.stderr)
                row = next(r for r in report['worktrees'] if r['worktree'] == str(self.wt))
                self.assertEqual(row['bucket'], 'verify-recent-chat')
                self.assertEqual(row['evidence'][0]['provider'], provider)
                self.assertFalse(report['network_used'])
                self.assertFalse(report['deletion_performed'])
                self.assertTrue(self.wt.exists())

    def test_cli_complete_empty_activity_still_requires_pinned_gate(self):
        root = self.area / 'empty transcripts'
        root.mkdir()
        result, report = self.audit({'schema_version': 1, 'coverage': 'complete', 'sources': [{'provider': 'claude', 'root': str(root), 'authorization': 'synthetic empty root', 'coverage': 'complete'}]})
        self.assertEqual(result.returncode, 0)
        row = next(r for r in report['worktrees'] if r['worktree'] == str(self.wt))
        self.assertEqual(row['activity'], 'no-recent-evidence')
        self.assertEqual(row['bucket'], 'verify-active-pinned')
        self.assertEqual(row['active_pinned_gate'], 'required-separately')
        self.assertFalse(row['deletion_authorized'])

    def test_cli_relative_sibling_shell_and_patch_activity(self):
        stamp = datetime.now(timezone.utc).isoformat()
        cmd = shlex.join(['cat', '../' + self.wt.name + '/README.md'])
        patch_text = '*** Begin Patch\n*** Update File: ../' + self.wt.name + '/README.md\n@@\n-fixture\n+fixture\n*** End Patch'
        cases = [
            ('claude', [{'type': 'assistant', 'timestamp': stamp, 'cwd': str(self.consumer), 'message': {'content': [{'type': 'tool_use', 'name': 'Bash', 'input': {'command': cmd}}]}}]),
            ('codex', [{'type': 'response_item', 'timestamp': stamp, 'payload': {'type': 'function_call', 'name': 'exec_command', 'arguments': json.dumps({'cmd': cmd, 'workdir': str(self.consumer)})}}]),
            ('codex', [{'type': 'session_meta', 'timestamp': stamp, 'payload': {'cwd': str(self.consumer)}},
                       {'type': 'response_item', 'timestamp': stamp, 'payload': {'type': 'custom_tool_call', 'name': 'apply_patch', 'input': patch_text}}])]
        for provider, records in cases:
            path = self.area / 'relative.jsonl'
            path.write_text('\n'.join(json.dumps(row) for row in records) + '\n')
            result, report = self.audit({'schema_version': 1, 'coverage': 'complete', 'sources': [{'provider': provider, 'files': [str(path)], 'authorization': 'synthetic', 'coverage': 'complete'}]})
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(report['worktrees'][1]['bucket'], 'verify-recent-chat')
            self.assertTrue(self.wt.exists())

    def test_cli_malformed_source_and_function_arguments_hold(self):
        result, report = self.audit({'schema_version': 1, 'coverage': 'complete', 'sources': [[]]})
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertEqual(report['worktrees'][1]['bucket'], 'hold-activity-unavailable')
        path = self.area / 'missing-arguments.jsonl'
        stamp = datetime.now(timezone.utc).isoformat()
        rows = [{'type': 'session_meta', 'timestamp': stamp, 'payload': {'cwd': str(self.consumer)}},
                {'type': 'response_item', 'timestamp': stamp, 'payload': {'type': 'function_call', 'name': 'exec_command'}}]
        path.write_text('\n'.join(json.dumps(row) for row in rows) + '\n')
        result, report = self.audit({'schema_version': 1, 'coverage': 'complete', 'sources': [{'provider': 'codex', 'files': [str(path)], 'authorization': 'synthetic', 'coverage': 'complete'}]})
        self.assertEqual(result.returncode, 2)
        self.assertEqual(report['worktrees'][1]['bucket'], 'hold-activity-unavailable')

    def test_cli_untracked_scratch_and_tracked_wip_are_retained(self):
        root = self.area / 'empty transcripts'
        root.mkdir()
        manifest = {'schema_version': 1, 'coverage': 'complete', 'sources': [{'provider': 'claude', 'root': str(root), 'authorization': 'synthetic', 'coverage': 'complete'}]}
        (self.wt / 'scratch.txt').write_text('untracked')
        _, report = self.audit(manifest)
        self.assertEqual(report['worktrees'][1]['bucket'], 'review-scratch')
        (self.wt / 'README.md').write_text('tracked edit')
        _, report = self.audit(manifest)
        self.assertEqual(report['worktrees'][1]['bucket'], 'hold-wip')

    def test_cli_cursor_is_ignored_and_cannot_supply_supported_host_coverage(self):
        ignored = {'provider': 'cursor', 'files': ['/not-authorized/not-read.jsonl'], 'coverage': 'complete'}
        result, report = self.audit({'schema_version': 1, 'coverage': 'complete', 'sources': [ignored]})
        self.assertEqual(result.returncode, 2)
        self.assertEqual(report['sources'][0]['coverage'], 'ignored')
        self.assertEqual(report['sources'][0]['files_scanned'], 0)
        self.assertEqual(report['worktrees'][1]['bucket'], 'hold-activity-unavailable')
        root = self.area / 'empty supported history'
        root.mkdir()
        supported = {'provider': 'codex', 'root': str(root), 'authorization': 'synthetic', 'coverage': 'complete'}
        result, report = self.audit({'schema_version': 1, 'coverage': 'complete', 'sources': [ignored, supported]})
        self.assertEqual(result.returncode, 0)
        self.assertFalse(report['worktrees'][1]['evidence'])

    def test_cli_supported_host_contexts_and_nested_progress_hold(self):
        stamp = datetime.now(timezone.utc).isoformat()
        deep = self.area / 'tools/deep'
        relative_target = '../../' + self.wt.name + '/README.md'
        calls = [
            {'type': 'function_call', 'name': 'exec_command', 'arguments': json.dumps({'cmd': shlex.join(['cat', relative_target]), 'workdir': '../tools/deep'})},
            {'type': 'function_call', 'name': 'exec_command', 'arguments': json.dumps({'cmd': shlex.join(['git', '-C', str(deep), '-C', '../../' + self.wt.name, 'status']), 'workdir': str(self.consumer)})}]
        path = self.area / 'context.jsonl'
        for payload in calls:
            rows = [{'type': 'session_meta', 'timestamp': stamp, 'payload': {'cwd': str(self.consumer)}},
                    {'type': 'response_item', 'timestamp': stamp, 'payload': payload}]
            path.write_text('\n'.join(json.dumps(row) for row in rows) + '\n')
            result, report = self.audit({'schema_version': 1, 'coverage': 'complete', 'sources': [{'provider': 'codex', 'files': [str(path)], 'authorization': 'synthetic', 'coverage': 'complete'}]})
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(report['worktrees'][1]['bucket'], 'verify-recent-chat')
        nested = {'type': 'progress', 'timestamp': stamp, 'cwd': str(self.consumer), 'data': {'type': 'agent_progress', 'message': {'message': {'content': [{'type': 'tool_use', 'name': 'Bash', 'input': {'command': shlex.join(['cat', '../' + self.wt.name + '/README.md'])}}]}}}}
        path.write_text(json.dumps(nested) + '\n')
        result, report = self.audit({'schema_version': 1, 'coverage': 'complete', 'sources': [{'provider': 'claude', 'files': [str(path)], 'authorization': 'synthetic', 'coverage': 'complete'}]})
        self.assertEqual(result.returncode, 2)
        self.assertEqual(report['worktrees'][1]['bucket'], 'hold-activity-unavailable')

    def test_cli_malformed_native_messages_files_and_sed_hold(self):
        stamp = datetime.now(timezone.utc).isoformat()
        cases = [
            ('codex', [{'type': 'session_meta', 'timestamp': stamp, 'payload': {'cwd': str(self.consumer)}},
                       {'type': 'response_item', 'timestamp': stamp, 'payload': {'type': 'message', 'role': 'assistant', 'content': [{'type': 'unknown_operation', 'command': 'cat ../sibling/README.md'}]}}]),
            ('claude', [{'type': 'assistant', 'timestamp': stamp, 'cwd': str(self.consumer), 'message': {'content': [{'type': 'tool_use', 'name': 'Read', 'input': {'path': str(self.consumer)}}]}}]),
            ('codex', [{'type': 'response_item', 'timestamp': stamp, 'payload': {'type': 'function_call', 'name': 'exec_command', 'arguments': json.dumps({'cmd': shlex.join(['sed', '-n', '1r ../' + self.wt.name + '/README.md', 'README.md']), 'workdir': str(self.consumer)})}}])]
        path = self.area / 'invalid-native-inputs.jsonl'
        for provider, rows in cases:
            path.write_text('\n'.join(json.dumps(row) for row in rows) + '\n')
            result, report = self.audit({'schema_version': 1, 'coverage': 'complete', 'sources': [{'provider': provider, 'files': [str(path)], 'authorization': 'synthetic', 'coverage': 'complete'}]})
            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertEqual(report['coverage'], 'unavailable')
            self.assertEqual(report['worktrees'][1]['bucket'], 'hold-activity-unavailable')
