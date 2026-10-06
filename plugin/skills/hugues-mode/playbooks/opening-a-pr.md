# Opening a PR

source: Adapted from pstack 0.15.9 at `e43c7ee26e0038c6c1fa8380dd34ce86ff94cb2a`, `pstack/skills/poteto-mode/playbooks/opening-a-pr.md`; MIT notice in PSTACK-LICENSE.

Prepare a reviewable local change. Publication requires an explicit owner request; that request may already authorize the per-implementation draft PR workflow.

## Steps

1. Inspect branch, worktree, base and unrelated edits. Preserve existing user changes and choose an isolated branch or worktree when needed. For a big or wide change, read [blast-radius](../../blast-radius/SKILL.md) in full and complete its downstream analysis and authorized falsifiable check; mark unrun safety facts explicitly. Inspect the actual diff and tracked content/history for credentials, private paths and unintended artifacts before any authorized publication.
2. Complete the package's coordinator verification and independent fresh review under the [PR review policy](../references/pr-review-policy.md): use supported Astra High delegation settings, adjudicate findings, apply authorized fixes, run full package checks and obtain an exact-head re-review. Apply the owner's available `unslop` skill to the diff's prose. Keep ordered local commits when authorized; prepare final summaries against the actual current head.
3. Prepare a short Conventional Commit title and body with `## Why`, `## What changed`, `## Scope`, optional `## Tradeoffs`, `## Blast Radius` and `## Verification`. State actual run paths, outcomes, gaps and the requested review state. Keep raw evidence outside the plugin and link public-safe supporting artifacts only.
4. Resolve publication authority and destination. With no explicit push/open authorization, stop at local commits and the prepared body. Under the owner's per-change review request, open a separate draft PR; use an available built-in PR tool first, otherwise the repository's configured forge CLI. Verify repository and base rather than guessing or overwriting a remote.
5. For an authorized PR, verify the remote head, URL and draft status, and attach it to the task when the host supplies an attachment tool. Report the review-ready material and return; merge, reviewer messages and ongoing monitoring each require their own explicit authority.

**Reply:** local branch and commits, summary, exact tests, known gaps, prepared body path or verified draft PR URL.
