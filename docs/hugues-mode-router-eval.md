# Hugues mode router eval

This receipt binds the Issue #22 routing eval to one commit. The rewritten
router was tested at code commit `3d39448beb7ec2288243db1263f52b316ffc89e7`,
tree `ec0714bd1530f548a4af54edbd13df2ff02d02f1`, branch
`feat/hugues-mode-router`, stacked on `feat/skill-list-budget` at `e563e25`.
It was compared with `main` at `a67df901162cc2add4aabb9e2a3843134696c490`. The
branch worktree printed nothing for `git status --short` at the start of the
run (the script below prints it first). The commit that carries this receipt
changes documentation only; `git diff 3d39448 HEAD -- plugin scripts tests`
is empty.

Ten runs, one per cell, all exited 0 and none was repeated or aborted. Raw
streams stay private, outside this repository; this receipt records their
SHA-256 and the per-cell states, not their contents. Nothing in the consumer
app `cmp-test` changed (see below). No host configuration file was edited and
nothing was installed: Claude Code loaded each revision with `--plugin-dir`
for one session at a time and wrote no session transcript
(`--no-session-persistence`). Claude Code's own routine state writes are not
audited here.

## Verdict

**The eval did not show the router routing, on either revision.** In tasks 1 to
4 the model never invoked `hugues-mode` on `main` or on the branch, so those
eight cells are FAIL against the spec's expectations (the mode fires, a
playbook is selected, its steps are copied, a principle is read). Task 5 did not
fire on either revision, so both task 5 cells are PASS.

The pass condition in the Issue is "this branch matches or beats `main` in
every cell, and task 5 does not fire on either revision". Read literally it
holds: the branch ties `main` in all five tasks and task 5 stayed quiet on both.
It holds only because both revisions failed in the same way, and it carries no
evidence that the rewrite improves routing or that the broader trigger from the
skill-list work fires at all. Per the task rules, a failed cell is reported as
failed and was not re-run, and no text was tuned. The rewritten body is tested
statically (the core and plugin checks and the unit suite) and not by a host
run, because no run reached it.

## Commands

Claude Code `2.1.293`, model `claude-sonnet-5-5` (the stream's init event names
both, and `--model` pinned it for every run). `<root>` stands for the
machine-specific folder that holds `huguesStack.worktrees` and `cmp-test`. The
`main` revision ran from a throwaway detached worktree
`huguesStack.worktrees/_eval-main` at `a67df90`, removed afterwards. Both
revisions loaded the same ambient setup: the owner's user-level plugins, skills
and MCP servers stayed enabled, 143 skills in the init event of every run. The
script was saved as `run-eval.sh` in the evidence folder and run there as
`sh ./run-eval.sh <root> > run-eval.out.txt 2>&1` (exit 0). The five prompts
are in `prompts.json` and `score.py` is printed after the script. All three were
written before the first run and are unchanged since.

```sh
#!/bin/sh
# Usage: sh run-eval.sh <root>   where <root> holds huguesStack.worktrees and cmp-test's parent.
# Runs each of five prompts once on main (a67df90) and once on the branch code commit.
set -u
ROOT="$1"
E="$ROOT/huguesStack.worktrees/_evidence/hugues-mode-router"
MAIN="$ROOT/huguesStack.worktrees/_eval-main"
BRANCH="$ROOT/huguesStack.worktrees/feat/hugues-mode-router"
CMP="$ROOT/cmp-test"
SCRATCH="$E/scratch"

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
  out="$E/runs/$id-$rev"
  date -u +%Y-%m-%dT%H:%M:%SZ > "$out.started"
  (cd "$dir" && claude -p "$prompt" \
    --model claude-sonnet-5-5 --no-session-persistence \
    --plugin-dir "$plugin" \
    --settings '{"disableAllHooks": true}' \
    --tools "Read,Glob,Grep,Skill" --allowedTools Read Glob Grep Skill \
    --disallowedTools Edit Write MultiEdit NotebookEdit Bash Task Agent \
    --permission-mode dontAsk --max-turns 10 \
    --output-format stream-json --verbose \
    < /dev/null > "$out.stream.jsonl" 2> "$out.stderr.txt"); echo "$id $rev exit $?" | tee -a "$E/runs/exit-codes.txt"
}

for id in t1 t2 t3 t4 t5; do
  run "$id" main "$MAIN/plugin"
  run "$id" branch "$BRANCH/plugin"
done
```

