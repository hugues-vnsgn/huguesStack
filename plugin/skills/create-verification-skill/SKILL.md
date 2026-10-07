---
name: create-verification-skill
description: "Generate a project-local verification skill that drives your app the way a user does — any language, framework, or platform. Use for /create-verification-skill, \"make a control skill for this repo\", or when a project has no scripted way to prove UI/CLI/service behavior."
source: pstack/skills/create-verification-skill/SKILL.md
disable-model-invocation: true
---

# create-verification-skill

Before work, read in full and in this order:

1. [Host adapter](../../adapters/host.md).
2. [Mobile adapter](../../adapters/mobile.md).
3. [Project PR policy](../../policies/astra-pr-review.md).
4. [Pinned create-verification-skill core](../../core/pstack/skills/create-verification-skill/SKILL.md).

Execute that core contract, applying only the named adapter translations and
explicit project policy. Read its phase-required references in full. Do not
substitute this loader for the workflow. Report blocked gates and actual proof.
