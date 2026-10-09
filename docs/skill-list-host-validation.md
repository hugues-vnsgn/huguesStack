# Skill-list host validation

This receipt binds the Issue #21 host observations to one commit. Fix round 4
(9 October 2026) reran every observation against code commit
`ae51493d009aa04c608160f027e980deba6fe87d`, tree
`28675e006a4a70b0a6278739a50617c77878627c`, branch `feat/skill-list-budget`,
from a worktree whose `git status --short` printed nothing at the start of the
run (the script below prints it first). The commit that carries this receipt
changes documentation only; `git diff ae51493 HEAD -- plugin` is empty. Nothing
here carries over from an earlier round: the receipts for `2559b5d` and
`6a6f31d` are superseded and their artifacts are not reused.

The five host commands below, run once by one script, wrote new files into an
evidence folder created for this round. Each exited 0 and none was repeated or
aborted, so no artifact holds a session from an earlier round. No consumer app
was edited or executed. No host configuration file was edited and nothing was
installed: Claude Code loaded the plugin with `--plugin-dir` for one session at
a time and wrote no session transcript (`--no-session-persistence`); Codex read
a project-local `.agents/skills` link inside a scratch directory. Each host's
own routine state writes are not audited here. Raw logs stay private, outside
this repository; this receipt records their SHA-256 and the per-cell states,
not their contents.

## Commands

Claude Code `2.1.293`, model `claude-sonnet-5-5` (the debug logs name it);
Codex CLI `0.161.0`. `<root>` stands for the machine-specific folder that holds
`huguesStack.worktrees`; every folder name below it is the real one. Claude runs
started in `scratch-claude`, the Codex run in `scratch-codex`, both inside the
evidence folder.

The script was saved as `run-host-validation.sh` in the evidence folder and run
there as `sh ./run-host-validation.sh <root> > run-host-validation.out.txt 2>&1`
(exit 0). `claude` and `codex` were the installed CLIs. `date -u` writes the
`.started` file of each run. The `extract.py` that the script calls is printed
after it.

