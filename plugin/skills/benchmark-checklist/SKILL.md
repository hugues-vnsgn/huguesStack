---
name: benchmark-checklist
description: "Vet a perf measurement (limiter, tuning, limits, errors, repeatability, relevance, and whether the work happened) before you report or act on it. Use when you run a benchmark or report a speedup or regression you measured."
source: pstack/skills/benchmark-checklist/SKILL.md
disable-model-invocation: true
---

# benchmark-checklist

Before work, read in full and in this order:

1. [Host adapter](../../adapters/host.md).
2. [Mobile adapter](../../adapters/mobile.md).
3. [Project PR policy](../../policies/astra-pr-review.md).
4. [Pinned benchmark-checklist core](../../core/pstack/skills/benchmark-checklist/SKILL.md).

Execute that core contract, applying only the named adapter translations and
explicit project policy. Read its phase-required references in full. Do not
substitute this loader for the workflow. Report blocked gates and actual proof.
