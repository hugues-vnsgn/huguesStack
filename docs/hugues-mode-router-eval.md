# Hugues mode router eval

This receipt binds the Issue #22 routing eval to one commit. The rewritten
router was tested at code commit `8b7127a638cb25065f8ed21b01e28c93e06f9ee9`
(fix round 1), tree `d4e7d4ee02fc6ffd1dfd25e95f1519bac5e44ade`, branch
`feat/hugues-mode-router`, stacked on `feat/skill-list-budget` at `e563e25`. It
was compared with `main` at `a67df901162cc2add4aabb9e2a3843134696c490`. Both
revisions printed nothing for `git status --short` at the start of the run (the
script below prints it first). The commit that carries this receipt changes
documentation only; `git diff 8b7127a HEAD -- plugin scripts tests` is empty. It
replaces the first receipt, commit `f9368f8`, which tested code commit `3d39448`
and is summarized under First attempt.

Twenty cells ran, one run each, and every run exited 0. None was repeated or
aborted. Four more runs were harness probes, not cells, and are listed under
Checks. Raw streams stay private, outside this repository; this receipt records
their SHA-256 and the per-cell states, not their contents. Nothing in the
consumer app `cmp-test` changed (see below). No host configuration file was
edited and nothing was installed: Claude Code loaded each revision with
`--plugin-dir` for one session at a time and wrote no session transcript
(`--no-session-persistence`). Claude Code's own routine state writes are not
audited here.

## Verdict

**Part A, firing: the router fired on the branch for 3 of the 4 task prompts
and on `main` for 0 of 4.** The positive control fired its target skill on both
revisions, so print mode does not stop skills from firing under Opus 5.5 at high
effort. The casual question stayed quiet on both. The one branch miss, task 1,
went to the owner's `tdd-kmp` skill instead of the router. Whether the first
attempt's zero came from Sonnet 5.5, from the old 312-character description or
from chance is not separated: that run had no control and used another model.

**Part B, routing after a typed `/hugues-stack:hugues-mode`: the branch met the
pre-registered pass condition in 4 of 4 cells, and the margin is thin.** No
signal was lower on the branch than on `main`. The branch was higher on the
route signal (task 3: it selected `cmp-two-target-change`, `main` did not) and on
principles read and named (tasks 1, 3 and 4). The steps-copied signal scored 0 of
the playbook's steps on all eight runs, so it separated nothing. Print mode has no
todo tool and no run copied a playbook step verbatim. A post-hoc read of the
replies, which is not a pre-registered signal, found that `main` enumerated the
playbook's steps in paraphrase and in order in task 3 (six numbered items covering
all eight steps) and task 4 (nine steps), and that the branch enumerated them in no
task. With paraphrase accepted, the branch is lower than `main` on that one signal
in two of four cells. I record the pass condition as met by the rule that was fixed
before the runs, and I flag the paraphrase reading for the owner.

**What this eval does not separate.** The branch carries both PR 1 and PR 2, and
no run used PR 1 alone. Part A's gap reflects the branch's router description
(PR 1's broader trigger, which PR 2's fix round 1 reordered into 236 characters
with the mobile clause first) together with PR 1's smaller skill list. Part B's
differences mix PR 1's tiering (principles and `how` are file reads on the branch
and Skill calls on `main`) with PR 2's body. Each cell is one sample, so a 3 of 4
against 0 of 4 gap is an observation and not a rate.

## First attempt

Commit `f9368f8` ran the Issue's five tasks once on each revision with
`claude-sonnet-5-5` in print mode, against code commit `3d39448` (the router
description was then 312 characters). The model invoked no skill of any kind in
any of the ten runs. Tasks 1 to 4 failed on both revisions because the router
never fired, task 5 stayed quiet, and the branch tied `main` in all five cells
without evidence that the rewrite helps. The finding was zero Skill use under
Sonnet 5.5 print mode. That run could not tell a router that does not fire from a
print mode that does not use skills, and it mixed two questions: whether the
router fires, which depends on PR 1's description, and whether it routes well once
running, which depends on PR 2's body. This eval answers them separately, adds a
positive control, and uses `claude-opus-5-5` at high effort. The first receipt's
script, artifact hashes and harness checks stay in git history at `f9368f8`. None
of its artifacts is reused here.

## Commands

Claude Code `2.1.293`, model `claude-opus-5-5` (the stream's init event names
both, and `--model` pinned it for every run). The huguesStack plugin reports
version `0.3.0-rc.1` on both revisions. **Effort was set to high with
`--effort high` on every run.** The init event does not echo an effort level (it
carries `per_turn_effort_active: true` and the model name), so the level is
recorded from the flag and not observed in the stream. The owner's user-level
settings carry `effortLevel: medium` for this model; the flag is what overrides
it for the session, and whether the override took effect is not independently
observed.

`<root>` stands for the machine-specific folder that holds `huguesStack.worktrees`
and `cmp-test`. The `main` revision ran from a throwaway detached worktree
`huguesStack.worktrees/_eval-main` at `a67df90`, created with `git worktree add
--detach` and removed with `git worktree remove` after scoring. Both revisions
loaded the same ambient setup: the owner's user-level plugins, skills and MCP
servers stayed enabled, and the init event lists 143 skills in every run. The
script was saved as `run-eval.sh` in the evidence folder. Part A and Part B ran
as two concurrent jobs, each a sequential loop, started with
`sh ./run-eval.sh <root> A > run-eval-A.out.txt 2>&1` and
`sh ./run-eval.sh <root> B > run-eval-B.out.txt 2>&1` (both exit 0). The twenty
cells started at 2026-10-09T02:43:03Z and the last one finished at 02:48:41Z.
`cmp-manifest.sh` took the before and after snapshots of `cmp-test`. The six
prompts are in `prompts.json`, and `score.py` is printed after the scripts. The
prompts, `run-eval.sh` and the first version of `score.py` were written before
the first cell and have not changed since, except for the one scorer edit
described under Scoring.