## Prompts

Each prompt ran once per revision, unchanged, with no instruction to stop after
routing. Tasks 1, 2, 3 and 5 ran with `cmp-test` as the working directory. Task 4
ran in an empty scratch folder, because it asks about a huguesStack PR and
`cmp-test` is a different repository.

| Task | Prompt |
|---|---|
| 1, bug fix | A negative settlement amount like -123456 shows up on the request card as "-,123,456" with a stray comma. Can you fix it? |
| 2, how does X work | How does the request list decide which settlement requests to show under each tab? |
| 3, small Kotlin feature | I'd like a small feature: the tab chips on the request list should show how many requests each tab holds, like "Pending (3)". Please put the counting in the shared Kotlin logic and wire it into the chips. |
| 4, check on PR N | Check on PR 20 in hugues-vnsgn/huguesStack. |
| 5, casual question | Quick question before I forget: for a top-level string constant in Kotlin, is it better to use val or const val? |

The task 1 bug is real: `formatAmountMinor(-123456)` returns `-,123,456`, which
was checked by hand against the source, not by running Kotlin. PR 20 is a merged
huguesStack PR.

## Harness choices and what they cost

These apply to both revisions equally.

- **Read-only.** `--tools "Read,Glob,Grep,Skill"`, `--allowedTools` with the same
  four, `--disallowedTools` for the edit, write, shell and agent tools, and
  `--permission-mode dontAsk` so that anything not allowed is denied. The
  stream's init event lists exactly those four built-in tools for every run. The
  model tried `Edit`, `Write` and `Bash` in tasks 1 and 3 anyway and each call
  came back as "No such tool available". In task 4 on the branch it tried a
  Gmail search through the owner's connected Gmail connector. That call was
  denied (`permission_denials: 1`) and returned nothing. The connectors stay
  visible to the model because the ambient setup stays enabled.
- **Hooks off.** `--settings '{"disableAllHooks": true}'` suppressed every hook
  (the streams carry zero hook events). Two things forced this. First, the
  project's own `SessionStart` hook runs `bd prime --hook-json`; on a throwaway
  copy of `cmp-test` it rewrote three embedded Dolt files with identical bytes
  and new modification times, so it cannot run in `cmp-test` without touching
  it. Second, the ambient agentmemory plugin has hooks on prompts and tool uses
  that would record these synthetic sessions in the owner's memory store. The
  cost is that the real setup's start-of-session context from those hooks is
  absent in every run, and its effect on whether the router fires is unobserved.
  Project settings and the project's `CLAUDE.md` stayed in effect (a probe
  confirmed the model quotes its issue-tracker rule), and skills, plugins and
  connectors stayed enabled.
- **Print mode has no todo tool.** `claude -p` in `2.1.293` exposes no
  `TodoWrite` or `TaskCreate` (a `--tools default` probe lists none), and the
  project's `CLAUDE.md` forbids both anyway. A todo list could only appear in
  the reply text, so `score.py` reads steps from the reply. No cell reached that
  step.
- **Turn cap.** `--max-turns 10`. No run reached it as an error; the runs that
  used 9 or 10 turns ended with `success`.
- **Task 4 and shell access.** With no shell and no GitHub tool, the model
  concluded it could not reach the PR. The read-only restriction may have
  contributed to task 4 not firing, on both revisions. It is recorded as a
  finding, and nothing was changed to work around it.

## Checks run before the cells

