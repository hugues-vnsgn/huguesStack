"""Static retained-workflow contracts; these tests do not execute a host agent."""
import hashlib
import json
from pathlib import Path
import re
import unittest

from release_snapshot import release_root
ROOT = release_root()
ARCHITECT = 'plugin/skills/architect/SKILL.md'
ARENA = 'plugin/skills/arena/SKILL.md'
RECEIPT = 'docs/upstream/retained-design-provenance.json'


def phases(text):
    return re.findall(r'^## Phase ([A-F]): (.+)$', text, re.M)


def section(text, phase):
    match = re.search(r'^## Phase ' + phase + r': [^\n]*\n(.*?)(?=^## |\Z)', text, re.M | re.S)
    return match.group(1) if match else ''


def workflow_errors(architect, arena):
    """Enforce phase-local obligations so wording in Outputs cannot replace them."""
    errors = []
    expected = {
        'architect': [('A', 'Ground the problem'), ('B', 'Sketch'), ('C', 'Agree (opt-in)'),
                      ('D', 'Implement against the sketch'), ('E', 'Scrap when the architecture is wrong')],
        'arena': [('A', 'Frame'), ('B', 'Fan out'), ('C', 'Cross-judge'),
                  ('D', 'Pick a base'), ('E', 'Graft'), ('F', 'Verify')],
    }
    for name, text in [('architect', architect), ('arena', arena)]:
        if phases(text) != expected[name]:
            errors.append(name + ' phase order')
    obligations = [
        ('ground-how', section(architect, 'A'), ('[how](../how/SKILL.md)', 'traced model', 'every touched subsystem')),
        ('ground-why', section(architect, 'A'), ('[why](../why/SKILL.md)', 'ownership or layering')),
        ('ground-blocked', section(architect, 'A'), ('genuinely greenfield', 'mark Ground blocked', 'missing dependency')),
        ('two-shapes', section(architect, 'B'), ('at least two structurally distinct candidates', 'dropout or convergence does not waive this minimum')),
        ('red-flags', section(architect, 'B'), ('Screen every candidate', 'references/design-red-flags.md', 'interface depth')),
        ('checkpoint', section(architect, 'C'), ('Default: proceed directly', 'No human checkpoint', 'invoker explicitly asks', 'pause for sign-off', 'Re-ground and re-run Phase B')),
        ('fresh-implementation', section(architect, 'D'), ('coordinator briefs a fresh implementation worker', 'sketch is the contract', 'actual diff', 'affected mobile lanes')),
        ('scrap', section(architect, 'E'), ('pattern', 'Two or more independent Phase D deviations', 'Re-run [how]', 'Return to Phase B and re-run arena')),
        ('rubric-private', section(arena, 'A'), ('3-6 concrete gradeable criteria', 'Candidates only see the task', 'omit it from every candidate prompt')),
        ('isolated-paths', section(arena, 'A'), ('own authorized git worktree', 'absolute local task directory', 'separate synthesis path')),
        ('native-default', section(arena, 'A'), ('fresh same-host native agent', '`inherit-parent`', 'omit model and reasoning overrides', 'mark the seat blocked')),
        ('candidate-brief-isolation', section(arena, 'A'), ('sanitized candidate brief', 'coordinator conversation', 'rubric-bearing records', 'shared grounding')),
        ('candidate-context-isolation', section(arena, 'B'), ('fresh context containing only the sanitized candidate brief', "`fork_turns: 'none'`", 'omit model and reasoning overrides', 'Verify the actual spawn capability', 'Fan out blocked', 'cannot establish isolation')),
        ('fan-out', section(arena, 'B'), ('concurrently', 'same task', 'artifact and a short rationale', 'dropout', 'separate explicit authority')),
        ('blind-judge', section(arena, 'C'), ('After all Phase B candidate writers finish', 'fresh read-only native judge', 'neutral path labels', 'without runner identities or parent preference', 'in parallel', 'not with the candidates themselves', 'Cross-judge blocked')),
        ('judge-context-isolation', section(arena, 'C'), ('fresh context containing only the sanitized judge brief', "`fork_turns: 'none'`", 'omit model and reasoning overrides', 'coordinator conversation', 'Inspect the actual spawn capability', 'cannot establish isolation', 'never claim blind judging')),
        ('judge-report-scope', section(arena, 'C'), ('returns its report to the coordinator for private persistence', 'no writes', 'report-only exception', 'exact isolated report path', 'no consumer writes')),
        ('pick', section(arena, 'D'), ('Read every candidate end to end', 'criterion by criterion', 'resolve the disputed criteria against the actual artifacts', 'counting votes or averaging scores cannot replace judgment', 'cross-judge\'s verdict')),
        ('graft', section(arena, 'E'), ('Walk each losing candidate once more', 'Fold each graft in by hand', 'from which candidate', 'rejected and why')),
        ('graft-owner-scope', section(arena, 'E'), ('For a design package, the coordinator owns the design synthesis', 'For an executable consumer artifact', 'briefs a fresh scoped implementation worker', 'coordinator retains the design choices', 'Inspect the actual diff', 'before Phase F', 'no additional authority')),
        ('convergence-divergence', section(arena, 'E'), ('converge on the same shape', 'No graft is needed', 'wildly diverge', 'Reframe and re-run', 'Architect must first satisfy')),
        ('actual-verify', section(arena, 'F'), ('actual synthesized artifact', 'original task and rubric', 'caller usage with types and signatures', 'every affected target', 'candidate test result', 'actual artifact identity')),
        ('verify-return', section(arena, 'F'), ('Phase A was wrong (re-frame and re-run)', 'go back to Phase E', 'required proof is observed')),
    ]
    for label, content, required in obligations:
        if any(fragment not in content for fragment in required):
            errors.append(label)
    return errors


