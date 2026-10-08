# huguesStack

huguesStack is pstack for mobile development, running in Claude Code and Codex.
pstack is poteto's Cursor plugin: a router mode matches a task to a playbook,
the playbook calls skills and principles as its steps fire, and the work ends in
evidence. huguesStack keeps pstack 0.15.9 *pinned* byte-for-byte and adds host
and mobile adapters for Swift/iOS, Kotlin/Android, Kotlin Multiplatform (KMP)
and Compose Multiplatform (CMP). Its router is `hugues-mode` (pstack's
`poteto-mode`). Read the [pstack guide](plugin/core/pstack/docs/guide/README.md)
for how pstack works and the [glossary](docs/GLOSSARY.md) for project terms.

This repository ships only the plugin. Agents working inside *consumer* apps,
the mobile projects that install huguesStack, load everything under `plugin/`,
so write it for them. Rules for maintaining huguesStack itself live here and in
`docs/`.

## Where an edit goes

- `plugin/core/pstack/` is the *pinned* core: 161 files whose bytes and Git
  modes the checks verify. It changes only in a pin upgrade, which is its own
  task ([upstream sync](docs/upstream/README.md)).
- *Generated*: every `plugin/skills/*/SKILL.md`, the playbooks in
  `plugin/skills/hugues-mode/playbooks/` that `plugin/core-bindings.json` names,
  and `plugin/agents/`. Change `scripts/render_core.py` or the bindings, then run
  `python3 scripts/render_core.py`.
- Everything else under `plugin/` is *authored*: adapters, the Astra policy, the
  mobile playbooks and the `hugues-mode` references. Many authored files have
  their SHA-256 recorded in a *receipt*; after editing one, run
  `grep -rl --include='*.json' '<path>' docs` and update any hash it finds in
  the same commit.

## Checks

Run every command in [Reference and maintenance](README.md#reference-and-maintenance)
from inside your worktree before each commit; all must pass. Adding or removing
a test changes the counts quoted in [test accounting](docs/TEST-COVERAGE.md) and
[core restoration](docs/CORE-RESTORATION.md). No check catches stale counts, so
update them in the same commit.

Static checks prove source and wiring only. A claim about host or mobile
behavior in docs, release notes or a PR body needs *observed* evidence from that
host, domain and target. Write anything unobserved as a gap.

## Worktrees and branches

Every task that edits files runs in its own worktree on its own branch: one
worktree, one branch, one writer. The primary checkout stays on `main` as the
clean base everyone branches from. Read-only tasks stay where they are.

1. **Check where you are.**

   ```sh
   git rev-parse --path-format=absolute --git-dir --git-common-dir
   git branch --show-current
   ```

   Two different paths mean you are in a linked worktree, often one your host
   made: keep it and its branch. If the branch line is empty (detached HEAD),
   run `git switch -c <branch>` there, named per step 2, before the first edit.
   Two equal paths mean the primary checkout: continue.
2. **Name the branch** `fix/<slug>` for a defect fix and `feat/<slug>` for
   everything else, with a short kebab-case slug: `fix/plan-check-spaces`,
   `feat/android-proof-lane`.
3. **Create the worktree beside the repository**, at `<repo>.worktrees/<branch>`.
   `scripts/check_plugin.py` walks every file under the repository root, so a
   worktree inside it (`.worktrees/`, `.claude/worktrees/`) makes
   `check-plugin.sh` fail in the primary checkout.

   ```sh
   root=$(dirname "$(git rev-parse --path-format=absolute --git-common-dir)")
   git fetch origin
   git worktree add --no-track -b feat/<slug> "$root.worktrees/feat/<slug>" origin/main
   ```

   `--no-track` keeps `origin/main` from becoming the branch's upstream; the
   first push sets the real one with `git push -u origin <branch>`. If the
   branch already exists, `git worktree list` shows whether a worktree holds it:
   enter that one, or else run `git worktree add "$root.worktrees/<branch>" <branch>`.
4. **Move in.** `cd` into the worktree, or use the host's enter-worktree tool,
   and run every later command, edit and check from there. Done when
   `git worktree list` shows your path on your branch and `git status` there is
   clean. Report the path, branch and base commit.

Parallel writers (arena candidates, swarm workers, subagents that edit) each get
their own worktree the same way, on branch `<your-branch>-<n>` based on your
branch's HEAD instead of `origin/main`. Commits go on the worktree's own branch.

`docs/planning/` is gitignored, so it exists only in the primary checkout; read
it there by absolute path. It and the local `private/planning-snapshots` branch
hold the owner's private planning and stay on this machine.

After the owner merges, clean up with `git worktree remove <path>`, then
`git branch -d <branch>`. Both refuse when work would be lost; on a refusal,
stop and report it to the owner.

## Publishing

Pushing, opening a PR, merging and releasing each need the owner's go-ahead for
the current task. For PR-bound changes, read and apply
[the project Astra High review policy](plugin/policies/astra-pr-review.md). This
file activates that policy for this repository only; installing the plugin does
not impose it on consumer projects.
