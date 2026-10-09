# Skill-list host validation

This receipt binds the Issue #21 host observations to one commit. Fix round 3
(9 October 2026) reran every observation against code commit
`2559b5d86811b749712fbcf78bbabb7a1650ceec`, tree
`477c26aca79fc9551f74121d1332ef544d198264`, branch `feat/skill-list-budget`,
from a worktree whose `git status` was empty. The commit that carries this
receipt changes documentation only; `git diff 2559b5d HEAD -- plugin` is empty.
Nothing here carries over from an earlier round: the receipt text for `6a6f31d`
is superseded, and its artifacts are not reused.

Each of the five host commands below wrote its own new files in an evidence
folder created for this round, ran once, exited 0 and was not repeated, so no
artifact holds a session from an earlier round or from an aborted run. No
consumer app was edited or executed. No host configuration file was edited and
nothing was installed: Claude Code loaded the plugin with `--plugin-dir` for
one session at a time and wrote no session transcript
(`--no-session-persistence`); Codex read a project-local `.agents/skills` link
inside a scratch directory. Each host's own routine state writes are not
audited here. Raw logs stay private, outside this repository; this receipt
records their SHA-256 and the per-cell states, not their contents.

## Commands

`<worktree>` is the checkout at the commit above, `<evidence>` the private
folder, `<scratch>` an empty directory inside it. Claude Code `2.1.293`, model
`claude-sonnet-5-5` (the debug log names it); Codex CLI `0.161.0`. Claude runs
started in `<scratch>/claude`, the Codex run in `<scratch>/codex`.

```sh
# 1. Without huguesStack
claude -p "Reply with the single word ACK and nothing else." \
  --model claude-sonnet-5-5 --no-session-persistence \
  --debug-file "<evidence>/claude-without-plugin.debug.log" \
  > "<evidence>/claude-without-plugin.stdout.log" 2> "<evidence>/claude-without-plugin.stderr.log"

# 2. With huguesStack
claude -p "Reply with the single word ACK and nothing else." \
  --model claude-sonnet-5-5 --no-session-persistence --plugin-dir "<worktree>/plugin" \
  --debug-file "<evidence>/claude-with-plugin.debug.log" \
  > "<evidence>/claude-with-plugin.stdout.log" 2> "<evidence>/claude-with-plugin.stderr.log"

# 3. Typed invocation of a user-only skill
claude -p '/hugues-stack:tdd Quote one exact sentence from the instructions this skill gave you, verbatim, inside double quotes, then stop. Do not write or run anything else.' \
  --model claude-sonnet-5-5 --no-session-persistence --plugin-dir "<worktree>/plugin" \
  --debug-file "<evidence>/claude-by-name-tdd.debug.log" \
  > "<evidence>/claude-by-name-tdd.stdout.log" 2> "<evidence>/claude-by-name-tdd.stderr.log"

# 4. Control for 3: the same prompt, no --plugin-dir
claude -p '/hugues-stack:tdd Quote one exact sentence from the instructions this skill gave you, verbatim, inside double quotes, then stop. Do not write or run anything else.' \
  --model claude-sonnet-5-5 --no-session-persistence \
  --debug-file "<evidence>/claude-by-name-tdd-control-without-plugin.debug.log" \
  > "<evidence>/claude-by-name-tdd-control-without-plugin.stdout.log" \
  2> "<evidence>/claude-by-name-tdd-control-without-plugin.stderr.log"

# 5. Codex: render the model-visible prompt input (local; no request to OpenAI)
ln -s "<worktree>/plugin/skills" "<scratch>/codex/.agents/skills"
(cd "<scratch>/codex" && codex debug prompt-input "Reply with the single word ACK and nothing else.") \
  > "<evidence>/codex-prompt-input.raw.json" 2> "<evidence>/codex-prompt-input.stderr.log"
```

Two read-only checks followed. The first extracts and measures the Codex
block with `extract.py` (below); the second looks for the sentence run 3 quoted:

```sh
python3 -I extract.py "<evidence>/codex-prompt-input.raw.json" "<worktree>/plugin/skills" \
  "<evidence>/codex-skills-instructions-block.txt"
grep -F -n 'Do not force a test when it would be impractical.' "<worktree>/plugin/skills/tdd/SKILL.md"
```

```python
import json, re, sys
from pathlib import Path

raw, plugin_skills, out_block = map(Path, sys.argv[1:4])
messages = json.loads(raw.read_text())
texts = [part["text"] for message in messages for part in message.get("content", [])
         if part.get("type") == "input_text"]
block = re.search(r"<skills_instructions>.*?</skills_instructions>",
                  next(t for t in texts if "<skills_instructions>" in t), re.S).group(0)
out_block.write_text(block)
roots = re.findall(r"^- `(r\d+)` = `", block, re.M)
entries = [l for l in block.split("### Available skills", 1)[1].splitlines() if l.startswith("- ")]
print("skill roots:", len(roots))
print("bullet lines in block:", sum(l.startswith("- ") for l in block.splitlines()),
      "= roots", len(roots), "+ skill entries", len(entries))
