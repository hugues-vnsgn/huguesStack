---
name: maintain-verification-skill
description: "Periodic pass that keeps a project's verification skill and feature map honest: parallel source readers per feature, one live session driving every feature, at most one PR of proven corrections. Use for /maintain-verification-skill or \"audit the verify skill\"."
source: pstack/skills/maintain-verification-skill/SKILL.md
disable-model-invocation: true
---

# maintain-verification-skill

Before work, read in full and in this order:

1. [Host adapter](../../adapters/host.md).
2. [Mobile adapter](../../adapters/mobile.md).
3. [Pinned maintain-verification-skill core](../../core/pstack/skills/maintain-verification-skill/SKILL.md).

Execute that core contract, applying only the named adapter translations and
the consumer project’s explicit policy. Read its phase-required references in full. Do not
substitute this loader for the workflow. Report blocked gates and actual proof.
