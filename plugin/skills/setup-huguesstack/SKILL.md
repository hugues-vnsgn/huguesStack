---
name: setup-huguesstack
description: Configure which models pstack uses per role and at what reasoning budget. Detects your available models and writes an always-applied rule that overrides the skill defaults. Use for /setup-pstack, "configure pstack models", "pstack budget", or changing pstack's model choices.
source: pstack/skills/setup-pstack/SKILL.md
---

# setup-huguesstack

Before work, read in full and in this order:

1. [Host adapter](../../adapters/host.md).
2. [Mobile adapter](../../adapters/mobile.md).
3. [Pinned setup-pstack core](../../core/pstack/skills/setup-pstack/SKILL.md).

Execute that core contract, applying only the named adapter translations and
the consumer project’s explicit policy. Read its phase-required references in full. Do not
substitute this loader for the workflow. Report blocked gates and actual proof.