```sh
#!/bin/sh
# Usage: sh run-eval.sh <root> <part> [id ...]
#   <root>  folder that holds huguesStack.worktrees and cmp-test's parent
#   <part>  A (natural prompts, --max-turns 10) or B (typed /hugues-stack:hugues-mode, --max-turns 25)
# Each id runs once on main (a67df90) and once on the branch code commit (8b7127a).
set -u
ROOT="$1"; PART="$2"; shift 2
E="$ROOT/huguesStack.worktrees/_evidence/hugues-mode-router/eval-2"
MAIN="$ROOT/huguesStack.worktrees/_eval-main"
BRANCH="$ROOT/huguesStack.worktrees/feat/hugues-mode-router"
CMP="$ROOT/cmp-test"
SCRATCH="$E/scratch"
case "$PART" in A) TURNS=10; PREFIX="";; B) TURNS=25; PREFIX="/hugues-stack:hugues-mode ";; *) echo "bad part"; exit 2;; esac
if [ "$#" -eq 0 ]; then
  if [ "$PART" = A ]; then set -- t1 t2 t3 t4 t5 c1; else set -- t1 t2 t3 t4; fi
fi

git -C "$MAIN" rev-parse HEAD
git -C "$MAIN" status --short
git -C "$BRANCH" rev-parse HEAD
git -C "$BRANCH" status --short
claude --version

run() { # id rev plugin_root
  id="$1"; rev="$2"; plugin="$3"
  cwd=$(python3 -I -c "import json,sys; r=[x for x in json.load(open(sys.argv[1])) if x['id']==sys.argv[2]][0]; print(r['cwd'])" "$E/prompts.json" "$id")
  prompt=$(python3 -I -c "import json,sys; r=[x for x in json.load(open(sys.argv[1])) if x['id']==sys.argv[2]][0]; print(r['prompt'])" "$E/prompts.json" "$id")
  case "$cwd" in cmp-test) dir="$CMP";; *) dir="$SCRATCH";; esac
  out="$E/runs/$PART-$id-$rev"
  date -u +%Y-%m-%dT%H:%M:%SZ > "$out.started"
  (cd "$dir" && claude -p "$PREFIX$prompt" \
    --model claude-opus-5-5 --effort high --no-session-persistence \
    --plugin-dir "$plugin" \
    --settings '{"disableAllHooks": true}' \
    --tools "Read,Glob,Grep,Skill" --allowedTools Read Glob Grep Skill \
    --disallowedTools Edit Write MultiEdit NotebookEdit Bash Task Agent \
    --permission-mode dontAsk --max-turns "$TURNS" \
    --output-format stream-json --verbose \
    < /dev/null > "$out.stream.jsonl" 2> "$out.stderr.txt"); echo "$PART $id $rev exit $?" | tee -a "$E/runs/exit-codes.txt"
  date -u +%Y-%m-%dT%H:%M:%SZ > "$out.finished"
}

for id in "$@"; do
  run "$id" main "$MAIN/plugin"
  run "$id" branch "$BRANCH/plugin"
done
echo "script done"
```

The `CMP` path in `cmp-manifest.sh` names the real folder; the copy below shows
it as `<root>/cmp-test`.

```sh
#!/bin/sh
# Usage: sh cmp-manifest.sh <label> <outdir>
# Records git status plus a SHA-256 manifest and a modification-time listing of cmp-test, read-only.
set -u
CMP=<root>/cmp-test
label="$1"; out="$2"
cd "$CMP" || exit 1
find . -type f ! -path './.git/index' -print0 | LC_ALL=C sort -z | xargs -0 shasum -a 256 > "$out/cmp-test-$label.manifest.txt"
find . -type f ! -path './.git/index' -print0 | LC_ALL=C sort -z | xargs -0 stat -f '%m %N' > "$out/cmp-test-$label.mtimes.txt"
{ date -u +%Y-%m-%dT%H:%M:%SZ; echo "HEAD $(git rev-parse HEAD)"; echo "branch $(git branch --show-current)"; echo "--- git status --short --untracked-files=all"; git status --short --untracked-files=all; echo "(exit $?)"; } > "$out/cmp-test-$label.status.txt"
```

## Prompts

Each prompt ran once per revision, unchanged, with no instruction to stop after
routing. Tasks 1, 2, 3 and 5 and the control ran with `cmp-test` as the working
directory. Task 4 ran in an empty scratch folder, because it asks about a
huguesStack PR and `cmp-test` is a different repository. Part B used the same
text for tasks 1 to 4, preceded by `/hugues-stack:hugues-mode ` and followed by
nothing else.

| Prompt | Text |
|---|---|
| 1, bug fix | A negative settlement amount like -123456 shows up on the request card as "-,123,456" with a stray comma. Can you fix it? |
| 2, how does X work | How does the request list decide which settlement requests to show under each tab? |
| 3, small Kotlin feature | I'd like a small feature: the tab chips on the request list should show how many requests each tab holds, like "Pending (3)". Please put the counting in the shared Kotlin logic and wire it into the chips. |
| 4, check on PR N | Check on PR 20 in hugues-vnsgn/huguesStack. |
| 5, casual question | Quick question before I forget: for a top-level string constant in Kotlin, is it better to use val or const val? |
| C1, positive control | Debug this: on the request card, a settlement amount of -123456 renders as "-,123,456". Diagnose why. |

The task 1 bug is real: `formatAmountMinor(-123456)` returns `-,123,456`, which
was checked by hand against the source in the first attempt, not by running
Kotlin. The control reuses that bug on purpose and changes only the wording to
the trigger words of the owner's `diagnosing-bugs` skill, whose description says
"Use when the user says 'diagnose'/'debug this'". Task 1 and the control then
differ in phrasing alone. PR 20 is a merged huguesStack PR.