bundled = sorted(p.name for p in plugin_skills.iterdir() if p.is_dir())
in_root = lambda l, root: f"(file: {root}/" in l
huguesstack = [l for l in entries if in_root(l, roots[-1])]
print("entries under the huguesStack root:", len(huguesstack), "of", len(bundled), "skill directories")
for line in huguesstack:
    name = re.match(r"- ([^:]+:[^:]+):", line).group(1)
    skill = name.split(":")[1]
    description = line.split(name + ": ", 1)[1].rsplit(" (file:", 1)[0]
    declared = re.search(r"^description:\s*(.+)$",
                         (plugin_skills / skill / "SKILL.md").read_text().split("---", 2)[1], re.M).group(1).strip()
    print(" ", name, "rendered", len(description), "of", len(declared), "characters;",
          "complete" if description == declared else ("prefix of declared" if declared.startswith(description) else "DIFFERS"))
other = [(re.match(r"- ([^:]+):", l).group(1), re.search(r"\(file: (r\d+)/", l).group(1))
         for l in entries if not in_root(l, roots[-1]) and re.match(r"- ([^:]+):", l).group(1) in bundled]
print("same-named skills from other roots:", other)
```

## Claude Code: skill count with and without huguesStack

Runs 1 and 2, started 2026-10-09T01:16:58Z and 01:17:07Z.

- Without huguesStack, the debug log says `getSkills returning: 65 skill dir
  commands, 20 plugin skills, 39 bundled skills, 1 builtin plugin skills`, then
  `Sending 63 skills via attachment (initial)`.
- With `--plugin-dir`, it says `Loaded 50 skills from plugin hugues-stack
  default directory`, then `getSkills returning: 65 skill dir commands, 70
  plugin skills, 39 bundled skills, 1 builtin plugin skills`, then `Sending 65
  skills via attachment (initial)`.

**State: OBSERVED.** The attached list grows by exactly **2** (63 to 65), the
number of model-invocable skills in the source (`hugues-mode`,
`setup-huguesstack`); all 50 directories load, and the other 48 are not
attached. The log carries counts, not names, so which two skills were attached
is inferred from that arithmetic, not observed. Both replies were `ACK`. This
observes the count half of Issue user stories 1 and 28.

## Claude Code: typed invocation of a user-only skill

Runs 3 and 4, started 01:17:21Z and 01:17:37Z. `tdd` is user-only
(`disable-model-invocation: true`), so it is not one of the two attached skills.

With the plugin, the reply was exactly: `"Do not force a test when it would be
impractical."` Line 17 of `plugin/skills/tdd/SKILL.md` begins with that
sentence: "Do not force a test when it would be impractical. If the available test
would require broad harness setup, brittle mocks, ..." The `grep -F` above
finds it once, verbatim. That checked sentence is the only quote this receipt
takes from the file.

Without the plugin (the control), the same prompt produced no skill text: the
model said `/hugues-stack:tdd` "didn't run and gave me no instructions" and that
a plain `/tdd` skill is listed, which is the owner's personal one.

**State: OBSERVED**, with a control. Typing a user-only skill by its namespaced
name still runs it. This closes the typed-invocation half of Issue user stories
3 and 28. Run 3's stderr holds one line from a SessionEnd hook of another
installed plugin (`agentmemory`); huguesStack ships no hooks.

*Correction to the previous version of this receipt.* It said the reply quoted
two phrases that a `grep` of the file confirmed. Only one was in the file as a
phrase: "Write the failing test first" occurs once, inside step 3's
"**Write the failing test first.**". "When one would be impractical" occurs
nowhere in `tdd/SKILL.md`, which says "when it would be impractical". That was a
paraphrase, not an exact phrase.

## Codex: prompt-input skills block

Run 5, started 01:17:49Z. `codex debug prompt-input` renders the model-visible
prompt input locally. It ran from a scratch directory outside the repository
that held only a project-local `.agents/skills` link to `<worktree>/plugin/skills`.

The rendered `skills_instructions` block has 8 skill roots and **77** skill
entries: 85 bullet lines, which include the 8 root lines (the previous version
of this receipt called 85 "skills"). Exactly two entries come from the
huguesStack root: `hugues-stack:hugues-mode` and
`hugues-stack:setup-huguesstack`. The other 48 skill directories under that root
have no entry. The only same-named entries in the block (`recall`, `tdd`,
`unslop`) come from the owner's own `~/.agents/skills` root, so each of those
names appears once.

