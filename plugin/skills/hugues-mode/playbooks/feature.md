# Feature

source: Adapted from pstack 0.15.9 at `e43c7ee26e0038c6c1fa8380dd34ce86ff94cb2a`, `pstack/skills/poteto-mode/playbooks/feature.md`; MIT notice in PSTACK-LICENSE.

Own the design and proof; delegate code-writing.

## Steps

1. Inspect the affected subsystem with the owner's available `how` skill or directly cited source. Pin the requested behavior, authorized files, domain and proof lane from [mobile lanes](../references/mobile-lanes.md).
2. Explore the design with the owner's available `architect` skill. When that skill is absent, record the gap and compare concrete alternatives before choosing the types, state machine or table that organizes the change.
3. Add four throughput todos: blocking first steps, independent workstreams, shared mutable state and smallest safe decomposition. Give each a concrete plan; retain a dimension that does not apply with `n/a: <reason>`. Separate writable paths before parallel work and serialize shared invariants.
4. Brief a fresh implementation subagent with owned paths, chosen shape, behavior and success criteria. When competing implementations are warranted, use an available `arena` skill or state that capability gap. Each new implementation round gets a fresh worker; workers own their diffs directly and do not recursively delegate.
5. Inspect the actual diff and run [mobile proof](mobile-proof.md) yourself against the matching target and installed artifact. Finish only when each required observation has an actual outcome or a named blocker.
6. Prepare small ordered local commits when authorized, keeping each coherent slice verifiable. Shared primitive changes require every affected caller and target to be accounted for.
7. Obtain an independent fresh review from a non-implementer or a separately available, authorized other host. Record the independence type, resolve findings, and send corrections to a fresh implementer before repeating coordinator verification.
8. Run [opening a PR](opening-a-pr.md) with the final scope and exact verification evidence.

**Reply:** behavior added, design choice, throughput checkpoint, proof, decisions and gaps.
