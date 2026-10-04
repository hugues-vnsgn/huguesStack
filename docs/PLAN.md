# huguesStack implementation plan

Public requirements summary of the owner’s revised 4 October 2026 plan. The exact source documents remain preserved locally, with SHA-256 provenance. This summary omits personal machine inventories and historical consumer-project research.

## Product and boundaries

Build a standalone, mobile-first adaptation of pstack for Claude Code and Codex. Native Swift/iOS, native Kotlin/Android, Kotlin Multiplatform shared logic, and Compose Multiplatform shared UI are first-class domains. Consumer applications remain separate projects.

Layer 1 is the entire 0.1.0 release candidate: skills, playbooks, principles, one agent definition, two small scripts, and documentation. Layer 2 is the deferred hstack-alpha managed-worker runtime. Its earlier evidence does not establish Layer 1 support. The inaccessible mobile-stack prototype ZIP and its reported 44-test baseline are superseded; this implementation does not depend on them.

Target completion remains end of day **9 October 2026, GMT+7**. The revised plan assigns five working blocks, 5–9 October. Deadline alone establishes no readiness claim.

## Method

The owner supplies a goal and a way to check it. `hugues-mode` selects a playbook and copies its steps into the host’s todo list. The coordinator investigates, designs, delegates implementation to a fresh subagent each round, and verifies independently. Same-vendor fresh-agent review provides process independence; cross-host review provides model independence. Each completed package gets a separate draft pull request for owner-arranged Claude review. Do not merge automatically.

Claude Code is the primary host; Codex is smoke-tested. Default model roles inherit the parent. Use the owner’s existing mobile and authoring skills rather than duplicating them. Compose jev-ios-bridge for device screen checks when available.

## Work packages

| Package | Deliverable | Acceptance |
|---|---|---|
| WP1 package and loaders | Repository, marketplace/plugin manifests, validator, cold-load evidence | Host states observed or honestly labelled; regression tests reject invalid packages |
| WP2 mode and playbooks | `hugues-mode`, ten adapted playbooks, four mobile playbooks, 24 principles, `hugues-agent` | Routing prompts open expected steps; principles attributed |
| WP3 proof lane | `mobile-proof`, `build-doctor`, jev wiring, project-local verification skill | One driven feature and durable evidence artifacts |
| WP4 consumer tasks | Swift, Kotlin and KMP/CMP tasks outside this repository | Red-then-green task evidence on the claimed targets |
| WP5 upstream sync | Pin, delta, sync script, re-pinned responsibility ledger | Reproduce 3 added / 18 changed / 0 removed files from the earlier pin |
| WP6 docs and release | Workflow guide, support matrix, README and accepted 0.1.0 tag | Owner can start a task and see every remaining gap |

WP1 is the first implementation package. Its loader probe does not claim WP2 routing or mobile workflow support. Consumer execution and edits require clear authorization; the current repository implementation does not grant it. Tool installation, global settings changes, automatic cleanup, and unattended work are outside this package.

## Planned upstream baseline

Upstream: [cursor/plugins pstack](https://github.com/cursor/plugins/tree/e43c7ee26e0038c6c1fa8380dd34ce86ff94cb2a/pstack), version 0.15.9 at `e43c7ee26e0038c6c1fa8380dd34ce86ff94cb2a`. The owner’s research reports 161 files and a 21-file delta from version 0.15.5 at `2eb7ed4613cfc8f098dfe464a23680ea44d84c5e`. Re-fetch and verify these during WP5; they are planning inputs until independently checked. Forked skills retain upstream `source:` paths. Port principles verbatim with MIT attribution. Weekly triage compares blob SHAs; read playbook diffs rather than overwriting adaptations.

0.1.0 functional scope: mode, how, why, architect, arena, interrogate, tdd, blast-radius, bounded local swarm, create/maintain verification skills, show-me-your-work, correct, setup-huguesstack, fresh worker, and the 24 principles. Reference the installed unslop skill where available.

Adapted playbooks: investigation, bug-fix, feature, prototype, refactoring, visual-parity, authoring-a-skill, session-pickup, pause-safely, and opening-a-pr. Mobile additions: build-doctor, mobile-proof, kmp-bridge-change, and cmp-two-target-change.

## Proof and reporting

Per-cell states are authored, static-tested, observed-pass, observed-fail, blocked, or deferred. Run outcomes are pass, fail, flaky, skipped, or incomplete. Keep them separate. A skipped test is never a passed assertion, retry success is reported as flaky, and wrong-target results do not count.

The personal-workflow bar is one observed task per domain, Claude primary, Codex smoke-tested, with gaps listed rather than silently promoted to support. Swift proof includes relevant XCTest, a simulator build and one driven user path. Kotlin proof includes relevant tests, demoDebug assembly and an emulator user path. KMP proof includes common tests and a native caller on each target; CMP proof includes Android and iOS screens plus semantics or text scaling. One cross-host review must have adjudicated findings.

Keep run evidence outside the repo. Record plugin Git SHA, host version, consumer repo and SHA, target/device identity, each command as argv with exit code, and artifact paths. Keep raw test and device artifacts. List evidence limitations in support.md.

## Deferred work

Layer 2 retains work ledgers, leases, cancellation, worker accounting, managed isolation and unattended authority contracts. Parsers, evidence schemas and deterministic archives are dropped from Layer 1. Performance, benchmark wiring, eval, reflect, teach, recall, figure-it-out, no-comments, technical-writing, bro, multi-phase plans and automatic workflows are deferred. Automate-me, make-bot-ui and Benny are not planned. Store submission, physical-device performance certification, system SDK/JDK changes and full upstream parity are non-goals.

### Post-first-release workflow additions

Both additions below are explicitly deferred until after the first release. They add no 0.1.0 acceptance criteria and do not weaken the existing build, test, native-caller or UI proof checks. Keep feature implementation paused at this checkpoint while the owner reviews WP1 PR #1.

| Addition | Post-release acceptance | Rationale |
|---|---|---|
| Consumer-app feature map | For each chosen consumer app, maintain a short summary of its key user-visible features and expected behavior. Keep consumer app source outside the plugin. | Give the owner and agents a simple shared picture of the app's features. |
| CLI-first verification for easy paths | Identify straightforward checks that CLI commands can prove; record argv, exit codes and artifacts. Retain required native/UI verification wherever CLI is insufficient. | Reduce token use on easy paths while preserving the proof bar. |