`setup-huguesstack`'s description is rendered whole (130 of 130 characters).
**`hugues-mode`'s is cut: 243 of its 312 characters are rendered**, ending at
"...or any mobile tas". The clause that names the mobile domains (`Swift/iOS,
Kotlin/Android, KMP, CMP, simulator or emulator proof`) is not in what Codex
shows the model. The previous version of this receipt said both entries carried
their exact descriptions; that was wrong for `hugues-mode`.

**State: OBSERVED.** `disable-model-invocation: true` (mirrored to Codex as
`allow_implicit_invocation: false`) removes a skill's description from Codex's
rendered prompt input, not only from Claude's. This answers Issue user story 15
for this Codex version at the render level. The extracted block has the same
SHA-256 as the one extracted in the previous round, which fits unchanged
descriptions under an unchanged Codex version.

## Codex: no live exec

`codex exec` was not run; the task authority withholds it. The first round's one
approved live-exec corroboration is not reasserted here.

## Cells

| Cell | Host | State |
|---|---|---|
| Skill count, no plugin (63 attached) | Claude Code 2.1.293 | OBSERVED |
| Skill count, plugin loaded (65 attached, +2) | Claude Code 2.1.293 | OBSERVED |
| Names of the two attached skills | Claude Code 2.1.293 | NOT OBSERVED (log has counts only) |
| Router description as the model sees it in the list | Claude Code 2.1.293 | NOT OBSERVED |
| Typed `/hugues-stack:tdd` runs the skill, with control | Claude Code 2.1.293 | OBSERVED |
| Skills block lists only the two model-invocable skills | Codex 0.161.0 | OBSERVED |
| Router description rendered whole | Codex 0.161.0 | OBSERVED: cut at 243 of 312 characters |
| Typed `$name` invocation of a disabled skill | Codex 0.161.0 | NOT RUN |
| Live model turn (`codex exec`) | Codex 0.161.0 | NOT RUN (withheld) |
| Install through Codex's plugin or marketplace mechanism | Codex 0.161.0 | NOT RUN |
| Router fires on a task, or stays quiet on a casual one | both | NOT RUN (PR 2's eval) |
| Mobile device, build or simulator proof | both | NOT RUN |

## Evidence

Each artifact is private, kept outside this repository; only its SHA-256 is
recorded here.

| Artifact | SHA-256 |
|---|---|
| Debug log, run 1 (without huguesStack) | `0966ab8fad8bcf685054a42f3c966e404de7a39503e20d030d76fb0b9768d464` |
| Stdout, run 1 | `e12c759830c2d48901ac4a4d7729fc218d96f1eb8f4a418a0634f732ad6492f0` |
| Debug log, run 2 (with huguesStack) | `d010258510784d64fa544a85ad14bf14166fdb6136e18570c4d2707a438e842d` |
| Stdout, run 2 | `e12c759830c2d48901ac4a4d7729fc218d96f1eb8f4a418a0634f732ad6492f0` |
| Debug log, run 3 (typed `tdd`) | `e2901681b9cfba874e6ac02bc008a1a181ad76c202759a1759d4ebff16c2dd98` |
| Stdout, run 3 | `4bbd455e508e13fb05a1605a4a3a96613797f37e2216fec215753133d4e9ef05` |
| Stderr, run 3 (SessionEnd hook line) | `915a68c1e6ea35650afb3c7a25119e9b3600a54679a96c65755d10f777e35788` |
| Debug log, run 4 (control) | `6a9a1c9fca567af8c642ac6533b222dbaff5d7ef54fa959210b5e5b62960cdc2` |
| Stdout, run 4 | `e368b5ae08209bc458801c9a29b948787feae8da923bf1fc5fe1e566122ab916` |
| Codex `prompt-input` raw JSON | `6d6d236f24f1f5a22f696af93b6de7bd837e8684dced3c9dbe860a65932a301e` |
| Codex `prompt-input` stderr (empty; so are the stderr files of runs 1, 2 and 4) | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| Extracted `skills_instructions` block | `e4b5598a93758d0363671d3358c933e4a85c9d53d371aa041d4102b7c95eb5e4` |

## Gaps

Codex installation through its own plugin or marketplace mechanism, a native
Codex `$name` invocation of a disabled skill and any live Codex model turn
remain unrun. Codex's cut of the router description (above) is a finding this
receipt does not resolve, and whether Claude Code cuts that description too is
unobserved, because the model-visible list was not read there. No mobile
device, build or simulator proof is implied. This receipt covers the host
skill-list and typed-invocation claims behind Issue user stories 1, 2 (Codex
only), 3, 14 and 15 (both at the render level), and 28. It says nothing about
whether the router fires.