## Harness choices and what they cost

These apply to both revisions equally.

- **Read-only.** `--tools "Read,Glob,Grep,Skill"`, `--allowedTools` with the same
  four, `--disallowedTools` for the edit, write, shell and agent tools, and
  `--permission-mode dontAsk` so that anything not allowed is denied. The init
  event lists exactly those four built-in tools in all twenty streams. The model
  said in many replies that it had no edit, shell or agent tool and gave the
  patch as text.
- **Denied connector calls.** In task 4 the model tried a Gmail search through
  the owner's connected Gmail connector in four runs (Part A and Part B, both
  revisions), and a search of the agentmemory store in one (Part A, `main`). Every
  such call was denied and returned nothing (the result event lists each under
  `permission_denials`), so nothing was read or written there. The connectors
  stay visible to the model because the ambient setup stays enabled.
- **Hooks off.** `--settings '{"disableAllHooks": true}'` suppressed every hook;
  all twenty streams carry zero hook events. Two things force this. The consumer
  project's own `SessionStart` hook runs `bd prime --hook-json`, which rewrote
  three embedded Dolt files in a throwaway copy of `cmp-test` in the first
  attempt, so it cannot run in `cmp-test` without touching it. And the ambient
  agentmemory plugin has hooks on prompts and tool uses that would record these
  synthetic sessions in the owner's memory store. The cost is that the start of
  session context those hooks add is absent in every run, and its effect on
  whether the router fires is unobserved. Project settings and the project's
  `CLAUDE.md` stayed in effect, and skills, plugins and connectors stayed enabled.
- **Ambient memory stays in context.** The owner's saved notes for `cmp-test`
  remain available. Three runs read one memory file about the settlement UI
  (`project_settlement_sharedui_android_only.md`): Part A task 3 on both
  revisions, and Part B task 3 on `main`. Part B task 1 cited saved notes on both
  revisions. The notes are the same for both revisions.
- **Print mode has no todo tool.** The built-in tool list holds no `TodoWrite` or
  `TaskCreate`, and the project's `CLAUDE.md` forbids both. A todo list can appear
  only in the reply text, so `score.py` reads steps from the reply, and the
  steps-copied signal is structurally weak here.
- **Turn cap.** `--max-turns 10` in Part A and `--max-turns 25` in Part B. No run
  ended in an error: all twenty results are `success` with `terminal_reason`
  `completed`. The result event's `num_turns` counts more than assistant messages
  (it reached 18 in Part A), so it is not compared with the cap. Counted from the
  stream, assistant messages per run were at most 10 in Part A (task 4 on the
  branch used all ten) and at most 9 in Part B.
- **Task 4 and shell access.** With no shell and no GitHub tool, the model
  could not reach the PR on either revision. The read-only restriction may have
  limited what task 4 can show. Nothing was changed to work around it.
- **Concurrency.** Part A and Part B ran at the same time. Each used its own
  output files, so no artifact is shared, and no run shared a session.

## Checks run before the cells

Four runs that are not cells, all from the scratch folder with prompts that are
not task prompts. They only checked the harness. Their hashes are in the evidence
table.

- A one-word reply probe on the branch (`--max-turns 2`): it confirmed that the
  stream names `claude-opus-5-5` and that `--effort high` is accepted (exit 0).
  The init event holds no effort field.
- A typed-invocation probe on the branch, `/hugues-stack:hugues-mode` followed by
  a request to reply "ready". The stream does not replay the user message, so it
  could not show the expansion.
- Two typed-invocation probes, one per revision, that asked the model to quote the
  first heading of the skill text it was handed. On `main` it quoted `## Host
  invocation contract` and then `# Poteto mode`. On the branch it quoted `# Hugues
  mode`, with `## Non-negotiables` as the second section. So the typed command
  expands each revision's own router body.
- The first attempt's other two checks were not repeated, and the twenty streams
  are consistent with them. Plugin files outside the working directory were read
  under `dontAsk` with no `--add-dir`. Replies cite the project's `bd` workflow,
  so its `CLAUDE.md` stayed in effect with hooks off. The streams also confirm the
  tool list and the zero hook events.

## Scoring

The rules are in the docstring of `score.py`, printed below, and were fixed
before the first cell ran. In short:

- **Part A.** Per run, the skills invoked and whether `hugues-mode` fired (a
  Skill call named `hugues-stack:hugues-mode`). Tasks 1 to 4 are PASS when it
  fired and FAIL when it did not. Task 5 is PASS when it did not fire and no
  playbook was read. The control is PASS when `diagnosing-bugs` was invoked.
- **Part B.** Per run, whether the expected playbook was read (bug-fix,
  investigation, feature, babysit), steps found in the reply (first 60
  characters, markup removed) and how many came in order, distinct principle
  files read and distinct principles named in the reply, plus one signal per
  task: `how` reached (task 2), the `cmp-two-target-change` route read or named
  (task 3), a `check` mode declared (task 4). The route for task 3 was chosen
  before the runs from `mobile-workflows.md`: the chips are CMP rendering, and the
  adapter says CMP rendering implementation adds `cmp-two-target-change`.
  PASS needs the playbook plus the task signal (and, for task 1, every step in
  order and a principle read and named). PARTIAL is the playbook read without
  that. FAIL is no playbook read.
- **The pass condition.** The branch matches or beats `main` in a task only if
  its state is at least as high and every listed signal is at least as high.

After the cells ran, one scorer edit was made, and `score.v1.py` keeps the
original. The v1 matcher counted a principle as named only when its title
appeared without punctuation, so it scored "Test Behavior, Not Implementation"
as unnamed. Version 2 ignores punctuation and also records the number of numbered
list items in each reply. No state and no comparison changed: Part A output is
byte-identical, and in Part B only the named counts moved (task 1 branch from 2
to 3, task 3 branch from 2 to 3). Both outputs are in the evidence table.

