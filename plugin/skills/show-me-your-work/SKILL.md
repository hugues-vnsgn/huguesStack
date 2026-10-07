---
name: show-me-your-work
description: "Keep a reviewable decision trail for long-running or unattended work: a TSV log with one row per decision (what, why, evidence, result). Local by default; commit it when a reviewer needs the trail to trust the result. Use for /show-me-your-work, autonomous or multi-phase runs, or work a human reviews after stepping away."
source: pstack/skills/show-me-your-work/SKILL.md
disable-model-invocation: true
---

# show-me-your-work

Before work, read in full and in this order:

1. [Host adapter](../../adapters/host.md).
2. [Mobile adapter](../../adapters/mobile.md).
3. [Pinned show-me-your-work core](../../core/pstack/skills/show-me-your-work/SKILL.md).

Execute that core contract, applying only the named adapter translations and
the consumer project’s explicit policy. Read its phase-required references in full. Do not
substitute this loader for the workflow. Report blocked gates and actual proof.
