# PR 1 fix round 1: host validation

The 9 October 2026 fix round reruns the two host observations from the first
PR 1 round against the fixed-round worktree `feat/skill-list-budget`,
uncommitted working tree on parent `8fe9b2d`. No consumer app was edited or
executed. No installation, marketplace entry or global host/user
configuration was changed; both hosts loaded the plugin from a session-local
or project-local reference only. Raw logs and renders are private, kept
outside this repository; this receipt records their SHA-256 and per-cell
states, not their contents verbatim.

## Claude Code: skill count with and without huguesStack

Claude Code `2.1.293`. Two disposable non-interactive sessions ran from a
scratch directory outside the repository, each with a trivial one-line
prompt and `--debug` logging to a private file:

- Without huguesStack: no `--plugin-dir`. Ten other plugins were already
  enabled in this account (unrelated to huguesStack). Debug log:
  `getSkills returning: 65 skill dir commands, 20 plugin skills, 39 bundled
  skills, 1 builtin plugin skills`, then `Sending 63 skills via attachment
  (initial)`.
- With huguesStack: `--plugin-dir` pointed at the worktree's `plugin`
  directory for that session only. Debug log: plugin `hugues-stack` loads
  50 skills from its directory (`Loaded 50 skills from plugin hugues-stack
  default directory`), raising plugin skills loaded to 70 and
  `getSkills returning: 65 skill dir commands, 70 plugin skills, 39 bundled
  skills, 1 builtin plugin skills`, then `Sending 65 skills via attachment
  (initial)`.

**State: OBSERVED.** The delta is exactly **+2** (63 to 65), matching the two
model-invocable skills (`hugues-mode`, `setup-huguesstack`). All 50
huguesStack skill directories load as available for `/name` invocation, but
only those two reach the attached, model-visible list; the other 48
(`disable-model-invocation: true`) are loaded without being sent. This
directly observes Issue user stories 1, 2 and 28 against the current round's
bytes, not the first round's.

Not rerun in this round, carried over unverified from the first round's own
account: that a disabled principle still runs when typed by name, and that
the router's new description appears correctly in the model's own
paraphrase. Both remain plausible from the static wiring and the first
round's prior observation, but this round did not re-exercise them.

## Codex: prompt-input skills block

Codex CLI `0.161.0`. `codex debug prompt-input` renders the model-visible
prompt input locally; it issues no request to OpenAI and needed no approval
beyond the standing one for this task. It ran from a scratch project
directory outside the repository, with a project-local `.agents/skills`
reference to the worktree's `plugin/skills` directory (no global `~/.codex`
change, no marketplace install).

**State: OBSERVED.** The rendered `skills_instructions` block lists 85
available skills across every configured root. Exactly two are namespaced
`hugues-stack:`: `hugues-stack:hugues-mode` and
`hugues-stack:setup-huguesstack`, with their exact current descriptions.
None of the other 48 huguesStack skill names appear under any root, even
though all 50 directories are reachable from the linked path. This directly
observes that `disable-model-invocation: true` (mirrored to Codex as
`allow_implicit_invocation: false`) removes a skill's description from
Codex's rendered prompt input, not only from Claude's — answering Issue user
story 15's open question for the current round.

## Codex: one approved live exec rerun

One `codex exec` ran in the same scratch project, sandbox `read-only`,
`--skip-git-repo-check` (the scratch directory is not a Git repository), with
a trivial fixed-string prompt. This sends that prompt and the rendered skill
list to OpenAI on the owner's account; the owner approved exactly one such
rerun for this task.

**State: OBSERVED.** The session reported model `gpt-6.1-sol`, provider
`openai`, sandbox `read-only`, and returned the requested fixed string with
no other side effect, confirming the harness exercises the same skill-list
rendering seen in the static `prompt-input` check above under a real,
network-backed turn. 6,893 tokens were used. This is the one rerun the task
authorized; no further `codex exec` ran.

## Evidence

Each artifact below is private, kept outside this repository; only its
SHA-256 is recorded here.

| Artifact | SHA-256 |
|---|---|
| Claude Code debug log, without huguesStack | `870067ac00cb819b32c5822ea09cbecc9397ad25dd1c065b45e8a3e39a7e0e03` |
| Claude Code stdout, without huguesStack | `f22962e629a0f75b32518684c260001f0edf86c22c272c6a928d0f666d6601a2` |
| Claude Code debug log, with huguesStack | `222693f1254e2e7ef36ca1641a71196167d52f21ce99dda63478101acb896e6c` |
| Claude Code stdout, with huguesStack | `f22962e629a0f75b32518684c260001f0edf86c22c272c6a928d0f666d6601a2` |
| Codex `prompt-input` raw JSON | `d73e55ab50382bac420d8976cd3e73c2611e6aeed31f680f10fb17ccc56bd11d` |
| Codex `prompt-input` stderr (empty) | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| Extracted `skills_instructions` block | `3be6202b0f66ed5ae5775a0d4f1fcef9ce5f3244a66257a8a40bc4068ce8b6e7` |
| Codex `exec` session log | `45b2d6b05a99c741431e2872e90e21ebbf279eeda01ab5b5ce27798c4bb58324` |

## Gaps

Codex installation through its own plugin/marketplace mechanism (as opposed
to a project-local skills reference) remains unrun, as does a native Codex
`/name` invocation of a disabled huguesStack skill. Claude Code's disabled
skill re-invocation and self-reported description paraphrase are carried
over from the first round, not re-observed here. No mobile device, build or
simulator proof is implied by this receipt; it covers only the host
skill-list claim in the Issue's Problem Statement and user stories 1, 2, 14,
15 and 28.
