---
name: blast-radius
description: "Find what a change could break somewhere else before it ships, beyond the diff, and prove the one fact it's safe because of by running real code instead of writing it up. Use for 'blast radius of X', 'what could this break', or reviewing a small diff you don't trust."
source: pstack/skills/blast-radius/SKILL.md
disable-model-invocation: true
---

# blast-radius

Before work, read in full and in this order:

1. [Host adapter](../../adapters/host.md).
2. [Mobile adapter](../../adapters/mobile.md).
3. [Pinned blast-radius core](../../core/pstack/skills/blast-radius/SKILL.md).

Execute that core contract, applying only the named adapter translations and
the consumer project’s explicit policy. Read its phase-required references in full. Do not
substitute this loader for the workflow. Report blocked gates and actual proof.
