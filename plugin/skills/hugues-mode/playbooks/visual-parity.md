# Visual parity

source: Adapted from pstack 0.15.9 at `e43c7ee26e0038c6c1fa8380dd34ce86ff94cb2a`, `pstack/skills/poteto-mode/playbooks/visual-parity.md`; MIT notice in PSTACK-LICENSE.

Own pixel equivalence. The captured baseline is the spec.

## Steps

1. Establish authorized consumer scope and [mobile lanes](../references/mobile-lanes.md). Capture the unchanged baseline and target across the relevant states, fixing device, viewport, theme, font scale and capture conditions. Finish when the images and harness are preserved outside the plugin; no baseline means no parity claim.
2. Pin the baseline and harness against changes made to obtain a pass. If the baseline itself is disputed, stop for that decision before migration; preserve the original images.
3. Brief a fresh implementation subagent for one component or safe batch with owned paths, baseline states and success criteria. Migrate shared primitives before their callers and use disjoint paths for independent work; workers own diffs directly and do not recursively delegate.
4. Inspect the diff and compare screenshots yourself with image diff on the same target and conditions. A nonzero diff fails pixel parity; diagnose the delta and give each correction round to a fresh worker. Record runtime interaction and accessibility observations separately from pixel equivalence.
5. Obtain an independent fresh review of the untouched baseline, harness and target comparisons. Resolve findings and run [opening a PR](opening-a-pr.md) per component or safe batch with each comparison's result.

**Reply:** components, per-target image-diff results, baseline and harness paths, unresolved deltas and remaining scope.