class RetainedDesignTests(unittest.TestCase):
    def setUp(self):
        self.architect = (ROOT / ARCHITECT).read_text()
        self.arena = (ROOT / ARENA).read_text()
        self.receipt = json.loads((ROOT / RECEIPT).read_text())

    def test_phase_local_contracts(self):
        self.assertEqual(workflow_errors(self.architect, self.arena), [])

    def test_mutations_cannot_drop_control_branches(self):
        mutations = [
            ('architect', '[how](../how/SKILL.md)', 'generic investigation', 'ground-how'),
            ('architect', '[why](../why/SKILL.md)', 'guess the rationale', 'ground-why'),
            ('architect', 'mark Ground blocked', 'continue to Sketch', 'ground-blocked'),
            ('architect', 'at least two structurally distinct candidates', 'one candidate', 'two-shapes'),
            ('architect', 'pause for sign-off', 'continue automatically', 'checkpoint'),
            ('architect', 'coordinator briefs a fresh implementation worker', 'reuse the candidate worker', 'fresh-implementation'),
            ('architect', 'Return to Phase B and re-run arena', 'patch the old sketch', 'scrap'),
            ('arena', 'omit it from every candidate prompt', 'send rubric to every candidate', 'rubric-private'),
            ('arena', 'sanitized candidate brief', 'full coordinator brief', 'candidate-brief-isolation'),
            ('arena', 'rubric-bearing records', 'ordinary records', 'candidate-brief-isolation'),
            ('arena', 'fresh context containing only the sanitized candidate brief', 'candidate inherits coordinator conversation', 'candidate-context-isolation'),
            ('arena', 'fresh context containing only the sanitized judge brief', 'judge inherits coordinator conversation', 'judge-context-isolation'),
            ('arena', "`fork_turns: 'none'`", "`fork_turns: 'all'`", 'candidate-context-isolation'),
            ('arena', "`fork_turns: 'none'`", "`fork_turns: 'all'`", 'judge-context-isolation'),
            ('arena', 'cannot establish isolation', 'claims isolation without checking', 'candidate-context-isolation'),
            ('arena', 'cannot establish isolation', 'claims isolation without checking', 'judge-context-isolation'),
            ('arena', 'returns its report to the coordinator for private persistence', 'writes into the consumer tree', 'judge-report-scope'),
            ('arena', 'report-only exception', 'unrestricted write access', 'judge-report-scope'),
            ('arena', 'After all Phase B candidate writers finish', 'While candidates are writing', 'blind-judge'),
            ('arena', 'without runner identities or parent preference', 'with model identities and parent preference', 'blind-judge'),
            ('arena', 'resolve the disputed criteria against the actual artifacts', 'average the scores', 'pick'),
            ('arena', 'Walk each losing candidate once more', 'skip losing candidates', 'graft'),
            ('arena', 'For a design package, the coordinator owns the design synthesis', 'worker picks the design', 'graft-owner-scope'),
            ('arena', 'briefs a fresh scoped implementation worker', 'edits executable consumer code directly', 'graft-owner-scope'),
            ('arena', 'Inspect the actual diff', 'trust the graft worker summary', 'graft-owner-scope'),
            ('arena', 'Reframe and re-run', 'average divergent shapes', 'convergence-divergence'),
            ('arena', 'actual synthesized artifact', 'ungrafted base', 'actual-verify'),
            ('arena', 'go back to Phase E', 'accept the known failure', 'verify-return'),
        ]
        for target, old, new, error in mutations:
            with self.subTest(error=error, target=target):
                values = {'architect': self.architect, 'arena': self.arena}
                self.assertIn(old, values[target])
                values[target] = values[target].replace(old, new)
                self.assertIn(error, workflow_errors(values['architect'], values['arena']))
        swapped = self.arena.replace('## Phase D: Pick a base', '## Phase Z: Pick a base')
        self.assertIn('arena phase order', workflow_errors(self.architect, swapped))

    def test_isolation_contracts_cannot_move_out_of_launch_phases(self):
        # A frame or Outputs disclaimer cannot guard a context-inheriting spawn.
        for phase, label in (('B', 'candidate-context-isolation'), ('C', 'judge-context-isolation')):
            with self.subTest(phase=phase):
                moved = self.arena.replace(section(self.arena, phase), '\n')
                moved += '\n' + section(self.arena, phase)
                self.assertIn(label, workflow_errors(self.architect, moved))

    def test_real_grounding_dependency_is_present(self):
        # Deliberately fails on an unstacked design checkout: no fake dependency fallback.
        for name in ('how', 'why'):
            dependency = ROOT / 'plugin/skills' / name / 'SKILL.md'
            with self.subTest(dependency=name):
                self.assertTrue(dependency.is_file(), f'Integrate research dependency: {dependency}')
                if dependency.is_file():
                    self.assertIn(f'name: {name}', dependency.read_text())

    def test_exact_source_and_destination_fingerprints(self):
        snapshot = json.loads((ROOT / 'docs/upstream/snapshots/pstack-0.15.9.json').read_text())
        inventory = {row['path']: row for row in snapshot['files']}
        self.assertEqual({k: self.receipt[k] for k in ('repository', 'revision', 'upstream_version', 'package')}, {
            'repository': 'https://github.com/cursor/plugins',
            'revision': 'e43c7ee26e0038c6c1fa8380dd34ce86ff94cb2a',
            'upstream_version': '0.15.9', 'package': 'design',
        })
        sources = {
            'pstack/skills/architect/SKILL.md', 'pstack/skills/arena/SKILL.md',
            'pstack/skills/architect/references/design-red-flags.md',
            'pstack/skills/architect/references/rationale-template.md',
            'pstack/skills/architect/references/runner-prompt.md',
        }
        self.assertEqual({row['source'] for row in self.receipt['files']}, sources)
        self.assertEqual(len(self.receipt['files']), 5)
        ledger = json.loads((ROOT / 'docs/upstream/huguesStack-dispositions.json').read_text())
        ledger = {row['path']: row for row in ledger['items']}
        for row in self.receipt['files']:
            with self.subTest(source=row['source']):
                for key in ('blob_sha', 'sha256', 'mode'):
                    self.assertEqual(row[key], inventory[row['source']][key])
                body = (ROOT / row['destination']).read_bytes()
                self.assertEqual(hashlib.sha256(body).hexdigest(), row['destination_sha256'])
                self.assertTrue(row['retained_contracts'])
                if row['disposition'] == 'verbatim':
                    self.assertEqual(hashlib.sha256(body).hexdigest(), row['sha256'])
                    self.assertEqual(hashlib.sha1(b'blob ' + str(len(body)).encode() + b'\0' + body).hexdigest(), row['blob_sha'])
                    self.assertEqual(row['deviations'], [])
                else:
                    self.assertTrue(row['deviations'])
                self.assertEqual(ledger[row['source']]['implementation_state'], 'present')
                self.assertEqual(ledger[row['source']]['destinations'], [row['destination']])
                self.assertEqual(ledger[row['source']]['disposition'],
                                 {'adapted': 'port with adaptation', 'verbatim': 'port verbatim'}[row['disposition']])

    def test_0159_agent_resistance_reference_and_usage_template(self):
        redflags = (ROOT / 'plugin/skills/architect/references/design-red-flags.md').read_text()
        self.assertEqual(re.findall(r'^## (.+)$', redflags, re.M), [
            'Shallow module', 'Information leakage', 'Temporal decomposition', 'Pass-through method',
            'Split ownership', 'Two ways to do one task', 'Importable internals', 'Hand-synced list',
        ])
        for behavior in ('one owner', 'delete them in the same change', 'fails the build', 'make the build fail'):
            self.assertIn(behavior, redflags)
        rationale = (ROOT / 'plugin/skills/architect/references/rationale-template.md').read_text()
        self.assertLess(rationale.index('## Usage'), rationale.index('## Shape'))
        self.assertIn('reconcile the sketch to the usage', rationale)
        self.assertIn('Judge each alternative on interface depth', rationale)

    def test_native_adapter_and_worker_scope(self):
        host_notes = '../hugues-mode/references/host-notes.md'
        self.assertIn(host_notes, self.arena)
        for required in ('absolute mode/skills paths', 'complete hugues-agent wrapper', 'actual native tool schema',
                         'actual diff', 'without recursive delegation', 'Candidate paths remain private',
                         'After all Phase B candidate writers finish'):
            self.assertIn(required, self.arena)
        runner = (ROOT / 'plugin/skills/architect/references/runner-prompt.md').read_text()
        self.assertIn('usage and two or three real call sites before the types', runner)
        self.assertIn('without recursive delegation', runner)
        self.assertIn('runners may inherit the same model', runner)
        self.assertNotIn('each on a different model', runner)
        for text in (self.architect, self.arena):
            for stale in ('pstack-models.mdc', 'run_in_background: true', 'grok-4.7', 'claude-opus-5-5-max'):
                self.assertNotIn(stale, text)


if __name__ == '__main__':
    unittest.main()
