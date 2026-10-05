# Pause safely

source: Adapted from pstack 0.15.9 at `e43c7ee26e0038c6c1fa8380dd34ce86ff94cb2a`, `pstack/skills/poteto-mode/playbooks/pause-safely.md`; MIT notice in PSTACK-LICENSE.

Use only for an explicit pause. Leave a checkpoint a cold session can resume.

## Steps

1. Stop at an atomic boundary: finish the current safe unit or preserve its partial state. Start no new work and stop active delegates, retaining their known files and outcomes.
2. Keep the pause local. Take no new push, PR, merge or destructive cleanup action merely to stop; preserve unrelated user edits.
3. Make authorized work durable in a clear local `wip:` commit when local commits are permitted. If a commit is unavailable or includes unrelated changes, preserve the files and record the dirty state instead. State any broken checks explicitly.
4. Write a resume note outside the plugin with intent, authority, current branch and SHA, progress, verified evidence, pending todos, skipped reasons, next action, files and blockers. Point to an existing evidence trail instead of duplicating it.

**Reply:** checkpoint path, durable files or commit, tree state, active-worker outcome and first resume action.
