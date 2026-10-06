---
name: correct
description: "Turn recurring agent mistakes into architecture, types, lint or tests, prove enforcement against a real past mistake, and keep a rule/enforcement table."
disable-model-invocation: true
source: pstack/skills/correct/SKILL.md
---

# Correct

Change the repo so the next agent cannot repeat the mistakes the owner keeps correcting. Assume an agent sees only opened files, copies the nearest example and chooses the shortest path that compiles. Read this file directly when a playbook needs it.

## Steps

1. Establish the repository, owner's correction, writable paths and current edit/execution authority under [mode authority](../hugues-mode/SKILL.md#authority). Read recent commits, reverts, review comments, repository instructions and workaround comments. Group mistakes into classes backed by at least two actual occurrences. Record exact evidence; distinguish a one-off from a recurring class. Use local history and already available authorized readers; missing review access is a gap, not permission to connect or contact people.
2. Choose the highest enforcement level that works for each class. Read [encode lessons in structure](../principle-encode-lessons-in-structure/SKILL.md) and [type system discipline](../principle-type-system-discipline/SKILL.md) at that decision. First eliminate the mistake with architecture: one state owner, one supported task path, hidden internals, one source of truth, removal of obsolete examples. Then encode illegal states in Swift types/enums or Kotlin sealed/value types, including actual KMP export constraints. If bad code still compiles, use a scoped existing lint/check whose diagnostic names the replacement file, type or function; when already widespread, reject new occurrences rather than forcing unrelated cleanup. Next test real behavior using the appropriate Swift Testing/XCTest, Kotlin/JUnit or KMP target seam. Write docs or agent rules last, for judgment calls that cannot be enforced. Record why each higher level did not work.
3. Fix the most frequent classes within the authorized diff. Keep each class independently reviewable, one commit per class only when commits are authorized. Read [test behavior](../principle-test-behavior-not-implementation/SKILL.md); replace or remove tests that still pass when called functions return nothing. Prove each new check fails on a real past mistake in an isolated authorized copy, preserving the failure and its diagnostic. Run the same command after the correction and retain the passing result. Use existing CI parity when available; report CI unrun or missing rather than installing CI, changing global policies or claiming a remote run. An unexecuted proposed check is unproven.
4. Keep a rule/enforcement table in the repository's existing agent instruction file within scope. Pair each rule with its actual architecture/type/lint/test enforcement and proof command; label judgment-only rules as such. When the owner corrects a covered recurring mistake, repair its missing enforcement at the highest level in the same authorized change. Drop a rule once the mistake cannot happen. Exceptions require the offending line, reason, expiry date and actual human approval under repository policy; a skill cannot grant that approval. Report needed approval without fabricating it or relaxing enforcement.

Use the [evidence guide](../hugues-mode/references/evidence-guide.md) and [mobile lanes](../hugues-mode/references/mobile-lanes.md) for affected mobile proof. Preserve separate failing and passing artifacts, exact commands/tool results, revisions, target identities and remaining gaps. Consumer edits, builds, installs, settings changes, publication and new transmission still require their own current authority.

**Reply:** each class and its repeated evidence, chosen enforcement level, why higher levels failed, actual failing-before/passing-after proof, rule/enforcement table path, CI parity or gap and remaining blockers.
