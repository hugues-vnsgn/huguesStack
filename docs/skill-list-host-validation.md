# Skill-list host validation

Renamed from `pr1-fix-round-1-validation.md`: this receipt now carries a
content name instead of a round number, and binds to a commit instead of
describing "the fixed-round worktree" generically. The 9 October 2026 fix
round 2 reruns the Issue #21 host observations against this round's code
commit `6a6f31d8e1e4d958811f99dbef7a0b9123b03b76`, tree
`a744531b78d58b12f35bef5ee64bfc4ad634f028`, on branch `feat/skill-list-budget`.
No consumer app was edited or executed. No installation, marketplace entry or
global host/user configuration was changed; both hosts loaded the plugin from
a session-local or project-local reference only. Raw logs and renders are
private, kept outside this repository; this receipt records their SHA-256 and
per-cell states, not their contents verbatim.

## Claude Code: skill count with and without huguesStack

Claude Code `2.1.293`, model `claude-sonnet-5-5`. Two disposable non-interactive sessions ran from a
scratch directory outside the repository, each with a trivial one-line
prompt and `--debug-file` logging to a private file:

- Without huguesStack: no `--plugin-dir`. Debug log: `getSkills returning: 65
  skill dir commands, 20 plugin skills, 39 bundled skills, 1 builtin plugin
  skills`, then `Sending 63 skills via attachment (initial)`.
- With huguesStack: `--plugin-dir` pointed at this round's worktree `plugin`
  directory for that session only. Debug log: plugin `hugues-stack` loads 50
  skills from its directory (`Loaded 50 skills from plugin hugues-stack
  default directory`), raising plugin skills loaded to 70 and `getSkills
  returning: 65 skill dir commands, 70 plugin skills, 39 bundled skills, 1
  builtin plugin skills`, then `Sending 65 skills via attachment (initial)`.

**State: OBSERVED.** The delta is exactly **+2** (63 to 65), matching the two
model-invocable skills (`hugues-mode`, `setup-huguesstack`). All 50
huguesStack skill directories load as available for `/name` invocation, but
only those two reach the attached, model-visible list; the other 48
(`disable-model-invocation: true`) are loaded without being sent. This
repeats the first round's observation on the same wiring -- this fix round
changed how a user-only skill's body is reached (guard ordering, allowed
set), not the model-invocable tiering itself -- against this round's bytes.
Directly observes Issue user stories 1, 2 and 28 (the list-size half).

## Claude Code: typed invocation of a user-only skill

The same loaded session (`--plugin-dir`, no other config change) ran a second
disposable turn with the prompt `/hugues-stack:tdd Say in one sentence what
this skill instructed, citing one exact phrase from its SKILL.md. Do not
write or run anything else.`

**State: OBSERVED.** The reply quoted "Write the failing test first" and
described skipping a new test "when one would be impractical" -- both exact
phrases from the installed `plugin/skills/tdd/SKILL.md` at this round's
commit, confirmed by a direct `grep` of that file. `tdd` is user-only
(`disable-model-invocation: true`) and absent from the attached skill list
observed above; this directly observes that typing a user-only skill by name
still runs it, closing the gap the first round's receipt carried over
unverified ("Not rerun in this round, carried over unverified from the first
round's own account: that a disabled principle still runs when typed by
name"). Directly observes Issue user stories 2, 3 and 28 (the typed-
invocation half).

Not rerun this round: the router's new description surfacing in its own
self-reported paraphrase. It remains attributed to the first round's own
observation and bytes, not reasserted as current evidence.

## Codex: prompt-input skills block

Codex CLI `0.161.0`. `codex debug prompt-input` renders the model-visible
prompt input locally; it issues no request to OpenAI and needed no approval
beyond the standing one for this task. It ran from a scratch project
directory outside the repository, with a project-local `.agents/skills`
reference to this round's worktree `plugin/skills` directory (no global
`~/.codex` change, no marketplace install).

**State: OBSERVED.** The rendered `skills_instructions` block lists 85
available skills across 8 configured skill roots. Exactly two are namespaced
`hugues-stack:`: `hugues-stack:hugues-mode` and
`hugues-stack:setup-huguesstack`, with their exact current descriptions.
None of the other 48 huguesStack skill names appear under the worktree's
skill root, even though all 50 directories are reachable from the linked
path. This directly observes that `disable-model-invocation: true` (mirrored
to Codex as `allow_implicit_invocation: false`) removes a skill's description
from Codex's rendered prompt input, not only from Claude's -- repeating the
first round's answer to Issue user story 15's open question against this
round's bytes.

## Codex: no live exec this round

This round's task authority explicitly withholds `codex exec` approval ("no
`codex exec` this round"). The first round's single approved live-exec
corroboration (`gpt-6.1-sol`, sandbox `read-only`, 6,893 tokens) is not rerun
and is not reasserted as current evidence; it remains attributed to the
first round's own bytes only.

## Evidence

Each artifact below is private, kept outside this repository; only its
SHA-256 is recorded here.

| Artifact | SHA-256 |
|---|---|
| Claude Code debug log, without huguesStack | `e46708b46bc0556b48a7113d5c73159ed833b989c7fbce208202ca7393662517` |
| Claude Code stdout, without huguesStack | `e12c759830c2d48901ac4a4d7729fc218d96f1eb8f4a418a0634f732ad6492f0` |
| Claude Code debug log, with huguesStack | `8665643d5e7142d3041068e8e8ac54bf8360abda4c3ab913924f799bd8063426` |
| Claude Code stdout, with huguesStack | `bf122265acaece545b367a2301763ad16c7a053b670ea825f55f5dae62391cfb` |
| Claude Code debug log, by-name `tdd` invocation | `d121874639a44e4144e510fa0f180afdd9e20878ba5549a7edfd4cbdf5676966` |
| Claude Code stdout, by-name `tdd` invocation | `27c6329c318587284c87944ec95b3655dd48ce2f598a86b512834aa8509d5a8c` |
| Codex `prompt-input` raw JSON | `fb8cad642ee56f546e69a835a01959a2acf6e07b6e2916de39cde9cd7187551c` |
| Codex `prompt-input` stderr (empty) | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| Extracted `skills_instructions` block | `e4b5598a93758d0363671d3358c933e4a85c9d53d371aa041d4102b7c95eb5e4` |

## Gaps

Codex installation through its own plugin/marketplace mechanism (as opposed
to a project-local skills reference) remains unrun, as does a native Codex
`/name` invocation of a disabled huguesStack skill (Claude Code's own
by-name invocation is observed above; Codex's is not). The first round's one
approved live `codex exec` corroboration is not rerun this round and is not
reasserted as current evidence. No mobile device, build or simulator proof is
implied by this receipt; it covers only the host skill-list and typed-
invocation claims in the Issue's Problem Statement and user stories 1, 2, 3,
14, 15 and 28.