```sh
#!/bin/sh
set -u
W="$1/huguesStack.worktrees/feat/skill-list-budget"
E="$1/huguesStack.worktrees/_evidence/skill-list-budget/round-4"
PROMPT_ACK='Reply with the single word ACK and nothing else.'
PROMPT_TDD='/hugues-stack:tdd Quote one exact sentence from the instructions this skill gave you, verbatim, inside double quotes, then stop. Do not write or run anything else.'

git -C "$W" rev-parse HEAD
git -C "$W" status --short
mkdir -p "$E/scratch-claude" "$E/scratch-codex/.agents"

# 1. Without huguesStack
date -u +%Y-%m-%dT%H:%M:%SZ > "$E/claude-without-plugin.started"
(cd "$E/scratch-claude" && claude -p "$PROMPT_ACK" \
  --model claude-sonnet-5-5 --no-session-persistence \
  --debug-file "$E/claude-without-plugin.debug.log" \
  > "$E/claude-without-plugin.stdout.log" 2> "$E/claude-without-plugin.stderr.log"); echo "run 1 exit $?"

# 2. With huguesStack
date -u +%Y-%m-%dT%H:%M:%SZ > "$E/claude-with-plugin.started"
(cd "$E/scratch-claude" && claude -p "$PROMPT_ACK" \
  --model claude-sonnet-5-5 --no-session-persistence --plugin-dir "$W/plugin" \
  --debug-file "$E/claude-with-plugin.debug.log" \
  > "$E/claude-with-plugin.stdout.log" 2> "$E/claude-with-plugin.stderr.log"); echo "run 2 exit $?"

# 3. Typed invocation of a user-only skill
date -u +%Y-%m-%dT%H:%M:%SZ > "$E/claude-by-name-tdd.started"
(cd "$E/scratch-claude" && claude -p "$PROMPT_TDD" \
  --model claude-sonnet-5-5 --no-session-persistence --plugin-dir "$W/plugin" \
  --debug-file "$E/claude-by-name-tdd.debug.log" \
  > "$E/claude-by-name-tdd.stdout.log" 2> "$E/claude-by-name-tdd.stderr.log"); echo "run 3 exit $?"

# 4. Control for 3: the same prompt, no --plugin-dir
date -u +%Y-%m-%dT%H:%M:%SZ > "$E/claude-by-name-tdd-control-without-plugin.started"
(cd "$E/scratch-claude" && claude -p "$PROMPT_TDD" \
  --model claude-sonnet-5-5 --no-session-persistence \
  --debug-file "$E/claude-by-name-tdd-control-without-plugin.debug.log" \
  > "$E/claude-by-name-tdd-control-without-plugin.stdout.log" \
  2> "$E/claude-by-name-tdd-control-without-plugin.stderr.log"); echo "run 4 exit $?"

# 5. Codex: render the model-visible prompt input (local; no request to OpenAI)
ln -s "$W/plugin/skills" "$E/scratch-codex/.agents/skills"
date -u +%Y-%m-%dT%H:%M:%SZ > "$E/codex-prompt-input.started"
(cd "$E/scratch-codex" && codex debug prompt-input "$PROMPT_ACK") \
  > "$E/codex-prompt-input.raw.json" 2> "$E/codex-prompt-input.stderr.log"; echo "run 5 exit $?"

# Read-only checks
python3 -I "$E/extract.py" "$E/codex-prompt-input.raw.json" "$W/plugin/skills" \
  "$E/codex-skills-instructions-block.txt"; echo "extract exit $?"
grep -F -n 'Do not force a test when it would be impractical.' "$W/plugin/skills/tdd/SKILL.md"; echo "grep exit $?"
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

Claude Code's `--debug-file` also left a `latest` symlink in the evidence folder,
pointing at the last log it wrote. It was deleted after the runs and carries no
evidence.

## Claude Code: skill count with and without huguesStack

Runs 1 and 2, started 2026-10-09T01:42:40Z and 01:42:45Z.

- Without huguesStack, the debug log says `getSkills returning: 65 skill dir
  commands, 20 plugin skills, 39 bundled skills, 1 builtin plugin skills`, then
  `Sending 63 skills via attachment (initial)`.
- With `--plugin-dir`, it says `Loaded 50 skills from plugin hugues-stack
  default directory`, then `getSkills returning: 65 skill dir commands, 70
  plugin skills, 39 bundled skills, 1 builtin plugin skills`, then `Sending 65
  skills via attachment (initial)`.

**State: OBSERVED (counts).** The attached list grows by exactly **2** (63 to
65), the number of model-invocable skills in the source (`hugues-mode`,
`setup-huguesstack`); all 50 directories load. The log carries counts, not
names, so two things are inferred from that arithmetic and not observed: that
the two attached skills are `hugues-mode` and `setup-huguesstack`, and that the
other 48 are not attached. Both replies were `ACK`. This observes the count half
of Issue user stories 1 and 28.

## Claude Code: typed invocation of a user-only skill

Runs 3 and 4, started 01:42:49Z and 01:42:54Z. `tdd` is user-only
(`disable-model-invocation: true`), so it is not one of the two attached skills.
It is not a `principle-*` skill (see the gaps).

With the plugin, the reply was exactly: `"Do not force a test when it would be
impractical."` Line 17 of `plugin/skills/tdd/SKILL.md` begins with that
sentence. The `grep -F` above finds it once, verbatim, at line 17. That checked
sentence is the only quote this receipt takes from the file.

Without the plugin (the control), the same prompt produced no skill text: the
model said `/hugues-stack:tdd` "isn't available in this session, so it didn't
run" and that a plain `/tdd` skill is installed but is a different command,
which is the owner's personal one.

**State: OBSERVED**, with a control. Typing a user-only skill by its namespaced
name still runs it. This closes the typed-invocation half of Issue user stories
3 and 28 for `tdd` only. The stderr files of all four Claude runs are empty.

## Codex: prompt-input skills block

Run 5, started 01:42:59Z. `codex debug prompt-input` renders the model-visible
prompt input locally. It ran from a scratch directory outside the repository
that held only a project-local `.agents/skills` link to `<worktree>/plugin/skills`.

The rendered `skills_instructions` block has 8 skill roots and **77** skill
entries: 85 bullet lines, which include the 8 root lines. Exactly two entries
come from the huguesStack root: `hugues-stack:hugues-mode` and
`hugues-stack:setup-huguesstack`. The other 48 skill directories under that root
have no entry. The only same-named entries in the block (`recall`, `tdd`,
`unslop`) come from the owner's own `~/.agents/skills` root, so each of those
names appears once.

