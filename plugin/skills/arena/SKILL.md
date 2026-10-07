---
name: arena
description: "Spawn N parallel candidates at the same task, pick a base, graft the strongest parts of the losers into it. Use for /arena, 'arena this', 'throw it in the arena', or when one attempt at a non-trivial artifact would lock in the wrong shape."
source: pstack/skills/arena/SKILL.md
disable-model-invocation: true
---

# arena

Before work, read in full and in this order:

1. [Host adapter](../../adapters/host.md).
2. [Mobile adapter](../../adapters/mobile.md).
3. [Project PR policy](../../policies/astra-pr-review.md).
4. [Pinned arena core](../../core/pstack/skills/arena/SKILL.md).

Execute that core contract, applying only the named adapter translations and
explicit project policy. Read its phase-required references in full. Do not
substitute this loader for the workflow. Report blocked gates and actual proof.