## Part A: does the router fire

Skills invoked, from the Skill tool calls in each stream. `fired` means the
router, `hugues-stack:hugues-mode`.

| Prompt | `main` skills | `main` fired | Branch skills | Branch fired | `main` / branch state |
|---|---|---|---|---|---|
| 1, bug fix | none | no | `tdd-kmp` | no | FAIL / FAIL |
| 2, how does X work | none | no | `hugues-stack:hugues-mode` | yes | FAIL / PASS |
| 3, small Kotlin feature | `cook` | no | `hugues-stack:hugues-mode` | yes | FAIL / PASS |
| 4, check on PR N | none | no | `hugues-stack:hugues-mode` | yes | FAIL / PASS |
| 5, casual question | none | no | none | no | PASS / PASS |
| C1, positive control | `diagnosing-bugs` | no | `diagnosing-bugs` | no | PASS / PASS |

What each run did, from its stream:

- **Task 1.** `main` grepped and read `AmountFormat.kt` and its test, then
  answered. The branch did the same, then invoked `tdd-kmp` and answered. Neither
  invoked the router or read a playbook. The branch's `tdd-kmp` call turned the
  request into a test-first brief. The stream does not say why it chose that
  skill; its description names a regression test before a bug fix, which is an
  inference.
- **Task 2.** `main` grepped and read three source files, then answered. The
  branch invoked the router first, read `investigation.md`, then read four source
  files.
- **Task 3.** `main` read the chip code and a memory file, then invoked the
  owner's `cook` skill and answered. The branch invoked the router, read
  `host.md`, `mobile.md`, `feature.md` and `mobile-workflows.md`, read a principle
  and `cmp-two-target-change.md`, and answered.
- **Task 4.** `main` tried a Gmail search and an agentmemory search, both
  denied, and answered. The branch invoked the router, read `babysit.md` and
  two adapters, tried the denied Gmail search, looked for the `watch-pr` script,
  and answered.
- **Task 5.** Neither revision invoked a skill or read a playbook. Both answered
  in one turn.
- **Control.** Both revisions invoked `diagnosing-bugs` first and then read
  `AmountFormat.kt`. Neither fired the router, and the scorer records that
  without scoring it.

