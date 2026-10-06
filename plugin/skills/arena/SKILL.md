---
name: arena
description: "Compare isolated parallel candidates, pick a base, graft the strongest parts and verify the synthesized artifact."
disable-model-invocation: true
source: pstack/skills/arena/SKILL.md
---

# Arena

Fan out N parallel attempts at the same task. Read every candidate end to end. Pick the strongest as the base. Graft the best ideas from the others into it. Verify the synthesized result.

## Start

Open the host todo list with one entry per phase before launching anything. If no todo tool exists, show the same numbered checklist and disclose that limit.

1. Frame
2. Fan out
3. Cross-judge
4. Pick
5. Graft
6. Verify

Read [hugues-mode](../hugues-mode/SKILL.md) for authority and [host notes](../hugues-mode/references/host-notes.md) for the actual native agent adapter. The coordinator runs arena; an assigned candidate or judge completes its scoped brief directly without recursive delegation. All work stays on the same host and in local isolated paths. Cloud workers and external transmissions are outside this workflow. Consumer edits, command execution and publication require the owner's existing explicit scope.

## Phase A: Frame

The N candidates will receive the same prompt, so the prompt is the contract.

1. State the artifact each candidate is producing.
2. Derive the rubric. State what success looks like for *this* task, then turn it into 3-6 concrete gradeable criteria. The rubric is the picker's tool in Phase D. Candidates only see the task.
3. Pick the runners. Default every seat to a fresh same-host native agent with `inherit-parent`: omit model and reasoning overrides. Same model N times is valid; distinct personas do not establish model diversity. Honor owner-selected role models only when accepted by the actual tool schema. Record configured and actual selections; disclose a rejected optional model and inherit the parent. If the owner required that model, mark the seat blocked instead of silently substituting. Missing model-role configuration needs no setup. Choose N for the exploration; architect requires at least two structurally distinct viable candidates.
4. Assign output paths. Each candidate writes to its own authorized git worktree where available, otherwise an absolute local task directory such as `/tmp/arena-<task-id>/candidate-<n>/`, per [separate-before-serializing-shared-state](../principle-separate-before-serializing-shared-state/SKILL.md). Resolve paths, verify assigned writable paths are disjoint and give each candidate exclusive output ownership. Apply native write restrictions when the host supports them. Worktree creation and local Git writes stay within recorded authority. Keep app source outside this plugin. Record the exact base revision and a separate synthesis path.
5. Follow [host notes](../hugues-mode/references/host-notes.md) before launching. Resolve both absolute mode/skills paths from the loaded package. Prepare complete fresh briefs with the common task, all later directives, consumer/revision, grounding paths, individual writable output scopes, domain/proof and authority. Use the registered Claude worker or complete wrapper fallback; Codex receives the complete hugues-agent wrapper before its assignment. Use the actual native tool schema and lifecycle tools to collect each result. Keep the 3-6 criterion rubric in the coordinator/judge record; omit it from every candidate prompt. Frame ends with the artifact, task, rubric, seats, base revision and isolated paths recorded. If native subagents are unavailable or prohibited, preserve this frame and report Fan out blocked; sequential self-attempts cannot establish independent candidates.

## Phase B: Fan out

Launch all N fresh native subagents concurrently through the host's actual tools, each with the same task, the path to the shared grounding, its own output path, and instructions to produce both the artifact and a short rationale. Use background execution only when the tool exposes it. Follow [host notes](../hugues-mode/references/host-notes.md) for the wrapper and lifecycle adapter. Candidate paths remain private while writers run; candidates receive no rival outputs. Each brief requires the actual diff, authorized checks with exit codes and unresolved gaps alongside its artifact and rationale. Candidate workers may sketch types/source in their assigned design scope; consumer implementation or test execution requires separate explicit authority.

Each rationale names the alternatives the candidate considered and what it rejected.

Wait for every candidate writer to finish before cross-judging. Inspect its actual files, not just its completion summary. If a candidate fails to produce output, proceed with N-1 and note the dropout in the synthesis record. At least one complete candidate is required for generic arena. For architect, preserve its two structurally distinct viable candidates requirement: replace a dropout or reframe before synthesis.

## Phase C: Cross-judge

After all Phase B candidate writers finish, spawn one fresh read-only native judge using [host notes](../hugues-mode/references/host-notes.md). Give the judge the task, grounding, authority, both absolute mode/skills paths and an isolated report path. It performs its read-only assignment directly without recursive delegation. Default to `inherit-parent`. Prefer a different model family only when the owner configured an available model; label actual process independence and any observed model difference accurately. It sees the task, rubric and candidates by neutral path labels, without runner identities or parent preference. Omit model names and candidate self-scores from its brief; require artifact citations for its recommendation. It scores each criterion and recommends a base with rationale. It runs in parallel with the coordinator's end-to-end reading and independent scoring in Phase D, not with the candidates themselves. The judge writes only its isolated report. If the judge cannot run, record Cross-judge blocked; retain candidates for a fresh judge rather than claiming adjudicated synthesis.

## Phase D: Pick a base

Read every candidate end to end before picking.

Score each candidate against the rubric criterion by criterion, not on holistic feel. Compare against the cross-judge. Agreement on the base confirms the pick. Disagreement means one of you is biased or the rubric was ambiguous. Read both rationales and resolve the disputed criteria against the actual artifacts before deciding. Record the disagreement and its resolution; counting votes or averaging scores cannot replace judgment.

Pick the base on which candidate a future maintainer can extend most easily without breaking invariants. Prefer the cleaner boundary or smaller API when two feel tied, per the Laziness Protocol.

Record the pick and the reason in a short synthesis note alongside the base artifact, including the cross-judge's verdict.

## Phase E: Graft

Walk each losing candidate once more and identify what is worth porting into the base. The signal is usually one or two things per candidate, not most of it.

Fold each graft in by hand, per the **redesign-from-first-principles** principle skill. Don't paste mechanically. The result has to remain coherent under one mental model.

Record what was grafted, from which candidate, and what was rejected and why.

For generic arena, when N candidates converge on the same shape, that is a strong agreement signal. Note the convergence in the record and ship the consensus shape. No graft is needed. When N candidates wildly diverge, Phase A was under-specified. Reframe and re-run rather than averaging the divergence. Architect must first satisfy its two structurally distinct viable candidates requirement; convergence is a reason to seek another whole-shape alternative before its synthesis.

## Phase F: Verify

Inspect and verify the actual synthesized artifact at its recorded path against the original task and rubric, per [prove-it-works](../principle-prove-it-works/SKILL.md). For a design package, reconcile caller usage with types and signatures, trace the module map and grounding invariants, and screen [design red flags](../architect/references/design-red-flags.md). For an executable mobile artifact, follow [mobile lanes](../hugues-mode/references/mobile-lanes.md) on every affected target within execution authority. A runner report, candidate test result or compilation of the ungrafted base does not verify the synthesis. Record commands, exit codes, inspected reports and actual artifact identity. Blocked proof remains blocked; retain its required check.

If verification surfaces a problem the arena did not catch, either Phase A was wrong (re-frame and re-run) or one candidate caught it and you missed the graft (go back to Phase E). Record which branch the evidence supports and repeat that phase with fresh scoped workers where work changes. Complete Verify only when the synthesized artifact satisfies the task and rubric and the required proof is observed; report any remaining gap without claiming completion.

## Outputs

One synthesized artifact. One short synthesis note alongside, naming the base, the grafts (with source candidate), the rejections, the dropouts if any, and the verification result.
