---
name: tdd
description: "Prove a mobile bug with a cheap focused regression check that fails before the fix and passes after it."
disable-model-invocation: true
source: pstack/skills/tdd/SKILL.md
---

# TDD bug fix

Use when the user explicitly requests TDD, a failing test or a regression test, or when the bug has an obvious cheap local test target. Skip a new test when the path is unclear, expensive, integration-heavy or impractical. Read this file directly when another playbook needs it; disabled model invocation is not a tool call.

## Steps

1. Establish the consumer, intended behavior, current behavior, affected path, smallest observable reproduction and current authority. Read [mobile lanes](../hugues-mode/references/mobile-lanes.md), the consumer's instructions and existing tests. Consumer edits and execution need the owner's authorization under [mode authority](../hugues-mode/SKILL.md#authority). End with the selected test seam and affected targets, or an explicit impractical-seam decision.
2. Choose the narrowest existing executable check. For Swift/iOS, use the repository's Swift Testing or XCTest target; for Kotlin/Android, its Kotlin/JUnit unit target or relevant instrumentation target. For KMP, use the common test seam on each affected Android and iOS target and cover changed native boundaries. Read the relevant installed owner test skill at this decision point if available; record its absence. If setup requires brittle mocks, slow end-to-end infrastructure, production-only state, vague reproduction or unrelated fixture churn, take the fallback below.
3. Write the smallest regression test before editing production code. Call the real behavior and assert a literal expected value or observable effect. Read [test behavior](../principle-test-behavior-not-implementation/SKILL.md). Finish when the check would catch the reported bug, rather than restating the implementation.
4. Run that check against the unfixed implementation. Preserve its exact command/tool arguments, target, failure and raw report under the [evidence guide](../hugues-mode/references/evidence-guide.md). RED means an observed failure for the intended reason. A passing test or unrelated build/fixture failure is not RED; correct the test or reproduction before the fix.
5. Fix the bug with the smallest production change that preserves nearby contracts. Keep the test's intended assertion. Weaken an assertion only when the expected behavior actually changed and the reason is explicit. For a flaky bug, make the check deterministic and record the signal it protects. Finish with a focused diff; consider broader sibling coverage only after the focused regression path works.
6. Run the same regression check after the fix. GREEN means its relevant assertions executed and passed on the stated target. Inspect reports for skips, retries and zero assertions. Run nearby affected checks and the lane's required runtime/native-caller proof within authority. A JVM pass proves no iOS result, and unit GREEN proves no screen journey. Preserve RED and GREEN separately, with literal expected and observed behavior, device/artifact identity and any blocked checks.

## Impractical seam

Prefer the closest useful executable regression check: a targeted script calling real code, a permitted manual reproduction command, UI automation, snapshot comparison, log assertion or focused integration check. Read [jev Drive](../hugues-mode/references/jev-drive.md) when the fallback drives a screen. Use existing permitted tools and authorized data. Missing runtime, tools or execution authority leaves that check blocked; it does not authorize installation, settings changes or new transmission.

Prefer no new test over a test that only checks mocks, implementation details, timing or unrelated global state. State why failing-before evidence was impractical, what the fallback directly observed and what remains unproven. Preserve the original failing mobile observation when the bug claims a runtime defect.

**Reply:** failing-before check and actual failure; passing-after command and actual assertions; literal behavior; nearby and per-target proof; fallback reason, evidence paths and remaining gaps.
