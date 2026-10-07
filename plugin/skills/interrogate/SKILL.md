---
name: interrogate
description: "Use for \"interrogate\", \"adversarial review\", \"multi-model review\", \"challenge this\", \"stress test this code\", \"find blind spots\", or \"tear this apart\". Multiple LLM reviewers challenge changes from independent angles."
source: pstack/skills/interrogate/SKILL.md
disable-model-invocation: true
---

# interrogate

Before work, read in full and in this order:

1. [Host adapter](../../adapters/host.md).
2. [Mobile adapter](../../adapters/mobile.md).
3. [Project PR policy](../../policies/astra-pr-review.md).
4. [Pinned interrogate core](../../core/pstack/skills/interrogate/SKILL.md).

Execute that core contract, applying only the named adapter translations and
explicit project policy. Read its phase-required references in full. Do not
substitute this loader for the workflow. Report blocked gates and actual proof.
