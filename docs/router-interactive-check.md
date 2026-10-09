# Router interactive check

This receipt binds one interactive Claude Code session of the `hugues-mode`
router to one commit. The session ran on 9 October 2026 against `main` at
`0988b5622af1d2d5e99aa6422ed3a88caf2b873f` (tree
`c5b416cbb990ca007442f75f52951f03c20cbbd4`, `plugin/` tree
`9db3493b76940f9c341cf5466971cd3f74accd3c`), the merge of PR #25. The plugin
came from a detached checkout of that commit. Checked after the run, its
`git status --short` printed nothing.

The release commit that carries this receipt differs from the tested commit in
`plugin/` by the version in `plugin/.claude-plugin/plugin.json` (`0.3.0-rc.1`
became `0.3.0`) and by the sealed payload hashes that the version change moves:
`plugin/adapters/runtime/payload.json`, `plugin/adapters/runtime/payload.py` and
`plugin/adapters/host_tools.py`. No skill, playbook or adapter text differs.

Raw files stay private, outside this repository, because the transcript holds
the consumer app's source and instructions. This receipt records their SHA-256
and what was observed, not their contents. It is one session with one prompt. It
is an observation, not a rate.

The [router eval](hugues-mode-router-eval.md) ran print mode, where no run
copied a playbook step verbatim, and lists the router under an interactive
session as not run. This is that session, run once. The
[skill-list host validation](skill-list-host-validation.md) left Claude Code's
view of the router description unobserved. The session's first-turn skill list
shows it.

## Setup

- Claude Code `2.1.293` (every transcript record carries it). Model
  `claude-opus-5-5`; the assistant records carry effort `high`.
- The plugin loaded with `--plugin-dir` from a detached checkout of `main` at
  `0988b56`, under `huguesStack.worktrees/_router-check`. The transcript's skill
  base directory names `_router-check/plugin/skills/hugues-mode`. The manifest
  there still read `0.3.0-rc.1`.
- Hooks were disabled with `--settings '{"disableAllHooks":true}'`. This is the
  launcher's record: no script or log preserves the command line. The
  transcript holds no hook record.
