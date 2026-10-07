---
name: make-bot-ui
description: "Use when building a custom UI (page, dashboard, buttons) that should wake a Grok Bot over a webhook, when the user must provide a webhook sender key, or when exposing that UI on Tailscale."
source: pstack/skills/make-bot-ui/SKILL.md
disable-model-invocation: true
---

# make-bot-ui

Before work, read in full and in this order:

1. [Host adapter](../../adapters/host.md).
2. [Mobile adapter](../../adapters/mobile.md).
3. [Project PR policy](../../policies/astra-pr-review.md).
4. [Pinned make-bot-ui core](../../core/pstack/skills/make-bot-ui/SKILL.md).

Execute that core contract, applying only the named adapter translations and
explicit project policy. Read its phase-required references in full. Do not
substitute this loader for the workflow. Report blocked gates and actual proof.
