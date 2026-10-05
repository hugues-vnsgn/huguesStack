# PR review policy

For new huguesStack PR reviews and re-reviews, use an independent **GPT-6 Astra
reviewer with High effort**, as requested by the owner on 5 October 2026. Keep
past Claude Fable and Opus receipts unchanged. Claude host compatibility probes
still use Claude; this preference changes PR reviewing only. Implementation
workers continue to inherit the parent model unless separately instructed.

## Reviewer handoff

Inspect the current host's delegation schema before starting a reviewer. The
available Codex delegation tool accepts `model: "gpt-6-astra"` and
`reasoning_effort: "high"`. Use `fork_turns: "none"` with those overrides and
supply a complete scoped prompt; full-history forks do not accept overrides.
Treat these as verified settings for that tool, not a guessed Codex CLI alias
or a promise that another host supports them. A Claude-only Agent tool cannot
select Astra natively; use a verified delegation path only when the current
request authorizes it, otherwise report the review as blocked. If the required model or effort
is unavailable or rejected, report the exact review blocker and the smallest
decision needed. Do not silently substitute another model or return to Fable.

Give a fresh reviewer the exact base and candidate commit, intended behavior,
diff, surrounding context, rubric and existing check receipts. Require read-only
inspection: no edits, installs, consumer execution, publication or remote
messages. If using [interrogate](../../interrogate/SKILL.md), keep its two-reviewer
and adjudication requirements; apply these settings to both reviewers. State
process independence for fresh same-host reviewers. A cross-host claim requires
an actual review in the other host, not a different model name.

## Review and repair

1. Complete coordinator checks and review the exact candidate head.
2. Adjudicate every finding against the actual code and intent. Record fixes,
   accepted tradeoffs and dismissals with reasons; preserve access limits.
3. Apply authorized fixes, run affected checks and the full package checks, and
   commit the resulting candidate. Start a fresh Astra High re-review against
   that exact final head. Repeat when new findings require changes.
4. Before authorized draft publication, verify that the reviewed head still
   matches the local and remote candidate. A review of older bytes does not
   cover later edits. Publication and merging retain their own authority rules.

Record the base and reviewed commit, reviewer identity, requested and confirmed
model/effort, actual reviewing host, independence label, verdict, findings and
adjudications, check results and access limits. Preserve the invocation and
result receipt outside the plugin when it contains private evidence. Distinguish
an accepted launch from a completed review; if the host does not confirm a
setting or revision, state that limit instead of inventing confirmation.
