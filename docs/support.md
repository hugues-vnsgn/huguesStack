# Support evidence

Status snapshot: **5 October 2026**, development package `0.1.0-dev.3`.
The [evidence index](evidence-index.md) is authoritative for receipts, revisions,
counts, failed attempts and prerequisites. Use [WORKFLOW](WORKFLOW.md) to start
a task. This combined PR #6/#7 checkout retains WP6 documentation and the
[verification continuation](verification-continuation.md). It runs no consumer
proof; PR publication states below describe the pre-integration snapshots.

Use per-cell states **authored**, **static-tested**, **observed-pass**,
**observed-fail**, **blocked** and **deferred**. Separately record run outcomes
**pass**, **fail**, **flaky**, **skipped** or **incomplete**. A review's completion
and verdict are separate facts. A blocked test is unrun, a skip is an excluded
assertion, and a successful retry retains its flaky outcome.

| Cell | State | Evidence and limits |
|---|---|---|
| Package, 27 skills and local contracts | static-tested | Integrated main: 119 framework tests and package/upstream/strict metadata/shell/whitespace checks passed. PR #6 pre-integration head: 120 tests. Counts are historical; combined final-head checks belong in the integration PR receipts |
| Upstream inventory | static-tested | pstack 0.15.9; all 161 responsibilities reconciled; verified delta 3 added / 18 changed / 0 removed. [Manual sync procedure](upstream/README.md); deferred benchmark link preserves exact upstream bytes |
| Claude historical cold load | observed-pass | WP1 fresh session and exact probe reply; historical body only |
| Claude project recipe invocation | observed-pass | Later native Skill-tool read-only invocation passed; two earlier unknown-skill probes retained |
| Claude verification generator invocation | observed-pass | Authored a complete private candidate; no canonical consumer write or full cycle inferred |
| Claude full mode routing | deferred | Unrun; static review and generator invocation do not establish fourteen-playbook routing |
| Codex marketplace discovery/manual path | observed-pass | Discovery without installation; manual project-skill probes and direct-read fallback. WP2 full planning preview: 11 routes/61 steps on its recorded head |
| Codex native install/invocation | blocked | Installation outside current authority; no native invocation pass claimed |
| Native todo integration | blocked | Codex preview used displayed checklist fallback; no native todo tool exposed |
| Fresh host delegation and multi-turn persistence | authored | Guidance supplied; native runtime behavior unrun |
| Project-local recipe and full applied cycle | blocked | Private candidate/helper reviewed; cached compile/APK and eight fresh iOS logic tests passed. Canonical guide and new native screens await separate approvals; API37 blocks 12 new Android tests |
| Historical KMP shared navigation/header task | observed-pass | 12 Android JVM/eight iOS logic tests and callers on both native hosts; artifact-bound, bounded scope. Older 11-test snapshot retained separately |
| Historical CMP journey/header task | observed-pass | Android and two iOS runtime journeys, normal/enlarged text; successful attempts followed failures. Header geometry checks scoped; bottom-tab clipping outside assigned scope |
| Android Jev labels | observed-pass | One approved run: 3/3 checkpoints, six claims, 0.98 to 0.99 probabilities. Labels only; run authority consumed |
| iOS Jev judgment | blocked | Driver uses MobileBuildMCP; consumer requires XcodeBuildMCP. Local captures remain separate |
| Independent Swift app/test-bundle build | observed-pass | Signing-disabled build passed on retry; zero tests and no launch |
| Independent Swift task | blocked | NetNewsWire hosted runtime authority pending; no independent feature proof |
| Independent Kotlin demo build | observed-pass | Now in Android demo assembled offline; zero tests and no launch |
| Independent Kotlin task | blocked | Three uncached test libraries require download authority; distinct from the shared-UI consumer's API37 |
| Layer 2, feature maps and CLI-first addition | deferred | Managed workers remain outside Layer 1; draft #2 additions remain post-first-release |

PRs [#1](https://github.com/hugues-vnsgn/huguesStack/pull/1),
[#3](https://github.com/hugues-vnsgn/huguesStack/pull/3),
[#4](https://github.com/hugues-vnsgn/huguesStack/pull/4) and
[#5](https://github.com/hugues-vnsgn/huguesStack/pull/5) are merged.
[#6](https://github.com/hugues-vnsgn/huguesStack/pull/6) was a separate draft
for continuation evidence and review policy at WP6 review; its changes are
included in this combined checkout. [#2](https://github.com/hugues-vnsgn/huguesStack/pull/2)
remains a deferred draft. Read the evidence index for exact heads and review
verdicts. Historical cross-host Opus/Fable reviews remain preserved; new PR
reviews use independent **GPT-6 Astra High**, with exact final-head evidence.
Read the [PR review policy](../plugin/skills/hugues-mode/references/pr-review-policy.md)
before launching those reviews. Same-host agent review establishes process
independence, not cross-host proof.

WP6 originally covered docs, checks, review and a new draft PR. The owner later
approved integrating and merging PRs #6 and #7 after combined checks and review.
Consumer-guide/screens, Swift runtime and Kotlin download decisions remain
pending; no dependent consumer run or release is authorized.
The four-domain coverage and full generated cycle remain incomplete. The
owner's revised [plan](PLAN.md) permits a release checkpoint with labelled gap
reasons; those reasons never become observed support. Target remains
**9 October 2026, end of day GMT+7**.

Historical methods and receipts remain in [WP1 validation](wp1-validation.md),
[WP2 validation](wp2-validation.md), [WP3 validation](wp3-validation.md),
[host loading](host-loading.md) and the evidence index. Raw native artifacts
remain outside the public repository.
