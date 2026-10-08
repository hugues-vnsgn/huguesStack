> Retained bounded-mobile extension template. Use only for an explicitly requested one-journey diagnostic. The default generator loads its owned feature-map example and seeds the top 3–5 features. This template cannot satisfy generation or whole-map maintenance by itself.

# Project verification skill template

Use this structure when writing a consumer-local skill. Replace angle-bracket prompts with facts from the repository; for an unavailable check, write its exact prerequisite and status instead of a guessed command. An incomplete recipe remains authored or blocked. This template is guidance, not an observed run.

```markdown
---
name: verify-<app>
description: "Verify <agreed user journey> on <named targets> and retain its evidence."
disable-model-invocation: true
---

# Verify <app>

## Scope and authority

<Repository/worktree, permitted files/actions, domains, journey and expected checkpoints.>
<Applicable repository instructions and required tools.>
<Repository-supported canonical skill path and host layout; verified symlink resolution/loader result or regular-copy hashes and synchronization rule. Record supported native invocation and actual discovery evidence. If unavailable or denied, hold; never substitute direct body reads.>

## Launch

<Exact working directory and build/test argv arrays, process-local environment, scheme/variant and destination.>
<Launch/install tool calls or argv, artifact identity and readiness signal for each target.>
<Missing checks and their prerequisites; use only permitted existing tools.>

## Doctor

<Read-only checks for the app/build identity, selected device, foreground screen and test data.>
<Run before the first drive and after any surprising result. Reset only owned test state within authority.>

## Drive

<One agreed journey, stable selectors observed in current screen captures and expected checkpoint text.>
<Actual installed jev test-ios/test-android skill and guide paths, available tools and scenario path.>
<If jev is unavailable: permitted UI test/device recipe, its observed evidence and label no judged verdict.>
<For shared changes: separate native callers/hosts and semantics or text-scaling checks where required.>

## Evidence

<Durable task folder outside the consumer and plugin repositories.>
<Plugin and consumer SHAs, dirty diff receipt, host/tool versions and per-target device/app identity.>
<Each command's cwd, argv, environment changes, exit code and logs; tool calls retain actual tool/arguments/result.>
<Separate attempt/result paths, assertion counts, screen observations and recorded verdict/reason code.>
<Skipped, flaky, incomplete and wrong-target results do not count as clean passing assertions.>
<Review scope/verdict and every blocked or unrun check. Keep private artifacts local.>

## Cleanup

<Only owned instances/scratch state and the commands/tools allowed to remove them.>
<Retain the evidence folder; reopen and inspect its artifacts after cleanup.>
<If teardown is unrequested or unsafe, record the retained instance and handoff.>
```

Include helpers only when they are needed and within scope. Give each an executable mode, exact invocation and bounded ownership. Keep build caches and processes that belong to the user intact.