**Interpretation.** The control fired on both revisions, so the Skill tool works
in print mode with the owner's ambient setup, and a prompt that uses a skill's
own trigger words fires it. Print mode is therefore not the confound, and the
conditional pseudo-terminal run was not needed and was not made. The natural task
prompts split by revision. `main` fired the router for none of them, and the
branch fired it for three of four, with the only miss going to a more specific
personal skill. The branch differs from `main` in two things the model sees
before it fires: the router description (PR 1's broader trigger, reordered by
PR 2's fix round 1 into 236 characters with the mobile clause first) and the size
of the skill list (the first attempt's probe, on Sonnet 5.5, showed 46
`hugues-stack` skills listed on `main` against 2 on the branch; that probe was not
repeated here). This fits the broader description doing its job. It does not
isolate the description from the list change, and `main` also reached for a
personal skill (`cook`) on task 3. The casual question stayed quiet on both. The
firing gap is an observation from one sample per cell, under Opus 5.5 at high
effort, with the hooks off.

## Part B: does it route well once running

The prompts were typed `/hugues-stack:hugues-mode <task>`. The table gives the
scored signals per run.

| Task | Revision | State | Playbook read | Steps copied, in order, total | Principles read, named | Task signal |
|---|---|---|---|---|---|---|
| 1, bug fix | `main` | PARTIAL | bug-fix | 0, 0, 6 | 0, 0 | none |
| 1, bug fix | branch | PARTIAL | bug-fix | 0, 0, 6 | 3, 3 | none |
| 2, how does X work | `main` | PASS | investigation | 0, 0, 4 | 0, 0 | `how` reached by Skill call |
| 2, how does X work | branch | PASS | investigation | 0, 0, 4 | 0, 0 | `how` reached by reading `skills/how/SKILL.md` |
| 3, small Kotlin feature | `main` | PARTIAL | feature | 0, 0, 8 | 2, 2 | no mobile route read or named |
| 3, small Kotlin feature | branch | PASS | feature, `cmp-two-target-change` | 0, 0, 8 | 4, 3 | route `cmp-two-target-change` read |
| 4, check on PR N | `main` | PASS | babysit | 0, 0, 9 | 0, 0 | `check` mode declared |
| 4, check on PR N | branch | PASS | babysit | 0, 0, 9 | 1, 1 | `check` mode declared |

Principle reads on the branch are file reads of the leaf `SKILL.md`, as `host.md`
requires for user-only skills. On `main` the two reads in task 3 were Skill calls.

The comparison, by the rule fixed before the runs:

| Task | Branch matches or beats `main` | Where the branch is higher | Post-hoc note on steps in the reply |
|---|---|---|---|
| 1 | yes | principles read 3 against 0, named 3 against 0 | Neither lists the playbook. The branch's closing paragraph names, in prose, the steps it could not do (track in `bd`, reproduce on an emulator, test fail then pass, split commits, open a PR). |
| 2 | yes (tie) | none | `main` wrote the step 2 line `throughput checkpoint: n/a, read-only investigation` exactly; the branch did not. |
| 3 | yes | route `cmp-two-target-change` against none, principles read 4 against 2, named 3 against 2 | `main` listed the Feature playbook's eight steps in order under "Feature playbook status", paraphrased and with steps 6 to 8 merged. The branch did not list them. It wrote step 3's four checkpoint headings and named, in prose, the arena and delegation steps it could not run. |
| 4 | yes | principles read 1 against 0, named 1 against 0 | `main` listed the Babysit playbook's nine steps in order, paraphrased, each with its outcome. The branch did not. |

No signal was lower on the branch by the rule. The steps-in-reply note is a manual
read of the replies after scoring. It is the only place the branch is lower, and
only for tasks 3 and 4. What each run showed:

- **Task 1.** Both read the bug-fix playbook and the host and mobile adapters
  first, found the cause (the minus sign is grouped as a digit group), and gave
  the same two-line fix and a regression test as text, because neither had an edit
  tool. The branch read three principle files and gave a "Principles" section
  naming Fix Root Causes, Test Behavior Not Implementation and Laziness Protocol.
  `main` read none and said it would name none, in line with the router's rule
  to cite only principles it had read.
- **Task 2.** Both read the investigation playbook and the adapters, reached
  `how`, and answered in the `how` shape (Overview, Key Concepts, How It Works,
  Where Things Live, Gotchas). Neither spawned the explainer subagent. `main` said
  the session had no agent tool, and the branch said the files were small enough
  to read itself.
- **Task 3.** Both read the feature playbook and `mobile-workflows.md`. The
  branch then read `cmp-two-target-change.md` and selected it. `main` never read
  or named any of the four mobile routes, and its Playbooks list does not name
  them. Both derived the count from `requestsFor` and said that the on-screen
  proof was blocked because `RequestList` has no caller.
- **Task 4.** Both declared `check` mode before any poll (no poll was possible),
  tried the denied Gmail search, and told the owner how to run the status check
  themselves. The branch read the `watch-pr` CLI source to check flag spellings.

**Verdict.** PASS on the pre-registered pass condition in all four tasks, with
the single flagged post-hoc signal above. On the signals fixed in advance the
branch is not worse at routing, and it is better at selecting the mobile route and
at reading the principle files the router points at. The eval does not show that
the steps are copied into a todo list on either revision, because print mode has
no todo tool.

## cmp-test unchanged

`git status --short --untracked-files=all` in `cmp-test` printed the same two
lines before and after, both left from earlier work:

```
 M .beads/interactions.jsonl
?? .beads.gate.lock
```

HEAD stayed `666cfa1c3075011f13261c3eff31927d8d5ee234` on `main`. A SHA-256
manifest of all 1,944 files (everything except `.git/index`) is byte-identical
before and after, and so is a listing of every file's modification time. The
manifest SHA-256 is `1b2d7d1f3679904229cfdec6efea263a2a8f2ad933ab32f7c6d6aa3edd01911d`
both times, the same value the first attempt recorded. `git status` itself can
refresh `.git/index`, which the manifest leaves out. Every Read call in the
twenty streams went to a file under `cmp-test`, under one of the two `plugin`
folders, or to the one memory file under the owner's Claude project folder, which
was read three times and never written.

## Evidence

Each artifact is private, kept outside this repository; only its SHA-256 is
recorded here. The twenty stderr files are empty
(`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`).

| Artifact | SHA-256 |
|---|---|
| Stream, Part A, task 1, `main` | `aee9bc3e80810cc02b90424d1aaef8d6e75a99e84f34ae7f8787fc6176ec5a2e` |
| Stream, Part A, task 1, branch | `828cb994c4f214aac90a033add5e04d62ad41a4b7703d3130cd9b09855bf91da` |
| Stream, Part A, task 2, `main` | `733ca9618e3ae27b570b9c3bad579ca6f49e4dd14d2526c2ee8e510924265828` |
| Stream, Part A, task 2, branch | `18df29072fdd221e706f13a6eccbcdd0fbad7c32a87b80f4358e421467921ed9` |
| Stream, Part A, task 3, `main` | `f6443a71148bff622c0f489eef2d46f96695b14e258ebe7618435c4c6d283635` |
| Stream, Part A, task 3, branch | `f1e6535042b92baa6fc9c41776a95f540fa67aa0f71243995feb15cb71d13b42` |
| Stream, Part A, task 4, `main` | `7124a6b8d59d61f89a4355a46744353121e4edc76b2a95ffadbcafc21ca03090` |
| Stream, Part A, task 4, branch | `795e2087ef33743a2f56fea352b815f28785739f5fab376ae673101d2c85bfd8` |
| Stream, Part A, task 5, `main` | `6b1f7b242903a9deca08b2ec6e2ff09e687c5dbd311105c5dc13abdc11b43b1b` |
| Stream, Part A, task 5, branch | `f5fa8c85fb9fe3d9e8af1cff670ddce858a931b61e53e0108bd47e4f6c777814` |
| Stream, Part A, control, `main` | `b0c33a95ae07874ea8c76186f8aaa01d40cbb88416af330fe99454f0d05d1d29` |
| Stream, Part A, control, branch | `644b6fe6e63f2014ffb3348e3fe9c77e08d3c1b2b2159bbdc223ce631d590b7d` |
| Stream, Part B, task 1, `main` | `c21f0e3c9151236769f8a1e6e1650e88f70edc432d430aee1c3e0f266a11349e` |
| Stream, Part B, task 1, branch | `45fd4c635badda5e527a1d5844dbc7df0b6c5197d22946fb48e80514fdac2cdf` |
| Stream, Part B, task 2, `main` | `5fedc940e174d856225e42b5b3cea5dceb001815d9a46c53521c671a5f129436` |
| Stream, Part B, task 2, branch | `37cbc826012164f064cd4ba208d025e9db68771e93906c9546c1a26004e6fca9` |
| Stream, Part B, task 3, `main` | `d61c2e98b9e2b8a14ad404f14c1bff3112c58fc8e3ef84268727d3d169ff503f` |
| Stream, Part B, task 3, branch | `c188860a14f0d6a8abd77b0b44cf5d0385dcef2160b3cda6f29cb1b385ae8767` |
| Stream, Part B, task 4, `main` | `00c1b55bdc3e1bdc2c499132671ed97b793c692f9a55f0390a98045413bee7ac` |
| Stream, Part B, task 4, branch | `00abde92552239ed1b87aa977021c7decea5bf15bac413e4d4aa5b7b5ca597fb` |
| `runs/exit-codes.txt` (twenty lines, all exit 0) | `3b29ad490aa6f9a579f6d7bd642c86b1007a5cae95ea48eb4e831dbf19ce49c5` |
| `runs/scores-A.json` (the v1 and v2 scorer outputs are byte-identical) | `17bc90f5fc810246ecd24dc11369160b873f679375f2868a23b45de40f68901a` |
| `runs/scores-B.json` (v2 scorer output) | `b4a111bb33c48667b7aec137a47a4154dc21374cbfcb387c0e5e4ea494a64917` |
| `runs/scores-B.v1.json` (v1 scorer output) | `3adc36afe3a9e288e3d37b226939bf7a4051866ac63a58afe9034bc8df0030e3` |
| `runs/score-A.out.txt` (printed table) | `c8c2ceef9ae1cac08691b271ed0ede1b43081d43a974d3f0f70a093889efd75f` |
| `runs/score-B.out.txt` (printed table, v2) | `ae1ed1c41ff6549ec4ca153dae941b3190c153472372ecfa4cdba948803caee9` |
| `prompts.json` | `36761d33a9a2c4f4149425208e82a30a77a085aef0c8fe4c66fbd9c177cc934c` |
| `run-eval.sh` | `43bee3041e8da7d720b89da1f13e6fc358275af631eeb0da4fec148b71db4ca4` |
| `run-eval-A.out.txt` | `930f355a32ad86968d3afdf28c0a4b96cb73cf832f447c05f05a12a475d93882` |
| `run-eval-B.out.txt` | `1bdf86b7dfa918bb05c8010a307c33aea815392e963f7b50d2a51bfc3c5435a0` |
| `score.py` (v2, printed below) | `0a2f1707d559db2468a703862dda73ee379f6de556a3350276206a70e9e243fa` |
| `score.v1.py` (the scorer the cells were first scored with) | `3fa8bea5dac8f46bbbb8847c193fca17fab749abb5bddcef88459d349a2cdaf9` |
| `cmp-manifest.sh` | `70ce22e11038d961a6a3fe27cc6ab43036a65d294e3d3224bd080f36e7fe9cd1` |
| `cmp-test` file manifest, before and after (identical) | `1b2d7d1f3679904229cfdec6efea263a2a8f2ad933ab32f7c6d6aa3edd01911d` |
| `cmp-test` modification times, before and after (identical) | `35752845a52a205ae29acd751c4fac97cc8ffdfd5a499cfc16abd8e57d205967` |
| `cmp-test` `git status`, before | `06f71b935a7a6d3e958a5e5740cd2818f9148b7c0b415fa560cc56e01e489755` |
| `cmp-test` `git status`, after | `e8520477d0be1c075b0d41bf52c162261c598635a1b830b04a035c5528d0409f` |
| Probe, model and effort flag | `b0314d2b965780ede339f5c40e939a19c2093264a38b4dd927eccbca6a2d9618` |
| Probe, typed invocation, branch, reply "ready" | `8d2e2114636b1762c2dd9223e69638efbc30bd80892fa4653e0fbfabc3ee33eb` |
| Probe, typed invocation, heading quote, `main` | `f5ed13990c0a8d0fb176f1aa09a579b1ed7619fb1d07d9251e1e061c334f3909` |
| Probe, typed invocation, heading quote, branch | `1a6733129b5bd1cc7e4b3a101c0fb2e8d2d809b69aebb646a18e5a25b3c90a64` |

The two `git status` hashes differ only by their first line, a timestamp.

```python
"""Score the stream-json runs. Usage: python3 -I score.py <eval-2-dir> <main-root> <branch-root> <A|B>.

Signals come from the stream only (assistant tool_use blocks and assistant text blocks).
Rules, fixed before any cell ran:

PART A (natural prompts, --max-turns 10). Per run: skills invoked, and whether hugues-mode fired
(a Skill call named hugues-stack:hugues-mode or hugues-mode).
  t1-t4  PASS = hugues-mode fired. FAIL = it did not.
  t5     PASS = hugues-mode did not fire and no playbook was read. FAIL = it fired.
  c1     (positive control, diagnosing-bugs trigger words) PASS = Skill diagnosing-bugs invoked.
         FAIL = it was not. hugues-mode firing on c1 is recorded, not scored.
  A run with no result event is GAP.

PART B (typed /hugues-stack:hugues-mode <task>, --max-turns 25). The reply is every assistant text block.
  playbook_read      the expected playbook file was read (t1 bug-fix, t2 investigation, t3 feature, t4 babysit)
  steps_copied       playbook steps (numbered lines) whose first 60 characters, markup removed, appear in the reply
  steps_in_order     greedy count of steps found in the reply at or after the previous found step's position
  principles_read    distinct principle-* SKILL.md files read, or principle-* Skill calls
  principles_named   distinct principles whose slug or spaced title appears in the reply (case-insensitive;
                     v2, edited after the cells ran, also ignores punctuation: v1 missed 'Test Behavior, Not Implementation')
  how_reached        t2 only: Skill hugues-stack:how, or a read of skills/how/SKILL.md
  route_match        t3 only: playbooks/cmp-two-target-change.md read or named in the reply (the chips are CMP
                     rendering, mobile-workflows.md: "CMP rendering implementation adds cmp-two-target-change").
                     route_any / routes_read / routes_named list every mobile route read or named.
  mode_declared      t4 only: the reply declares a check/drive/etc. mode for the Babysit playbook
                     (regex: mode within 40 chars of check, either order).
  State per run:
    t1 PASS = playbook_read, steps_in_order == steps total, principles_read >= 1, principles_named >= 1.
    t2 PASS = playbook_read and how_reached.
    t3 PASS = playbook_read and route_match.
    t4 PASS = playbook_read and mode_declared.
    PARTIAL = playbook_read but not PASS.  FAIL = playbook not read.  GAP = no result event.
  Comparison (the plan's pass condition, read strictly): for each task the branch matches or beats main iff
  the branch's state rank >= main's AND every signal of the task (playbook_read, steps_in_order,
  principles_read, principles_named, plus how_reached / route_match / mode_declared for t2 / t3 / t4) is
  >= main's (booleans as 0/1, counts as numbers). Lower signals are listed by name.
"""
import hashlib, json, re, sys
from pathlib import Path

E, MAIN, BRANCH = (Path(a) for a in sys.argv[1:4])
PART = sys.argv[4]
EXPECT = {'t1': 'bug-fix', 't2': 'investigation', 't3': 'feature', 't4': 'babysit'}
ROUTES = ['build-doctor', 'mobile-proof', 'kmp-bridge-change', 'cmp-two-target-change']
RANK = {'FAIL': 0, 'GAP': 0, 'PARTIAL': 1, 'PASS': 2}
MODE_FIRED = ('hugues-stack:hugues-mode', 'hugues-mode')


def plain(text):
    return ' '.join(re.sub(r'[*`]', '', text).split())


