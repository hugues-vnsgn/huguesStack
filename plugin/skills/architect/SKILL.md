---
name: architect
description: "Sketch mobile types, signatures and module boundaries, synthesize alternatives, then implement against the chosen design."
disable-model-invocation: true
source: pstack/skills/architect/SKILL.md
---

# Architect

Design before implementing. Sketch types, function signatures, class shapes, and module boundaries with `not implemented` bodies and pseudocode. Synthesize across independent design candidates, then fill in code against the chosen sketch. If implementation proves the sketch wrong, throw it out and redesign.

## Start

Open the host todo list with one entry per phase before starting. If no todo tool exists, show the same numbered checklist and disclose that limit.

1. Ground
2. Sketch
3. Agree
4. Implement
5. Scrap

Read [hugues-mode](../hugues-mode/SKILL.md) and establish the consumer, revision, authorized paths and whether this is design-only or implementation work. A design-only request ends after synthesis (or its requested checkpoint). Implementation requires authority for that consumer. Use [mobile lanes](../hugues-mode/references/mobile-lanes.md) to record Swift/iOS, Kotlin/Android, KMP shared logic or CMP shared UI, affected targets and required proof. Unknown lanes stay unresolved until repository evidence identifies them.

Act as the coordinator for this workflow. An assigned scoped worker performs its brief directly and returns its package; it does not recursively launch architect, arena or implementation delegates. Read disabled skills directly from their resolved package paths.

## Phase A: Ground the problem

Build a real mental model of every system the new code touches. Read and run [how](../how/SKILL.md) over the relevant subsystems.

Naming a file isn't grounding. Produce the traced model `how` prescribes. If the design redefines ownership or layering, also read and run [why](../why/SKILL.md) on the existing shape so the rationale becomes a constraint, not a guess.

Skip Phase A only when the work is genuinely greenfield with no surrounding system to integrate. Record that evidence and the skip reason. Otherwise finish only when how's traced model covers every touched subsystem and why's rationale covers any changed ownership or layering. If either required file or its evidence is absent, mark Ground blocked and report the missing dependency; resume here when it is available.

## Phase B: Sketch

Read and run [arena](../arena/SKILL.md) with the design-sketch task and the Phase A grounding artifacts. Pass [runner prompt](references/runner-prompt.md) as each runner's prompt. Each candidate produces a design package shaped per [rationale template](references/rationale-template.md). Use arena's native host adapter and isolated local paths. Candidates receive the task and grounding; the scoring rubric stays with the coordinator and cross-judge.

Use owner-selected architect runners only when the current host supports them. With no role configuration, use at least two fresh same-host native runners with `inherit-parent` (omit model and reasoning overrides). These are independent attempts, not evidence of model diversity. Record actual host/model availability and rejected selections per arena's Phase A.

Design it twice. Require at least two structurally distinct candidates before synthesis, even when the first looks sufficient. This is the **exhaust-the-design-space** principle skill made concrete. Whole-shape alternatives, not point fixes inside one shape. A dropout or convergence does not waive this minimum: launch a fresh replacement or reframe until two structurally distinct viable packages exist. If native delegation is unavailable or prohibited, retain the grounding and mark Sketch blocked; a single attempt cannot complete architect.

Screen every candidate against [`references/design-red-flags.md`](references/design-red-flags.md) before synthesis. Assume the next contributor is an agent that sees only the files it opened, copies the nearest example, and takes the shortest path that compiles. Prefer the design where a change that looks right from one file is right for the whole repo.

Compare viable candidates on interface depth. Prefer the design that hides more complexity behind a smaller, simpler public surface. A rich interface can keep call chains short by concentrating capability instead of scattering it across layers.

Complete Sketch only after every candidate has been screened, the cross-judge and coordinator scores are adjudicated, and arena has verified the actual synthesized usage, types, signatures and module map. Arena returns one synthesized design package. The synthesis decision populates the rationale's "Synthesis decision" section.

## Phase C: Agree (opt-in)

Default: proceed directly to implementation with the synthesized design. No human checkpoint. Apply this default within recorded consumer implementation authority. For design-only scope, mark Implement and Scrap skipped: design-only and return the verified package after any requested checkpoint.

Opt in to a checkpoint when the invoker explicitly asks: "/architect with checkpoint," "stop and show me before implementing," or similar. Then surface the synthesized design and pause for sign-off.

Within existing local Git authority, the synthesis can be saved as its own local commit either way, as the "scaffold first" mode of the **foundational-thinking** principle skill. Planned and scoped breakage during fill-in is fine, per the **outcome-oriented-execution** principle skill. For adversarial pressure on the design before implementing, read and run [interrogate](../interrogate/SKILL.md) on the synthesized sketch. Remote publication requires explicit owner authority.

If the human pushes back on the shape (in a checkpoint or after the fact), treat that as Phase A evidence. Re-ground and re-run Phase B before writing more code.

## Phase D: Implement against the sketch

The coordinator briefs a fresh implementation worker using [host notes](../hugues-mode/references/host-notes.md), the original request, later directives, both absolute mode/skills paths, exact revision, writable scope, grounding, synthesized package, mobile lane and current consumer authority. The worker replaces `not implemented` bodies with code, pseudocode with logic, directly within that scope. The synthesized sketch is the contract. Candidate runners are finished; implementation is a fresh work round. The coordinator inspects the actual diff and verifies the resulting artifact using the affected mobile lanes. Report every required target and blocked, skipped or flaky check separately; a build alone cannot establish native caller or UI behavior.

Deviations from the sketch are signal worth surfacing, not friction to absorb silently. If a function needs a parameter the sketch didn't anticipate, ask whether the sketch was wrong, the requirement was missed, or the implementation is overreaching.

## Phase E: Scrap when the architecture is wrong

If implementation keeps producing friction the sketch can't absorb, throw the sketch out. Don't bolt fixes onto a wrong design, per the **redesign-from-first-principles** and **fix-root-causes** principle skills.

The signal is a *pattern*, not single instances. Tells:

- The same shape of workaround appearing repeatedly across unrelated code.
- Multiple unrelated edge cases that all need special-case branches.
- Types that need escape hatches (`any`, casts, optional fields always set in practice) to compile.
- The "we need a lock" reflex when the sketch said the state wasn't shared.
- Callers having to know the abstraction's internal rules to use it.
- Two or more independent Phase D deviations of the same shape across the implementation.

Use judgment. A few edge cases don't condemn an architecture. Some problems are legitimately complex. Complexity in the data is not complexity in the design.

When you scrap:

1. Re-run [how](../how/SKILL.md) over what's been built; re-run [why](../why/SKILL.md) when ownership or layering changed.
2. Redesign as if the new constraints had been day-one assumptions, per redesign-from-first-principles.
3. Subtract before adding, per the **subtract-before-you-add** principle skill. The new sketch should be smaller than the old one before it grows.
4. Return to Phase B and re-run arena with fresh candidates and the new grounding. Preserve the old sketch and deviation record as evidence.

## Outputs

The caller's usage is written first and the type sketch derived from it. One file with new types and signatures for small changes. Module map plus type definitions for larger work. The rationale ships alongside, shaped per `references/rationale-template.md`, including the usage sketch and the synthesis decision.
