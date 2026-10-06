# Bug fix

source: Adapted from pstack 0.15.9 at `e43c7ee26e0038c6c1fa8380dd34ce86ff94cb2a`, `pstack/skills/poteto-mode/playbooks/bug-fix.md`; MIT notice in PSTACK-LICENSE.

Own the cause and the proof. Delegate the fix; keep only changes supported by the observed mechanism.

## Steps

1. Establish the authorized consumer checkout, domain and original failing path using [mobile lanes](../references/mobile-lanes.md). Reproduce on that path before edits and preserve the failing observation. If execution is not authorized or the runtime is unavailable, report the exact blocker rather than infer a reproduction.
2. Read [how](../../how/SKILL.md) and [why](../../why/SKILL.md) in full for the affected subsystem and regression history. Form hypotheses and eliminate them with runtime evidence; use scoped instrumentation only within edit authority. Continue until one mechanism explains the original observation, or report why the cause remains unresolved.
3. Design the smallest supported fix. For changes across a function boundary, read [architect](../../architect/SKILL.md) in full and complete its design-only grounding and synthesis before implementation. Read [tdd](../../tdd/SKILL.md) in full: when a cheap local seam exists, brief a fresh scoped regression-test worker to write only the focused test, then independently run that regression against unfixed production code and preserve observed RED before briefing a separate fresh production implementation subagent. A passing check or unrelated build failure is not RED. For an impractical seam, record its reason and preserve the original runtime failing observation. Brief the worker with the cause, design, owned files, regression and proof lane; each new fix round gets a fresh subagent. The worker owns its diff directly and does not recursively delegate.
4. Inspect the actual diff and reproduce the original path yourself on the same target. Run the lane's build, relevant tests and runtime check through [mobile proof](mobile-proof.md). Treat inconclusive, flaky, skipped or wrong-target results as their actual outcomes.
5. Preserve the [tdd](../../tdd/SKILL.md) RED evidence from step 3 and run the same regression after the fix for GREEN; inspect actual assertions, skips and retries. Keep the original runtime failing and passing observations separate. Order regression-before-fix local commits when commits are authorized; retain the impractical-seam reason when no focused test was added.
6. Obtain an independent fresh review from a subagent that did not implement the change, or the other host when separately available and authorized. Adjudicate findings; return any required fix to a fresh implementer and repeat coordinator proof before [opening a PR](opening-a-pr.md).

**Reply:** broken behavior, supported cause, fix, original failing and final passing observations, evidence paths and gaps.
