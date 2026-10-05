# Evidence index

This is the authoritative navigation and status snapshot for WP6 documentation
on **5 October 2026**. [Support](support.md) summarizes the cells;
[WORKFLOW](WORKFLOW.md) explains how to start a task. Raw consumer reports,
screenshots, identifiers, credentials and machine paths stay private. Public
summaries below are coordinator-observed receipts, with their limits retained.
They are historical evidence, not new executions by this documentation package.
This combined checkout includes PRs #6 and #7. Publication states below describe
pre-integration snapshots; exact integration checks and current merge state
belong in those PR receipts.

## Framework and host receipts

| Work | Public receipt | Binding and outcome |
|---|---|---|
| WP1 package/loaders | [PR #1](https://github.com/hugues-vnsgn/huguesStack/pull/1), [validation](wp1-validation.md), [host methods](host-loading.md) | Merged. 27 historical tests; Claude cold-load probe and Codex manual probe passed. Codex marketplace discovery observed; native installation/invocation unrun |
| WP2 mode/playbooks | [PR #3](https://github.com/hugues-vnsgn/huguesStack/pull/3), [validation](wp2-validation.md), [Claude review audit](reviews/wp2-claude-review.md) | Merged tree equals tested `51ca48ef7a65751d7817f1fd5e985f986eaef6a2`. 72 tests and Codex planning-only preview: 11 routes, 61 steps. No delegated mobile execution inferred |
| WP5 upstream sync | [PR #4](https://github.com/hugues-vnsgn/huguesStack/pull/4), [sync procedure](upstream/README.md), [Claude review audit](reviews/wp5-claude-review.md) | Merged `76f13b791cbefd984a028cad2841ce867165d012`; reviewed `7550c9e` CLEAN. Pin 0.15.9, 161 responsibilities; 3 added / 18 changed / 0 removed |
| WP3 integrated proof lane | [PR #5](https://github.com/hugues-vnsgn/huguesStack/pull/5), [validation](wp3-validation.md), [source receipts](wp3-source-receipts.json) | Merged `89e7125490a659a77381a3c12336abc56bb58dda`; tree `280f42f14603f9e0b89b3a049ca8a3e831d43d88` equals tested/reviewed integration `cdc44dc`. 119 framework tests and package/upstream/strict metadata/shell/whitespace checks passed; Fable High CLEAN after fixes |
| Verification continuation and review policy | [PR #6](https://github.com/hugues-vnsgn/huguesStack/pull/6), [head-bound receipt](https://github.com/hugues-vnsgn/huguesStack/blob/b2d75a0085429d25827f663ed99fd1f872707be0/docs/verification-continuation.md), [review policy](https://github.com/hugues-vnsgn/huguesStack/blob/b2d75a0085429d25827f663ed99fd1f872707be0/plugin/skills/hugues-mode/references/pr-review-policy.md) | Draft at the WP6 review snapshot, `b2d75a0085429d25827f663ed99fd1f872707be0`. 120 framework tests and package/upstream/strict metadata/shell/whitespace checks passed; independent Astra High final-head review CLEAN. Distinct pre-integration head; its changes are included in this combined checkout |
| Deferred additions | [PR #2](https://github.com/hugues-vnsgn/huguesStack/pull/2), [plan](PLAN.md) | Open draft at `4f032119f887407885a5e90851633d1887cc57cc`; consumer feature maps and CLI-first verification remain post-first-release work |

Historical Opus/Fable reviews remain evidence for their stated revisions. New PR
reviews use independent GPT-6 Astra High. Static review proves neither host
routing nor native app behavior. WP6's own tests and review belong in
[PR #7](https://github.com/hugues-vnsgn/huguesStack/pull/7) at its final reviewed
head; the 119/120 counts above are not WP6 results.

## Bounded shared-task observations

The later WP3 snapshot retained **12 Android JVM and eight iOS logic tests**,
plus the existing bounded placeholder navigation journey on Android and two
iOS simulator runtimes under normal and enlarged text. The earlier
[WP3 validation snapshot](wp3-validation.md#observed-bounded-proof) records
11 Android assertions; these are distinct report sets. Successful journey
attempts followed retained failures/incomplete attempts, including a System UI
ANR. Same-artifact/condition retries that subsequently pass retain a flaky
outcome; separate changed-condition or incomplete attempts remain visible.

Header checks covered the tested widths, Android 320 dp/font scale 2, ellipsis,
back-control geometry and callback. iOS selected return state relied on retained
screenshots because the harness exported no selected flag. Bottom-tab clipping
observed under narrow/enlarged text remains outside the agreed header scope.
This is bounded KMP/CMP task evidence, not general UI certification or independent
Swift/Kotlin feature proof.

Later, one approved Android Jev run returned `ALL_CHECKPOINTS_PASSED`: **3/3
checkpoints**, six label claims, probabilities **0.98 to 0.99**, model `jev-1.13.0`
through the installed 1.3.0 CLI. The approved checkpoint payload was transmitted
to TypeSafe; screenshots/logs stayed local. Its authority is consumed. This
judgment covers labels only; geometry, accessibility and selected state keep
their local evidence. iOS Jev judgment remains blocked by the bundled
MobileBuildMCP driver conflicting with the consumer's XcodeBuildMCP-only rule.

Claude's native project Skill invocation passed in a fresh read-only session;
two earlier isolated probes returned unknown-skill. A separate native generator
invocation authored a private candidate. Codex's direct-read fallback passed.
These observations do not establish a full applied generated-recipe cycle.

## Latest supported slice and remaining gates

The later private supported-slice handoff records a **partial/blocked** cycle:

| Check | Actual outcome |
|---|---|
| Android/iOS compilation and Android debug APK | PASS, cached/up-to-date |
| Fresh iOS logic reports | 8/8 PASS: seven navigation/resource cases plus one platform case; zero failures/errors/skips/duplicate identities; exact-target and standalone=false guards inspected |
| Private offline helper/guard checks | 12 isolated fixtures and four mock guard scenarios passed |
| New Android test task | 12 BLOCKED/unrun: missing cached `org.robolectric:android-all-instrumented:17-robolectric-15733970-i7` (API37); no download performed |
| Canonical guide application | BLOCKED/unrun; guide-only approval question pending |
| New native screen checks | BLOCKED/unrun; bounded-screen approval question pending. Automatic approval review rejected the action and its one permitted authority-reconciliation retry before execution; no further retry |
| Source preservation and cleanup | All seven owned consumer paths unchanged, including guide/metadata/symlink; one task-owned private Gradle daemon stopped; approved simulators remained booted |
| Final receipt review | Independent Astra High supported-slice review and authority-retry audit addendum CLEAN; no authority grant or screen proof inferred |

No app install/launch, emulator startup or new TypeSafe transmission occurred in
that slice. The candidate/helper review does not establish canonical-guide
application. Historical shared-task passes remain valid for their older
artifacts and reports; they do not fill these fresh blocked cells.

The private handoff and execution evidence were reopened for this index. They
retain command argv/cwd/scoped environment, report timestamps and identities,
source hashes, failed attempts, cleanup and review receipts. Offline controls
were inspected; they are not independent network telemetry.

## Separate native-domain prerequisites

| Domain/application | Completed | Blocked or unrun |
|---|---|---|
| Swift/iOS, NetNewsWire | App and test bundle built with signing disabled on retry | Zero tests; no install/launch. Hosted startup creates default account/feed state and may refresh; additional runtime authority pending |
| Native Kotlin/Android, Now in Android | Offline demo APK assembled | Zero unit/UI tests; no install/launch. Offline test build lacked `kotlin-test 2.3.0`, `androidx.test:rules 1.7.0-rc01`, `hilt-android-testing 2.59`; dependency-download authority pending |

These dependencies are separate from the agreed shared-UI consumer's API37 cache
gap. Existing bounded test approval for those native apps excludes the pending
runtime/download exceptions. Resolve each prerequisite before its dependent
execution; serialize authorized device runs. Independent documentation and
static review can proceed in parallel. Full applied-recipe and four-domain task
coverage remain incomplete. The owner may consider a release checkpoint with
labelled reasons under the revised [plan](PLAN.md); WP6 neither claims readiness
nor authorizes a release tag. The later owner-approved integration and merge of
PRs #6 and #7 requires its own exact-head tests and review; native scope
expansions remain pending.
