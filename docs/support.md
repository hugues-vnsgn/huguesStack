# Support evidence

Status snapshot: **6 October 2026**, prerelease candidate **`0.1.0-rc.1`**.
This candidate is for a separate draft RC review; no merge, tag or release is
established. The [evidence index](evidence-index.md) records historical revisions,
receipts, failed attempts and limits. Read [WORKFLOW](WORKFLOW.md) to start a task
and the [RC notes](RELEASE-0.1.0.md) for the review scope.

Use per-cell states **authored**, **static-tested**, **observed-pass**,
**observed-fail**, **blocked** and **deferred**. Separately record run outcomes
**pass**, **fail**, **flaky**, **skipped** or **incomplete**. Review completion
and verdict are separate facts. A blocked test is unrun; a skip is an excluded
assertion. A successful same-artifact retry retains its flaky outcome.

| Cell | State | Evidence and limits |
|---|---|---|
| Package, 27 skills and local contracts | static-tested | Merged main `94560c43bd4a5a062177870188f60a7ebafb5028`: historical 120 framework tests and seven checks passed on the identical reviewed integration tree. RC checks require their own receipts |
| Upstream inventory | static-tested | pstack 0.15.9; 161 responsibilities reconciled; delta 3 added / 18 changed / 0 removed. [Sync procedure](upstream/README.md); exact upstream benchmark link remains deferred |
| Claude historical cold load | observed-pass | WP1 fresh-session probe on its historical body |
| Claude project recipe invocation | observed-pass | Read-only native Skill invocation passed; two earlier unknown-skill probes retained |
| Claude verification generator invocation | observed-pass | Complete private candidate authored; this invocation wrote no consumer guide or ran a cycle |
| Claude full mode routing | deferred | Unrun; static review and generator invocation do not establish fourteen-playbook routing |
| Codex marketplace discovery/manual path | observed-pass | Historical discovery without installation, manual project-skill probes and direct-read fallback; WP2 planning preview: 11 routes/61 steps on its recorded head |
| Codex native install/invocation | blocked | Unrun; global installation outside recorded probe authority |
| Fresh RC host probes | authored | UNRUN pending recorded results; historical host passes do not bind this candidate |
| Native todo integration | blocked | Codex historical preview used displayed checklist fallback; native todo behavior unrun |
| Fresh host delegation and multi-turn persistence | authored | Guidance supplied; end-to-end native runtime behavior unrun |
| Applied generated-recipe cycle | blocked | Later approved guide body applied; 12 Android/eight iOS tests and five local journeys passed with retained failed attempts/fallback. Final iOS boot-state preservation unresolved; revised guide native invocation unrun. No full clean-cycle pass |
| Historical KMP shared navigation/header task | observed-pass | Android/iOS logic and native callers observed on bounded artifacts; older 11-test snapshot remains distinct from later 12-test reports |
| Historical CMP journey/header task | observed-pass | Android and two iOS runtime journeys, normal/enlarged text within recorded scope; successful attempts followed retained failures. Native Android enlarged text/forced ellipsis unrun; iOS bottom-tab clipping remains outside header scope |
| Android Jev labels | observed-pass | One approved run: 3/3 checkpoints, six claims, probabilities 0.98 to 0.99. Labels only; no new transmission or renewed authority |
| iOS Jev judgment | blocked | MobileBuildMCP driver conflicts with consumer's XcodeBuildMCP rule; local screen evidence remains separate |
| Native Swift build and selected Swift Testing tests | observed-pass | NetNewsWire at `626f08c3e5bf542a37f2bd59c65e13ffe0417bdf`: five methods/seven invocations PASS, zero failures/skips, Xcode 26.4.1/iOS 26.4.1. Historical; not rerun on Xcode 27. Approved hosted startup created default account/feed containers, retained |
| Native Swift feature task | authored | Selected existing tests are not a delegated feature or bug task, red-green proof or driven user path |
| Native Kotlin demo build and selected unit tests | observed-pass | Now in Android at `a49ed253d75e61a2b6ab80a8da677b57437b08eb`: offline demo build and nine SearchViewModel tests PASS, zero failures/errors/skips. Unit results historical and not rerun in Espresso 3.7 round |
| Native Kotlin selected UI tests | observed-pass | Five existing non-image search methods PASS in one Espresso 3.7 instrumentation attempt; zero fail/skip/unrun, Android 16/SDK 36 with empty minor field. Strict core/idling 3.7 dependency change limited to isolated AndroidTest configuration. Original Espresso 3.5 five initialization failures retained; changed APK/conditions are not a flaky retry |
| Native Kotlin feature task | authored | No feature/unit source change or feature red-green task; two image methods excluded from bounded UI scope |
| Layer 2, feature maps and CLI-first addition | deferred | Managed-worker runtime outside Layer 1; draft PR #2 remains post-first-release work |

PRs [#1](https://github.com/hugues-vnsgn/huguesStack/pull/1),
[#3](https://github.com/hugues-vnsgn/huguesStack/pull/3),
[#4](https://github.com/hugues-vnsgn/huguesStack/pull/4),
[#5](https://github.com/hugues-vnsgn/huguesStack/pull/5),
[#6](https://github.com/hugues-vnsgn/huguesStack/pull/6) and
[#7](https://github.com/hugues-vnsgn/huguesStack/pull/7) are merged.
[#2](https://github.com/hugues-vnsgn/huguesStack/pull/2) remains an open deferred
draft. Historical Opus/Fable reviews keep their original scope; new PR reviews
use independent **GPT-6 Astra High**, with actual final-head evidence. Read the
[PR review policy](../plugin/skills/hugues-mode/references/pr-review-policy.md).
Same-host review provides process independence, not cross-host proof.

The planned `how`, `why`, `architect`, `arena`, `tdd`, `blast-radius`, `swarm`,
`maintain-verification-skill`, `show-me-your-work`, `correct` and
`setup-huguesstack` leaves remain **unshipped**. They are planned 0.1.0 scope,
not already-approved deferred work. The owner must decide whether to accept a
reduced functional scope. The actual 27 skills/fourteen playbooks do not fill
that gap.

Four-domain feature-task coverage, native Swift/Kotlin red-green work, complete
mode routing/delegation/persistence and a full clean generated cycle remain
incomplete. The revised [plan](PLAN.md) permits an owner checkpoint with labelled
gaps; those gaps never become observed support. First-release readiness is
unestablished. Target remains **9 October 2026, end of day GMT+7**.

Historical [WP1](wp1-validation.md), [WP2](wp2-validation.md),
[WP3](wp3-validation.md) and [verification continuation](verification-continuation.md)
snapshots are preserved. Raw native artifacts stay outside the public repository.