def steps(path):
    return [m.group(2) for m in re.finditer(r'^(\d+)\. (.+)$', path.read_text(), re.M)]


def load(path):
    events = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    calls, text = [], []
    for e in events:
        if e.get('type') != 'assistant':
            continue
        for block in e['message']['content']:
            if block['type'] == 'tool_use':
                calls.append((block['name'], block['input']))
            elif block['type'] == 'text':
                text.append(block['text'])
    return events, calls, text


def common(task, rev, root):
    path = E / 'runs' / f'{PART}-{task}-{rev}.stream.jsonl'
    events, calls, text = load(path)
    out = {'task': task, 'revision': rev, 'stream_sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
    init = next((e for e in events if e.get('type') == 'system' and e.get('subtype') == 'init'), {})
    result = next((e for e in events if e.get('type') == 'result'), None)
    out['model'] = init.get('model')
    out['claude_code_version'] = init.get('claude_code_version')
    out['builtin_tools'] = [t for t in init.get('tools', []) if not t.startswith('mcp__')]
    out['plugin'] = next((p for p in init.get('plugins', []) if p['name'] == 'hugues-stack'), None)
    out['skills_in_list'] = len(init.get('skills', []))
    out['hook_events'] = sum(1 for e in events if e.get('type') == 'system' and str(e.get('subtype', '')).startswith('hook'))
    skills = [i.get('skill') for n, i in calls if n == 'Skill']
    reads = [i.get('file_path', '') for n, i in calls if n == 'Read']
    out['tool_sequence'] = [(n, i.get('skill') or i.get('file_path') or i.get('pattern') or i.get('path')) for n, i in calls]
    out['skills_invoked'] = skills
    out['fired'] = any(s in MODE_FIRED for s in skills)
    out['router_file_read'] = any(r.endswith('/skills/hugues-mode/SKILL.md') for r in reads)
    out['playbooks_read'] = [m.group(1) for r in reads for m in [re.search(r'/playbooks/([\w-]+)\.md$', r)] if m]
    out['adapter_reads'] = [Path(r).name for r in reads if '/adapters/' in r]
    out['reference_reads'] = [Path(r).name for r in reads if '/references/' in r]
    if result:
        out['result'] = {k: result.get(k) for k in ('subtype', 'is_error', 'num_turns', 'terminal_reason', 'total_cost_usd')}
        out['permission_denials'] = [d.get('tool_name') for d in (result.get('permission_denials') or [])]
    out['_calls'], out['_text'], out['_skills'], out['_reads'], out['_has_result'] = calls, text, skills, reads, result is not None
    out['first_text'] = text[0][:240].replace('\n', ' ') if text else None
    return out


def score_a(task, rev, root):
    out = common(task, rev, root)
    pbs = out['playbooks_read']
    if not out.pop('_has_result'):
        state = 'GAP'
    elif task == 't5':
        state = 'PASS' if not out['fired'] and not pbs else 'FAIL'
    elif task == 'c1':
        state = 'PASS' if any((s or '').split(':')[-1] == 'diagnosing-bugs' for s in out['_skills']) else 'FAIL'
    else:
        state = 'PASS' if out['fired'] else 'FAIL'
    for k in ('_calls', '_text', '_skills', '_reads'):
        out.pop(k)
    out['state'] = state
    return out


def score_b(task, rev, root):
    out = common(task, rev, root)
    calls, text, skills, reads = out.pop('_calls'), out.pop('_text'), out.pop('_skills'), out.pop('_reads')
    has_result = out.pop('_has_result')
    reply = '\n'.join(text)
    flat = plain(reply)
    expected = EXPECT[task]
    out['playbook_read'] = expected in out['playbooks_read']
    listed = steps(root / 'plugin/skills/hugues-mode/playbooks' / f'{expected}.md')
    found, last, in_order = [], 0, 0
    for s in listed:
        key = plain(s)[:60]
        if key in flat:
            found.append(s)
            idx = flat.find(key, last)
            if idx >= 0:
                in_order += 1
                last = idx
    out['steps_total'], out['steps_copied'], out['steps_in_order'] = len(listed), len(found), in_order
    principles = sorted({m.group(1) for r in reads for m in [re.search(r'/skills/(principle-[\w-]+)/SKILL\.md$', r)] if m}
                        | {s.split(':')[-1] for s in skills if s and s.split(':')[-1].startswith('principle-')})
    out['principles_read_list'] = principles
    out['principles_read'] = len(principles)
    slugs = sorted(p.name for p in (root / 'plugin/skills').iterdir() if p.name.startswith('principle-'))
    norm = lambda t: ' '.join(re.sub(r'[^a-z0-9]+', ' ', t.lower()).split())
    low = norm(reply)
    named = [s for s in slugs if norm(s) in low or norm(s.removeprefix('principle-')) in low]
    out['reply_numbered_items'] = len(re.findall(r'^\s*\d+\. ', reply, re.M))
    out['principles_named_list'] = named
    out['principles_named'] = len(named)
    out['how_reached'] = any((s or '').split(':')[-1] == 'how' for s in skills) or any(r.endswith('/skills/how/SKILL.md') for r in reads)
    out['routes_read'] = [p for p in out['playbooks_read'] if p in ROUTES]
    out['routes_named'] = [r for r in ROUTES if r in reply]
    out['route_any'] = bool(out['routes_read'] or out['routes_named'])
    out['route_match'] = 'cmp-two-target-change' in out['routes_read'] or 'cmp-two-target-change' in out['routes_named']
    out['mode_declared'] = bool(re.search(r'mode[^.\n]{0,40}\bcheck\b|\bcheck\b[^.\n]{0,40}\bmode\b', reply, re.I))
    out['reply_chars'] = len(reply)
    full = {
        't1': out['steps_in_order'] == out['steps_total'] and out['principles_read'] >= 1 and out['principles_named'] >= 1,
        't2': out['how_reached'], 't3': out['route_match'], 't4': out['mode_declared'],
    }[task]
    out['state'] = 'GAP' if not has_result else ('PASS' if out['playbook_read'] and full else 'PARTIAL' if out['playbook_read'] else 'FAIL')
    return out


def compare(main, branch, task):
    keys = ['playbook_read', 'steps_in_order', 'principles_read', 'principles_named']
    keys += {'t2': ['how_reached'], 't3': ['route_match'], 't4': ['mode_declared']}.get(task, [])
    lower = [k for k in keys if int(branch[k]) < int(main[k])]
    ok = RANK[branch['state']] >= RANK[main['state']] and not lower
    return ok, lower


tasks = ['t1', 't2', 't3', 't4', 't5', 'c1'] if PART == 'A' else ['t1', 't2', 't3', 't4']
scorer = score_a if PART == 'A' else score_b
rows = []
for task in tasks:
    for rev, root in (('main', MAIN), ('branch', BRANCH)):
        rows.append(scorer(task, rev, root))
(E / 'runs' / f'scores-{PART}.json').write_text(json.dumps(rows, indent=2) + '\n')
if PART == 'A':
    print('task | rev | state | fired | skills invoked | turns')
    for r in rows:
        print(r['task'], '|', r['revision'], '|', r['state'], '|', r['fired'], '|', r['skills_invoked'], '|', r['result']['num_turns'] if 'result' in r else None)
else:
    print('task | rev | state | playbook | steps copied/in order/total | principles read/named | how | route_match | mode_declared')
    for r in rows:
        print(r['task'], '|', r['revision'], '|', r['state'], '|', r['playbooks_read'], '|', r['steps_copied'], r['steps_in_order'], r['steps_total'], '|', r['principles_read'], r['principles_named'], '|', r['how_reached'], '|', r['route_match'], r['routes_read'], r['routes_named'], '|', r['mode_declared'])
    print()
    for task in tasks:
        m, b = (next(r for r in rows if r['task'] == task and r['revision'] == rev) for rev in ('main', 'branch'))
        ok, lower = compare(m, b, task)
        print(task, 'branch matches or beats main:', ok, 'lower signals:', lower)
```

## Gaps

| Cell | State |
|---|---|
| Router fires on a bug fix, "how X works" question, small feature or PR-status request in Claude Code with `claude-opus-5-5` at high effort | OBSERVED on the branch for 3 of 4 (tasks 2, 3, 4) and on `main` for 0 of 4, one sample per cell |
| Router stays quiet on a casual question | OBSERVED on both revisions (0 of 2 fired) |
| Positive control: a personal skill fires in print mode | OBSERVED on both revisions |
| Playbook selection, principle reads, mobile route and Babysit mode after a typed `/hugues-stack:hugues-mode` | OBSERVED on both revisions, one sample per cell |
| Playbook steps copied verbatim into a todo list | NOT OBSERVED (print mode has no todo tool; no run copied a step verbatim; the interactive run was not needed for the control and was not made) |
| Which of PR 1 and PR 2 caused each difference | NOT RUN (no revision carried PR 1 alone) |
| The router description text as the model sees it in Claude Code with Opus 5.5 | NOT OBSERVED (the router fired by name, which shows the skill was listed, but the rendered text was not captured; the first attempt's check used Sonnet 5.5 and the earlier 312-character description) |
| Effort level as echoed by the host | NOT OBSERVED (set by `--effort high`; the stream does not report it) |
| Task 4 with shell and `gh` available | NOT RUN (read-only restriction by design) |
| Effect of the start-of-session hooks on whether the router fires | NOT RUN (hooks were off for every run) |
| More than one sample per cell | NOT RUN (one run per cell, as the Issue specifies) |
| Other models, or the router under an interactive session | NOT RUN |
| Router eval in Codex | NOT RUN (out of scope) |
| Mobile device, build or simulator proof | NOT RUN |

The Issue's "Risk" note anticipated that the router is the only automatic way
into most of the stack. On this evidence the branch's trigger reached it for
three of four task prompts under `claude-opus-5-5` at high effort, where `main`'s
reached it for none, and the miss on a bug fix went to a personal skill that the
owner has installed.