Six runs that are not cells, all in a throwaway copy of `cmp-test` or a scratch
folder, used different prompts, and produced no counted result. They only
checked the harness.

- One vague dry run ("the greeting text looks wrong on iOS, can you look into
  it and fix it?") on the branch, with `--setting-sources user` and
  `--max-turns 4`. The model grepped and read files and invoked no skill.
- A `--tools default` probe that listed the built-in tools of print mode.
- A probe that a plugin file outside the working directory can be read under
  `dontAsk` with no `--add-dir`. The same run showed that
  `--setting-sources user` drops the project's `CLAUDE.md` (the model said it
  was not in context), which is why that flag was not used for the cells.
- A probe that `disableAllHooks` produces zero hook events, keeps the project's
  `CLAUDE.md` (the model quoted its issue-tracker rule) and leaves a copy of
  the project untouched.
- Two skill-list probes, one per revision (below).

**What the model sees in its skill list.** Asked without tools, the model on
`main` reported 46 `hugues-stack:*` skills and quoted the old `hugues-mode`
description ("poteto's agent style for concise, detailed responses..."). On the
branch it reported exactly two, `hugues-mode` and `setup-huguesstack`, and quoted
the 312-character router description, which equals the frontmatter text
character for character. This closes one cell the skill-list receipt left open
(the router description as the model sees it) for this Claude Code version, as
the model's own report of its context and not a debug-log line.

## Cells

States: PASS meets the spec's expectation for the task, PARTIAL fires the mode
and selects the right playbook but misses a later signal, FAIL does not meet
PARTIAL. The rules are in `score.py`, below, and were fixed before any run.

| Task | `main` | Branch | Branch matches or beats `main` |
|---|---|---|---|
| 1, bug fix | FAIL | FAIL | yes (tie) |
| 2, how does X work | FAIL | FAIL | yes (tie) |
| 3, small Kotlin feature | FAIL | FAIL | yes (tie) |
| 4, check on PR N | FAIL | FAIL | yes (tie) |
| 5, casual question | PASS (did not fire) | PASS (did not fire) | yes (tie) |

What each run did, from its stream:

- **Task 1.** Neither revision invoked any skill. Both grepped for the formatter,
  read `AmountFormat.kt` and its test, tried to edit (`Edit` or `Write`, plus
  `Bash` on `main`; all unavailable), then reported the root cause and the fix
  they would apply. `main` took 8 turns, the branch 7. No playbook, no copied
  steps, no principle read.
- **Task 2.** Neither revision invoked any skill. Both grepped, read
  `SettlementDisplayRules.kt` and `RequestList.kt`, and answered in 4 turns. The
  prompt is the "how X works" case that the router description names, and the
  branch did not fire on it.
- **Task 3.** Neither revision invoked any skill. Both read the list, the rules
  and their test, then tried three `Edit` calls (unavailable). 10 turns on
  `main`, 9 on the branch. No mobile route and no adapter was read.
- **Task 4.** Neither revision invoked any skill. `main` answered in one turn
  that it had no tool to reach the PR. The branch said the same, then tried the
  Gmail search (denied) and answered in two turns. No Babysit playbook, no mode
  declared.
- **Task 5.** Neither revision invoked any skill or read any playbook. Both
  answered in one turn: use `const val` when the value is a compile-time
  constant.

No run invoked a skill of any kind, not `hugues-mode`, not a principle, not one
of the owner's personal skills. Every run used the `Skill` tool zero times.

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
both times. `git status` itself can refresh `.git/index`, which the manifest
leaves out.

## Evidence

Each artifact is private, kept outside this repository; only its SHA-256 is
recorded here. The ten stderr files are empty
(`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`). Runs
started between 2026-10-09T02:09:53Z and 02:11:54Z.

