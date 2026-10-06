# Refactoring

source: Adapted from pstack 0.15.9 at `e43c7ee26e0038c6c1fa8380dd34ce86ff94cb2a`, `pstack/skills/poteto-mode/playbooks/refactoring.md`; MIT notice in PSTACK-LICENSE.

Own the behavior contract. Structural work preserves that contract; a discovered feature or bug becomes a separate task.

## Steps

1. Read [how](../../how/SKILL.md) in full and ground the subsystem. Pin existing behavior with a characterization test, snapshot or equivalence check before structural edits; type checking and lint alone do not pin behavior. Establish consumer authority and the [mobile lane](../references/mobile-lanes.md).
2. Name the missing structure and the invalid states or branches the new shape removes. Keep already clear local code; make reduced reader load the success criterion.
3. State the target module layout, types and call graph. For a shape across a function boundary, read [architect](../../architect/SKILL.md) in full and complete its design-only grounding and synthesis. For a wide or shared-API reshape, read [blast-radius](../../blast-radius/SKILL.md) in full, trace downstream callers and identify the falsifiable safety check before briefing implementation; preserve unproven facts when execution is blocked.
4. Brief a fresh implementation subagent to subtract dead code, redundant checks and one-caller wrappers before the reshape, within the owned files and pinned contract. Revert speculative cleanup unsupported by the goal; the worker owns the diff directly and does not recursively delegate.
5. Move in small steps with the behavior pin green. Migrate every affected caller and remove the old API in the same wave; inspect strings, documentation and back-references as well as symbols. Use a fresh worker for every new implementation round.
6. Inspect the diff and reproduce equivalence yourself on the actual artifact through [mobile proof](mobile-proof.md). Account for all affected targets and callers; compilation alone proves no behavior claim.
7. Obtain an independent fresh review of contract preservation and reader load. Resolve findings and repeat coordinator proof after corrections; discard a reshape that does not improve reader load.
8. Prepare ordered local commits when authorized, then [opening a PR](opening-a-pr.md). Keep newly discovered behavior changes outside this refactor's scope.

**Reply:** structural change, pinned contract, equivalence evidence, reader-load improvement and gaps.