`setup-huguesstack`'s description is rendered whole (130 of 130 characters).
**`hugues-mode`'s is cut: 243 of its 312 characters are rendered**, ending at
"...or any mobile tas". The clause that names the mobile domains (`Swift/iOS,
Kotlin/Android, KMP, CMP, simulator or emulator proof`) is not in what Codex
shows the model. That is a finding about the approved router description, not
resolved here.

**State: OBSERVED.** In Codex's rendered prompt input, a skill with
`disable-model-invocation: true` (mirrored to Codex as
`allow_implicit_invocation: false`) has no entry: 48 of the 50 skills are absent
from the block. That answers Issue user story 15 for this Codex version at the
render level. The Claude Code half is not observed the same way: no Claude
listing was read, and the removal there is inferred from the counts above. The
extracted block has the same SHA-256 as round 3's, which fits unchanged
descriptions under an unchanged Codex version.

## Codex: no live exec

`codex exec` was not run; the task authority withholds it. The first round's one
approved live-exec corroboration is not reasserted here.

## Cells

| Cell | Host | State |
|---|---|---|
| Skill count, no plugin (63 attached) | Claude Code 2.1.293 | OBSERVED |
| Skill count, plugin loaded (65 attached, +2) | Claude Code 2.1.293 | OBSERVED |
| Names of the two attached skills; the other 48 absent | Claude Code 2.1.293 | NOT OBSERVED (inferred from counts) |
| Router description as the model sees it in the list | Claude Code 2.1.293 | NOT OBSERVED |
| Typed `/hugues-stack:tdd` runs the skill, with control | Claude Code 2.1.293 | OBSERVED |
| A `principle-*` skill typed by name runs it | Claude Code 2.1.293 | NOT OBSERVED |
| A `principle-*` skill is absent from the model's list | Claude Code 2.1.293 | NOT OBSERVED (inferred from counts) |
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
| Debug log, run 1 (without huguesStack) | `c6408eebfd45f2e6f3ef0d7b09af8521001ab51a906046e03fffb843b3346700` |
| Stdout, run 1 | `e12c759830c2d48901ac4a4d7729fc218d96f1eb8f4a418a0634f732ad6492f0` |
| Debug log, run 2 (with huguesStack) | `346c47031d256e91ca4a87a506e7beb261094aa76a2985e22c690771e46cfbbe` |
| Stdout, run 2 | `e12c759830c2d48901ac4a4d7729fc218d96f1eb8f4a418a0634f732ad6492f0` |
| Debug log, run 3 (typed `tdd`) | `87156f21d2d09fc3bb378d97780a2c509ed1b2615c0682a851a23ed62ac2543b` |
| Stdout, run 3 | `4bbd455e508e13fb05a1605a4a3a96613797f37e2216fec215753133d4e9ef05` |
| Debug log, run 4 (control) | `fa25e8a438eb2e23011ec732b24cabd47a1c60ea7c61edebe0539bcd13811766` |
| Stdout, run 4 | `e27d2da7f0ad02279bd55d4143e15ba952e9c2a22301dbf4f2d5070ebe7eb5b2` |
| Codex `prompt-input` raw JSON | `08f054803bf0f31227fe701b487de4b3ddbc384b49de8f5e30cfac793f7d16e0` |
| Extracted `skills_instructions` block | `e4b5598a93758d0363671d3358c933e4a85c9d53d371aa041d4102b7c95eb5e4` |
| Empty stderr files (runs 1 to 5, five files) | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `run-host-validation.sh` | `e4dd2dcd82ea8aa8f0b17bf7707f5088587b4b413f5986528523768a64cd0fc1` |
| `extract.py` | `40f870754982124a512beca60373ebd274564ca2388eed897f865c15d3e08c3c` |
| `run-host-validation.out.txt` (the script's printed output) | `e6824c291ef3f1bfac8f9dee607c6f247ab9d2afff525c75a492f2098e82e285` |
| `lint-red-before-fix.txt` (round 3's lint against the ten new corpus rows: all ten missed) | `ab88aca734ad960456860f9471d7c7c2e3f4d6cca2cc5a0266af55ac1cdab745` |

## Gaps

Two cells the Issue asked for remain unobserved. The first is `hugues-mode`'s
description in Claude's list: the debug log carries skill counts, not text, so
whether Claude Code shows the 312-character description whole or cuts it, as
Codex does, is unknown. The second is a `principle-*` skill typed by name: run 3
typed `tdd`, which is user-only but not a principle, so the principles' typed
path is unobserved. The absence of a principle from Claude's list is inferred
from the counts, not seen.

Codex installation through its own plugin or marketplace mechanism, a native
Codex `$name` invocation of a disabled skill and any live Codex model turn
remain unrun. Codex's cut of the router description is a finding this receipt
does not resolve. No mobile device, build or simulator proof is implied. This
receipt covers the host skill-list and typed-invocation claims behind Issue user
stories 1, 2 (Codex only), 3 (for `tdd`), 14 and 15 (both at the render level),
and 28 (counts, for `tdd`). It says nothing about whether the router fires.

## Addendum: the reordered router description on Codex

9 October 2026, PR 2 fix round 1. The owner chose a reordered router description,
236 characters with the mobile clause first, to fit inside Codex's cut. This section
reruns run 5 only, the local Codex render, against the tree that the commit carrying
this section holds. That commit cannot name its own SHA, so the tested code is named
by its `plugin/` tree, `d08484abd8fbc16780ac9d75766ac50bcd64dfaf`, which
`git rev-parse <that commit>:plugin` returns. The script printed `HEAD` as
`f9368f8e7d23c3df4c98517407fed88b816af368`, the commit under it, and a dirty
`git status --short`: the fix round was uncommitted during the render. Codex CLI
`0.161.0`, started 2026-10-09T02:34:50Z, from a scratch directory outside the
repository that held only a project-local `.agents/skills` link to
`<worktree>/plugin/skills`, as in run 5. The render command exited 0 with an empty
stderr. Claude Code was not run, `codex exec` was not run, and no routing eval ran.
The command was `codex debug prompt-input 'Reply with the single word ACK and nothing
else.'`, then `extract-quoted.py` over its output.

The block has 8 skill roots and 77 skill entries, as in run 5. Two entries come from
the huguesStack root. **`hugues-mode`'s description is rendered whole: 236 of 236
characters**, ending at "...long autonomous run." `setup-huguesstack`'s is whole too
(130 of 130), so the two descriptions in the skill list total 366 characters. The
mobile clause (`Swift/iOS, Kotlin/Android, KMP, CMP, simulator or emulator proof`)
now sits inside what Codex shows the model. This replaces the "cut at 243 of 312" cell
above for the description now in the tree; the cell above stays as recorded for
`ae51493`.

The frontmatter holds the description in double quotes. Unquoted, its `work: bug fix`
reads as a YAML mapping indicator, and PyYAML 6.0.3 rejects the line with "mapping
values are not allowed here". Codex accepted both forms: a second render of a scratch
copy with the unquoted line also showed 236 of 236 characters. The scratch copy is
evidence only and is not in the tree. Whether Claude Code reads either form is
unobserved, which is why the tree keeps the form every YAML parser accepts. Many
other skills in this tree quote their descriptions.

| Cell | Host | State |
|---|---|---|
| Router description rendered whole (236 of 236) | Codex 0.161.0 | OBSERVED |
| Router description rendered whole, unquoted scratch copy | Codex 0.161.0 | OBSERVED (not the tree) |
| Router description as the model sees it in the list | Claude Code | NOT OBSERVED |
| Claude Code's parse of the quoted description | Claude Code | NOT OBSERVED |

| Artifact | SHA-256 |
|---|---|
| `codex-prompt-input.raw.json` (tree render) | `d628fefb86ef47db50332a88de12e9eeeb186b1a942e07ae42df6c65dcc9692a` |
| `codex-skills-instructions-block.txt` (tree render) | `946908a4284eb050fa1841219318686bc9b71bbbff0ce56dd4ab12d2e6d0c57f` |
| `run-render.sh` | `0e9e6bc3a2c489aae338f85a5436d6d7472e95198be683cf98dbe5547a4dc972` |
| `extract-quoted.py` (run 5's `extract.py`, comparing against the YAML-parsed description) | `a24a8b6964e3ab591f21c5dff3828f370e275f0fcc431545b51f297b734c54a9` |
| `run-render.out.txt` (the script's printed output) | `805fd76170b8dcc160b54c439e2627ffb569a2742f32eca02fa9e45b3e8f4418` |
| `codex-prompt-input.raw.json` (unquoted scratch copy) | `0215d0f673ff7f0f294d20dbe0c3105d87863ebc7070349c862fdeac1295935d` |
| `codex-skills-instructions-block.txt` (unquoted scratch copy) | `fd1b4e60ed37696b274e0064e69e547445680e8815fa513db9abe117b44c6df8` |
| Empty stderr files (both renders, two files) | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