| Artifact | SHA-256 |
|---|---|
| Stream, task 1, `main` | `443dac39f2f6c2f6ca47bd29d8acecf48538dcff23f5c6ff56aa058d8c79813f` |
| Stream, task 1, branch | `ed949a6c8816d925121ab90e0e844b12ca25d92a0148628f7074c6a38840e9e8` |
| Stream, task 2, `main` | `58fc8354d087127a7c5899f645273839b260b73f8c69943b17de192029a2b47a` |
| Stream, task 2, branch | `d260d96995c9ec55cf172edf2ddc4dcfe442a62ec268562d3d23508d1d3961a5` |
| Stream, task 3, `main` | `9392e95a9a135c433d1878e13662326705ebed7bc3264f99e2312833bf58ebfe` |
| Stream, task 3, branch | `9858b65b54aebf81f10486f3af5940559564a1434691567dc656e1d7659dfa02` |
| Stream, task 4, `main` | `908878a48347514fd9c0d4034ffb9dfdda528b5c298bbe8a2afbb8fc30a2ea45` |
| Stream, task 4, branch | `43022dde15fe0acae156b63244c37a03c5be36fc498c42b5d932d7fb6cb65a01` |
| Stream, task 5, `main` | `f8ec21b0712545fdc85e42c01a7d5e782de6ea64d6e3e83851c931b5fd71d72e` |
| Stream, task 5, branch | `00ff12fdd6dc86cd70edb433a99d6228003b0bcbf049fb6f1777f97b4315bf85` |
| `runs/exit-codes.txt` (ten lines, all exit 0) | `6eaca09471421e4a07e6441b54a9d3b63d4a911b8e635f68c270adb331beb9bc` |
| `runs/scores.json` (the scorer's output) | `8af64bed5974302576bd793bf22ccdf8bb9a2cdc6903dc895af5293ccfff74bd` |
| `prompts.json` | `926eac1056f832b44a95ead307e95ed4351158fede50cef7b148ecc8f4084ea7` |
| `run-eval.sh` | `a70b444a776dc8df2774aecf0e84da754c3eff0293acbe6bb3c644cc316bec5e` |
| `run-eval.out.txt` | `15f5d36acd51584771053cff88833f6456de14d1498ccc3c5dd85d0170f63270` |
| `score.py` | `19e2a8f0df20475bfd80b3e26247269143e8847d0f933365e72a253b40263e22` |
| `cmp-test` file manifest, before and after (identical) | `1b2d7d1f3679904229cfdec6efea263a2a8f2ad933ab32f7c6d6aa3edd01911d` |
| `cmp-test` modification times, before and after (identical) | `35752845a52a205ae29acd751c4fac97cc8ffdfd5a499cfc16abd8e57d205967` |
| `cmp-test` `git status`, before | `ca21ce3e8662058bc46cd50132557529af94fa2c71a8d44427413206fa3915b6` |
| `cmp-test` `git status`, after | `a4b8d7fb0a3c5626a0e826e40c9e679abee92e4df8835b01063900103f97ab9c` |
| Skill-list probe, `main` | `a575b6a37078ca52615419e692e663233e84a89447cbee863bdd2ecd21945d0d` |
| Skill-list probe, branch | `110591bd08c02d8deffce26d479f33586d270cc491956743a1f7bcbabc0e1d23` |
| Dry run, vague prompt | `61e8066dff8bad6197bb346c6a543d67fde167041b3a8578ff14b3dbf58ae2a9` |
| Probe, built-in tools of print mode | `e2c957484183d6faa320fdd36c54aa962e287e328f409b1b3c2c85d44f104d17` |
| Probe, plugin-file read and `CLAUDE.md` | `6f0bbd1dc85a92504ba3294d2e0d3e450a53794418ab499e31494b76b0c11892` |
| Probe, `disableAllHooks` | `540deaf0f3cc09540571c4f7c46f33601e938ac258e9cd1aeda52cc38ac0a4d7` |

The two `git status` hashes differ only by their first line, a timestamp.

```python
"""Score the stream-json runs. Usage: python3 -I score.py <evidence-dir> <main-root> <branch-root>.

Signals are read from the stream only. State rules (fixed before any run):
  t1 bug fix        PASS = mode fired, bug-fix playbook read, every playbook step copied (markup-insensitive,
                    first 60 characters), a principle leaf read, that principle cited in the reply text.
                    PARTIAL = mode fired and bug-fix playbook read, but a later signal is missing.
  t2 how X works    PASS = mode fired, investigation playbook read, `how` reached (Skill or SKILL.md read).
                    PARTIAL = mode fired and investigation read, `how` not reached.
  t3 feature        PASS = mode fired, feature playbook read, a mobile route playbook read or named in the
                    reply text. PARTIAL = mode fired and feature read, no route.
  t4 PR status      PASS = mode fired, babysit playbook read, a `check` mode declared in the reply text.
                    PARTIAL = mode fired and babysit read, no declaration.
  t5 casual         PASS = mode not fired and no playbook read. FAIL = mode fired.
  Any cell that does not meet PARTIAL is FAIL. A run with no result event is GAP.
"""
import hashlib, json, re, sys
from pathlib import Path

E, MAIN, BRANCH = (Path(a) for a in sys.argv[1:4])
EXPECT = {'t1': 'bug-fix', 't2': 'investigation', 't3': 'feature', 't4': 'babysit'}
ROUTES = ['build-doctor', 'mobile-proof', 'kmp-bridge-change', 'cmp-two-target-change']
RANK = {'FAIL': 0, 'GAP': 0, 'PARTIAL': 1, 'PASS': 2}


def plain(text):
    return ' '.join(re.sub(r'[*`]', '', text).split())


