---
name: correct
description: "Find the mistakes agents keep repeating in this repo and make each one impossible. Try architecture first, then types, then a lint whose error names the fix, then a test, and write docs last. Prove each check fails on a real past mistake. Repeat this each time the operator corrects you. Use for /correct."
source: pstack/skills/correct/SKILL.md
disable-model-invocation: true
---

# correct

Before work, read in full and in this order:

1. [Host adapter](../../adapters/host.md).
2. [Mobile adapter](../../adapters/mobile.md).
3. [Pinned correct core](../../core/pstack/skills/correct/SKILL.md).

Execute that core contract, applying only the named adapter translations and
the consumer project’s explicit policy. Read its phase-required references in full. Do not
substitute this loader for the workflow. Report blocked gates and actual proof.
