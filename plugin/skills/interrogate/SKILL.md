---
name: interrogate
description: "Review a diff adversarially, including a diff from the other host."
disable-model-invocation: true
source: pstack/skills/interrogate/SKILL.md
---

# Interrogate

Return an adjudicated review. Apply no fixes and perform no remote actions during this review. The review is read-only.

## Steps

1. Establish the exact review scope and base from the user's files, diff or PR. Read the actual changes and surrounding context. State the intended behavior in one paragraph; ask only when the intent cannot be established from available evidence.
2. State the producing host, reviewing host and independence claim. A diff produced by Claude Code and actually reviewed in Codex, or the reverse, is cross-host review. Two fresh reviewers in this host provide process independence only. If the producing host is unknown, label it unknown. Never invoke the other host or send it a message without the user's explicit request.
3. Read [host notes](../hugues-mode/references/host-notes.md), [reviewer prompt](references/reviewer-prompt.md), [rubric](references/rubric.md) and [code-quality lens](references/code-quality-review.md). Give two fresh read-only native subagents the same filled template, exact scope and context. Omit model overrides to inherit the parent by default. Honor explicit supported user model choices. Require each finding to name its location, actual execution path and evidence. If subagents are unavailable or prohibited, report the independence gap and conduct a labelled single-reviewer assessment.
4. Read [lead judgment](references/lead-judgment.md) and adjudicate every finding against the actual intent and context. Deduplicate agreement, preserve disagreements and verify material claims by reading the cited code or existing evidence. Classify each finding as act on, consider, noted or dismissed and give the reason. A read-only review never runs a consumer app unless the current user instruction expressly authorizes that verification.
5. Report intent, exact reviewed revision or files, reviewer identities and independence label, adjudicated findings and agreement map. Name unrun checks and evidence gaps. Leave fixes, publication and merging to a separately authorized work round.

## Review result

Use the upstream review categories. A clean result states `No material findings` and retains its scope and evidence limits. Agreement by two same-host agents does not establish model diversity. A cross-host label requires the actual reviewing host, not a request to arrange one.
