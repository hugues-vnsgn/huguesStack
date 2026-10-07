# worktree-cleanup

Read [host adapter](../../../adapters/host.md),
[mobile adapter](../../../adapters/mobile.md), then the
[pinned worktree-cleanup playbook](../../../core/pstack/skills/poteto-mode/playbooks/worktree-cleanup.md) in full.
Copy its ordered todos verbatim before execution. Keep skips with their reasons.
The pinned source owns the steps; the adapters translate host mechanics and add
applicable mobile proof. Missing capability blocks the gate, not its existence.

For step 1 execute the [native activity audit](../../../adapters/host-tools.md)
through `host_tools.py worktree-audit` with the saved binding, consumer repo and
explicit authorized source manifest. Unavailable coverage holds candidates.
The separate active/pinned-chat gate is required; the helper never deletes.
