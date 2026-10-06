---
name: blast-radius
description: "Find downstream breakages beyond a mobile diff and run a falsifiable check of the fact its safety depends on."
disable-model-invocation: true
source: pstack/skills/blast-radius/SKILL.md
---

# Blast radius

Find what a change breaks somewhere else before it ships. Callers found by search are the starting point. Follow unexpected effects beyond them. Read this file directly when a playbook needs it.

## Steps

1. Read the exact diff and changed, added and deleted symbols, including behavior the diff leaves implicit. Read [how](../how/SKILL.md) for runtime flow and [why](../why/SKILL.md) step 2 for commits and PR context. Use their actual host adapter and direct-reading path. If a dependency or history tool is unavailable, read the relevant source and available local history directly, record the missing coverage and preserve uncertainty. Establish the consumer, targets and current authority under [mode authority](../hugues-mode/SKILL.md#authority).
2. Find the one or two facts the change's safety depends on. State a concrete proposition whose failure would expose a real breakage. Select the cheapest check capable of falsifying it; a plausible writeup alone establishes nothing.
3. Look where symbol search stops. Read the called library's source at its pinned version and local patches. Follow JSON, storage migrations, wire formats, flags and consumers several calls downstream. For mobile changes, follow Swift/Kotlin callers across exported KMP APIs, serialization, nullability, ownership, cancellation, threading, lifecycle and teardown. Trace when callbacks run and which target owns state; shared source does not prove equal native behavior. Read [mobile lanes](../hugues-mode/references/mobile-lanes.md) to select all affected targets.
4. Record confirmed risks with a real `file:line`, the failure mechanism, likelihood, impact and cheapest check. Record checked-and-cleared risks separately with their evidence. An empty search is evidence of that search's scope, not proof no caller exists. Label inferred history and unproven safety; invent neither callers nor APIs.
5. Write and run a small script or focused test that calls the actual production function or the same pinned library the app ships. Assert literal behavior and fail loudly if the safety fact is wrong. Use the appropriate Swift Testing/XCTest, Kotlin/JUnit or KMP test seam, and inspect assertions and per-target reports. When runtime behavior is decisive, reproduce it in the running app within authority. Read the [evidence guide](../hugues-mode/references/evidence-guide.md) and [jev Drive](../hugues-mode/references/jev-drive.md) for screen proof. Preserve command/tool arguments, stdout, stderr, exit/result, artifact identity and observed values. Missing permitted execution leaves the safety fact unproven; finish available source checks and report the blocker.
6. For a big or wide change, read [arena](../arena/SKILL.md) and run its candidates, cross-judge and synthesis within current scope, using [host notes](../hugues-mode/references/host-notes.md). Compare several models only when the actual host and explicit model authority support them; otherwise disclose inherited-model process independence. Missing arena, delegation or model capability is a gap, not a successful arena. Verify the merged findings against real code.

## Proof level

For each safety fact, reach the strongest level that is cheap and authorized. Say where you stopped.

1. Assertion in prose, unproven.
2. Real source line or the library's own source.
3. Failure traced step by step and shown unreachable.
4. Script or test ran real code and would fail if the fact were false.
5. Reproduction in the running app.

## Reply

Report what changed, the safety fact and its proof level, risks, cleared cases and the cheapest pre-merge regression command or reproduction. Paste decisive observed output and link the retained proof. Mark a fact unproven when execution could not establish it. Apply the available owner `unslop` skill to the writeup, or disclose its absence and edit the prose directly. Strip private material before any separately authorized public publication.