- The session ran in a disposable copy of the consumer app `cmp-test`, at
  `/tmp/cmp-test-routercheck`, with its git remotes removed (the remote removal
  is the launcher's record). The transcript's working directory is the copy, or
  a folder inside it, on every record that carries one, and no command in it
  names the real app's path. Edits stayed in the copy.
- The prompt was the small-Kotlin-feature prompt from Issue #22's eval, byte for
  byte as in the router eval's task 3: "I'd like a small feature: the tab chips
  on the request list should show how many requests each tab holds, like
  "Pending (3)". Please put the counting in the shared Kotlin logic and wire it
  into the chips." No skill name or slash command was typed.
- The session was launched with `--permission-mode default` but ran in auto mode.
  The transcript holds eight permission-mode records, in this order: `default`
  three times, `acceptEdits` once (05:19:30Z) and `auto` four times (from
  05:19:42Z, where it also holds a plan-mode-exit marker and an auto-mode
  marker). The transcript does not say what changed the mode.
- The transcript's records run from 2026-10-09T05:18:59Z to 05:21:00Z. It holds
  12 Bash calls, 3 Agent calls and 1 Skill call. It holds no TodoWrite call.

## What the session did

**State: OBSERVED**, for each line below.

1. **The router fired, unprompted.** The first tool call, about three seconds
   after the prompt, was `Skill` with `hugues-stack:hugues-mode` and the task
   restated as its argument. The owner's own user-level skills, including `cook` and
   `tdd-kmp`, were in the same skill list. The eval saw those fire in other
   cells; here the router won. One session shows that it can, not how often.
2. **Claude Code's skill list held two huguesStack entries, whole.** The
   first-turn skill listing has 66 entries. Exactly two come from huguesStack:
   `hugues-stack:hugues-mode` with its 236-character description and
   `hugues-stack:setup-huguesstack` with its 130-character description. Both
   equal the declared descriptions, so the two descriptions in the list total
   366 characters. No other entry carries the `hugues-stack:`
   prefix, so the other 48 bundled skills have no entry. This observes in Claude
   Code what the skill-list receipt observed for Codex. It also turns that receipt's
   count-based inference for Claude Code into a read of the names.
3. **The router read its references as files.** It used `cat` through Bash on
   `adapters/host.md`, `adapters/mobile.md` and `adapters/mobile-workflows.md`,
   on the Feature, `cmp-two-target-change` and `kmp-bridge-change` playbooks,
   and on the bundled skills `how`, `architect`, `arena` and four principles
   (`principle-model-the-domain`, `principle-laziness-protocol`,
   `principle-test-behavior-not-implementation`, `principle-prove-it-works`).
   Two Bash calls exited 1 when the shell rejected an `echo` separator after
   the first file printed; the session repeated the reads it had missed. The
   `Skill` call was the only native invocation of a skill.
4. **It followed the consumer project's task-tracking rule.** The consumer's
   `CLAUDE.md` says to use `bd` for all task tracking and not to use TodoWrite.
   The session called `bd create`, then wrote the playbook steps with `bd note`,
   and never called TodoWrite. The bead note lists the Feature playbook's eight
   steps in the playbook's order, plus `cmp-two-target-change`, with a
   reason beside each step it skipped, folded into another or made conditional
   (`how`, `architect`, the commit step, `interrogate` and the PR step), and the
   throughput checkpoint's four dimensions on one line. The steps are
   abbreviated, not word for word. The router eval's steps-copied signal scored
   0 on every print-mode run, which has no todo tool; here all eight steps
   appear, in order.
5. **It spawned three arena candidates.** Three `Agent` calls named
   `subagent_type` `hugues-stack:hugues-agent`, each for one worktree under the
   copy, and each returned an "Async agent launched" result. The lead then
   recorded the arena rubric on the bead.

The transcript ends with `pendingBackgroundAgentCount: 3` at 05:21:00Z.

## Not observed

- **No candidate finished and no implementation outcome exists.** The arena run
  was stopped before its candidates returned. No judge ran, and nothing was
  verified, committed or merged. This check says nothing about whether the
  router's feature path produces a correct change.
- **The bug-fix prompt's session never started.** It stayed at Claude Code's
  folder-trust prompt, so this check covers only the feature prompt.
- **Which router instructions caused which behavior.** The transcript shows what
  the session did, not why. The bead note's step list follows the playbook, and
  the consumer's rule is in the same context. This receipt does not separate the
  two.
- Codex, the marketplace install route, a principle typed by name and a live
  Codex model turn remain exactly as the
  [skill-list receipt](skill-list-host-validation.md#gaps) records them. This
  session loaded the plugin for one session with `--plugin-dir` and installed
  nothing.
- No mobile build, device or simulator ran.

## Harness lesson

An earlier attempt ran two interactive sessions in the real `cmp-test`, in plan
mode. Plan mode replaced routing, so neither session fired the router. One
session's plan was approved into auto mode and changed the real app. Those
changes were removed at the owner's request. This is the launcher's record; no
artifact in the hash list below backs it. Run interactive checks in a disposable
copy of the consumer app, as this session did.

## Artifacts

Private, in `huguesStack.worktrees/_evidence/router-check/`. `SHA256SUMS` there
holds these four hashes, and `shasum -a 256 -c SHA256SUMS` passed on 9 October
2026 before this receipt was written.

| Artifact | SHA-256 |
|---|---|
| `interactive-feature.transcript.jsonl` (the session, 125 records) | `7b53bd12904158bdb53c4422388c78b41e6ba8c1cb05ce78b132a35093f89fc2` |
| `interactive-feature.bead-note.txt` (the bead's text with its notes) | `c0cc3fa32b254ea70764a7db91abffbf236df4622485f5eadaf6687aaad620b2` |
| `tab-chip-counts.patch` (kept with the run; no claim above rests on it) | `85de38dfa43ffb7381599c7891d6cc0ee5d16623b8587a765a33a558f50fe7c6` |
| `cmp-test-kip.bead.txt` (kept with the run; no claim above rests on it) | `05044678157d72d996aa058d0a51f68f59790e0961aeeb57436325368b0251ce` |