def steps(path):
    body = path.read_text()
    return [m.group(2) for m in re.finditer(r'^(\d+)\. (.+)$', body, re.M)]


def score(task, rev, root):
    path = E / 'runs' / f'{task}-{rev}.stream.jsonl'
    events = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    out = {'task': task, 'revision': rev, 'stream_sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
    init = next((e for e in events if e.get('type') == 'system' and e.get('subtype') == 'init'), {})
    result = next((e for e in events if e.get('type') == 'result'), None)
    out['model'] = init.get('model')
    out['claude_code_version'] = init.get('claude_code_version')
    out['tools'] = [t for t in init.get('tools', []) if not t.startswith('mcp__')]
    out['plugin'] = next((p for p in init.get('plugins', []) if p['name'] == 'hugues-stack'), None)
    out['hook_events'] = sum(1 for e in events if e.get('type') == 'system' and str(e.get('subtype', '')).startswith('hook'))
    calls, text = [], []
    for index, e in enumerate(events):
        if e.get('type') != 'assistant':
            continue
        for block in e['message']['content']:
            if block['type'] == 'tool_use':
                calls.append((index, block['name'], block['input']))
            elif block['type'] == 'text':
                text.append((index, block['text']))
    skills = [c[2].get('skill') for c in calls if c[1] == 'Skill']
    reads = [c[2].get('file_path', '') for c in calls if c[1] == 'Read']
    out['tool_sequence'] = [(c[1], c[2].get('skill') or c[2].get('file_path') or c[2].get('pattern') or c[2].get('path')) for c in calls]
    out['fired'] = any(s in ('hugues-stack:hugues-mode', 'hugues-mode') for s in skills)
    out['skills_invoked'] = skills
    out['playbooks_read'] = [m.group(1) for r in reads for m in [re.search(r'/playbooks/([\w-]+)\.md$', r)] if m]
    principles = [m.group(1) for r in reads for m in [re.search(r'/skills/(principle-[\w-]+)/SKILL\.md$', r)] if m]
    principles += [s.split(':')[-1] for s in skills if s and s.split(':')[-1].startswith('principle-')]
    out['principles_read'] = principles
    out['how_reached'] = any((s or '').split(':')[-1] == 'how' for s in skills) or any(r.endswith('/skills/how/SKILL.md') for r in reads)
    out['adapter_reads'] = [Path(r).name for r in reads if '/adapters/' in r]
    out['route_playbooks_read'] = [p for p in out['playbooks_read'] if p in ROUTES]
    reply = '\n'.join(t for _, t in text)
    out['route_named_in_text'] = [r for r in ROUTES if r in reply]
    out['principle_cited'] = [p for p in principles if p in reply or p.removeprefix('principle-').replace('-', ' ') in reply.lower()]
    expected = EXPECT.get(task)
    if expected:
        pb = root / 'plugin/skills/hugues-mode/playbooks' / f'{expected}.md'
        listed = steps(pb)
        flat = plain(reply)
        matched = [s for s in listed if plain(s)[:60] in flat]
        out['steps_total'], out['steps_copied'] = len(listed), len(matched)
    out['check_mode_declared'] = bool(re.search(r'mode[^.\n]{0,40}\bcheck\b|\bcheck\b[^.\n]{0,40}\bmode\b', reply, re.I))
    out['first_text'] = (text[0][1][:240].replace('\n', ' ') if text else None)
    if result:
        out['result'] = {k: result.get(k) for k in ('subtype', 'is_error', 'num_turns', 'terminal_reason', 'total_cost_usd')}
        out['permission_denials'] = len(result.get('permission_denials') or [])
    pbs = out['playbooks_read']
    if result is None:
        state = 'GAP'
    elif task == 't5':
        state = 'PASS' if not out['fired'] and not pbs else 'FAIL'
    else:
        base = out['fired'] and expected in pbs
        full = {
            't1': out['steps_copied'] == out['steps_total'] and bool(principles) and bool(out['principle_cited']) if 'steps_total' in out else False,
            't2': out['how_reached'],
            't3': bool(out['route_playbooks_read'] or out['route_named_in_text']),
            't4': out['check_mode_declared'],
        }[task]
        state = ('PASS' if full else 'PARTIAL') if base else 'FAIL'
    out['state'] = state
    return out


rows = []
for task in ['t1', 't2', 't3', 't4', 't5']:
    for rev, root in (('main', MAIN), ('branch', BRANCH)):
        rows.append(score(task, rev, root))
(E / 'runs/scores.json').write_text(json.dumps(rows, indent=2) + '\n')
print('task | main | branch | branch >= main')
for task in ['t1', 't2', 't3', 't4', 't5']:
    m, b = (next(r for r in rows if r['task'] == task and r['revision'] == rev) for rev in ('main', 'branch'))
    print(task, '|', m['state'], '|', b['state'], '|', RANK[b['state']] >= RANK[m['state']])
```

`score.py` read each revision's own playbook files to list the steps to match.
It ran after `_eval-main` still existed and printed the table above.

## Gaps

| Cell | State |
|---|---|
| Router fires on a bug fix, "how X works" question, small feature or PR-status request in Claude Code | NOT OBSERVED on `main` or the branch (0 of 8) |
| Router stays quiet on a casual question | OBSERVED on both revisions (0 of 2 fired) |
| Playbook selection, verbatim steps, principle read and cited, mobile route, Babysit mode declaration | NOT RUN (no run reached them) |
| Rewritten body after a typed `/hugues-stack:hugues-mode` invocation | NOT RUN (outside the Issue's five tasks) |
| Task 4 with shell and `gh` available | NOT RUN (read-only restriction by design) |
| Effect of the start-of-session hooks on whether the router fires | NOT RUN (hooks were off for every run) |
| More than one sample per cell | NOT RUN (one run per cell, as the Issue specifies) |
| Router eval in Codex | NOT RUN (out of scope) |
| Mobile device, build or simulator proof | NOT RUN |

The Issue's "Risk" note anticipated this outcome: the router is the only
automatic way into most of the stack, and when it fails to fire the bundled
skills are reachable only by typing them. This eval observed that failure
mode on the first four tasks, on both revisions.
