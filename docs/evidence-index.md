# Evidence index

This is the current documentation snapshot on **6 October 2026** for prerelease
candidate **`0.1.0-rc.2`**. [Support](support.md) summarizes cells;
[WORKFLOW](WORKFLOW.md) explains how to start a task. Raw consumer reports,
screenshots, device identifiers, credentials and machine paths stay private.
Receipt identifiers and hashes below allow the owner to check retained private
packets; those bytes are not public downloads. Historical native slices below
remain distinct from the later [RC2 native feature proof](rc2-native-feature-proof.md).
This documentation update runs no consumer command.
PRs #6 and #7 are merged into main `94560c43bd4a5a062177870188f60a7ebafb5028`.
The RC does not establish first-release readiness or create a tag/release.

## Framework and host receipts

| Work | Public receipt | Binding and outcome |
|---|---|---|
| WP1 package/loaders | [PR #1](https://github.com/hugues-vnsgn/huguesStack/pull/1), [validation](wp1-validation.md), [host methods](host-loading.md) | Merged. 27 historical tests; Claude cold-load probe and Codex manual probe passed. Codex marketplace discovery observed; native installation/invocation unrun |
| WP2 mode/playbooks | [PR #3](https://github.com/hugues-vnsgn/huguesStack/pull/3), [validation](wp2-validation.md), [Claude review audit](reviews/wp2-claude-review.md) | Merged tree equals tested `51ca48ef7a65751d7817f1fd5e985f986eaef6a2`. 72 tests and Codex planning-only preview: 11 routes, 61 steps. No delegated mobile execution inferred |
| WP5 upstream sync | [PR #4](https://github.com/hugues-vnsgn/huguesStack/pull/4), [sync procedure](upstream/README.md), [Claude review audit](reviews/wp5-claude-review.md) | Merged `76f13b791cbefd984a028cad2841ce867165d012`; reviewed `7550c9e` CLEAN. Pin 0.15.9, 161 responsibilities; 3 added / 18 changed / 0 removed |
| WP3 integrated proof lane | [PR #5](https://github.com/hugues-vnsgn/huguesStack/pull/5), [validation](wp3-validation.md), [source receipts](wp3-source-receipts.json) | Merged `89e7125490a659a77381a3c12336abc56bb58dda`; tree `280f42f14603f9e0b89b3a049ca8a3e831d43d88` equals tested/reviewed integration `cdc44dc`. 119 framework tests and package/upstream/strict metadata/shell/whitespace checks passed; Fable High CLEAN after fixes |
| Verification continuation and review policy | [PR #6](https://github.com/hugues-vnsgn/huguesStack/pull/6), [head-bound receipt](https://github.com/hugues-vnsgn/huguesStack/blob/b2d75a0085429d25827f663ed99fd1f872707be0/docs/verification-continuation.md), [review policy](https://github.com/hugues-vnsgn/huguesStack/blob/b2d75a0085429d25827f663ed99fd1f872707be0/plugin/skills/hugues-mode/references/pr-review-policy.md) | Merged as `831eee9419c076b90abbfd76106a55c951100180`. Original head `b2d75a0085429d25827f663ed99fd1f872707be0`: 120 framework tests and checks passed; independent Astra High final-head review CLEAN. Original receipt remains a distinct pre-integration snapshot |
| WP6 combined documentation integration | [PR #7](https://github.com/hugues-vnsgn/huguesStack/pull/7) | Merged main `94560c43bd4a5a062177870188f60a7ebafb5028`, tree `1525d353d7928e39f53f8f0025931e4e2f9f320e` identical to tested/reviewed `c4966f2e0a3038303bebb232e04ed2297508feed`. Historical 120 framework tests and seven checks PASS; independent Astra High final-head CLEAN |
| Historical RC1 initial static checks/review | [RC notes](RELEASE-0.1.0.md), [validation receipt](rc-validation.md) | `5af676e7486291fbfac1fb81263c2aecec629476`: fresh 120 framework tests/seven checks PASS; independent Astra High CLEAN. Historical RC1 result; it does not validate RC2 |
| Historical RC1 host probes | [validation receipt](rc-validation.md), [host methods](host-loading.md) | Claude 2.1.290 native session-local load and Codex 0.160.1 manual fallback: each 16 read-only cases/15 routes/87 exact steps; original eleven fixture domain/proof matches. Supplemental domain limit retained. 54 plugin fingerprints unchanged, bound to `21a82942019292f7212ff1185e9ef187ac96e86d` plugin bytes; no RC2 coverage. Fresh bounded scratch delegation/artifact review PASS; 22 outer-worker assertions and 14 independent coordinator checks PASS, recorded separately. Initial setup denial retained |
| Retained foundation/research/design/verification | [PR #9](https://github.com/hugues-vnsgn/huguesStack/pull/9), [PR #10](https://github.com/hugues-vnsgn/huguesStack/pull/10), [PR #11](https://github.com/hugues-vnsgn/huguesStack/pull/11), [PR #12](https://github.com/hugues-vnsgn/huguesStack/pull/12), [integration](retained-integration.md) | Separate open drafts; reviewed heads and source receipts remain distinct from the unmerged combined RC2 proposal. Verification head `f126656d2718084de8292cda0cb40b81333e4d6e`: 152 framework tests/seven checks PASS; independent Astra High CLEAN, with no host execution claim |
| RC2 host continuation | [RC2 receipt](rc2-host-validation.md), [host methods](host-loading.md) | `e2ff899`: Claude native session-local load and Codex manual project skills; each 16 routes/87 steps. Both original replies inferred unsupported Kotlin. Bounded synthetic RED/GREEN, design, static recipe loading and cold read-only pickup are recorded with separate limits. Private manifest `d4d6195bcb59d26db8db2fd88038de62b44fbdf570829f0b3d9cbb082ba3c898` |
| RC2 lane-evidence revision | [RC2 receipt](rc2-host-validation.md#lane-evidence-probes), [fixture](../tests/fixtures/rc2-lane-evidence.json) | `dba645fa3adc024487c1137486a81b31e12ec832`: 178 framework tests/seven checks PASS, clean before/after. Six cases per host/variant and 36 copied steps each; candidate semantic language/lane observations supported, all initial strict fixture comparisons FAIL. Adjudication accepted checker false positives and required target-component evidence/declaration anchors; raw failures remain. Independent review was pending at that initial snapshot; later routing-head review is separate. No general compliance claim |
| RC2 repaired lane previews | [Repaired schema receipt](rc2-host-validation.md#repaired-schema-probes) | Each host passed six unique cases/36 copied steps with corrected uncommitted bytes at `dba645f`. All 79 hashes subsequently match committed `68cb710`; map `ef3a077823f42ea2490bced4f5fe1bf13618fd8b15c11ba96ea87d8bdf222b1a`. Revised prompt protocol; planning-only, no clean-head invocation/full workflow claim |
| RC2 routing candidate checks/review | [Final routing binding](rc2-host-validation.md#committed-routing-binding) | `68cb710e709260317cb7023c84394abc9cc537f6`, tree `41dcde6fbe6330aec21ec6570fe70b107ba69da9`: 194 framework tests/seven checks PASS, clean before/after; independent same-host Astra High CLEAN. Later documentation heads and fresh probes require separate receipts |
| RC2 S1/K1 feature continuation | [Native feature proof](rc2-native-feature-proof.md) | S1 actual RED/pause/pickup/GREEN, recipe and maintenance assertion phases observed; original continuity/boot-state gaps prevent full clean-cycle acceptance. K1 actual RED/pause/pickup/unit GREEN and built APK; all new device/recipe/maintenance runs blocked |
| Selected combined RC2 delivery | [PR #13](https://github.com/hugues-vnsgn/huguesStack/pull/13), [integration](retained-integration.md#delivery-path) | Remote observed OPEN/DRAFT on main at `e2ff899`; later local candidate unpublished. PRs #8–#12 remain open drafts as the alternative stack; no close/merge is implied |
| Deferred additions | [PR #2](https://github.com/hugues-vnsgn/huguesStack/pull/2), [plan](PLAN.md) | Open draft at `4f032119f887407885a5e90851633d1887cc57cc`; consumer feature maps and CLI-first verification remain post-first-release work |

Historical Opus/Fable reviews remain evidence for their stated revisions. New PR
reviews use independent GPT-6 Astra High. Static review proves neither host
routing nor native app behavior. The merged integration counts above are historical; fresh RC checks and review must
bind the actual candidate. Main's merge receipt is `2026-10-05-pr6-pr7-merge`,
with both original PR heads retained as ancestors of the integrated tree.

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

## Later approved generated-recipe cycle

The earlier supported-slice blockers in [verification continuation](verification-continuation.md)
remain historical facts. Later owner approval allowed the reviewed canonical
guide body to be applied and bounded local tests/screens to run. The retained
receipt `2026-10-05-bfs-approved-cycle` records **12/12 fresh Android tests,
8/8 fresh iOS tests**, recorded builds and **five local journey passes**.
Wide iOS normal text passed through a reviewed tool fallback after two failed
standalone taps; those attempts remain visible. Same-artifact retries retain
flaky classification. The original guide metadata/symlink and app source,
tests and configuration were preserved.

This is a partial applied cycle, not a full clean-cycle PASS. Final preservation
of the two iOS simulators' boot state is **blocked/unestablished**: both were
Shutdown at the final observation, cause unknown, with no shutdown command in
the cycle. Native Android enlarged text and native forced ellipsis were unrun;
synthetic overflow/text-scale regressions passed. Enlarged iOS bottom-tab
clipping remains outside the header scope. A reviewed exact 24-byte Android
runtime-cache exception means an all-files-unchanged claim would be false.
Fresh native-host invocation of the revised guide body remains unrun.

A material initial artifact-binding finding was corrected by retaining distinct
iOS debug-dylib and full-bundle identities; identical launcher stubs alone did
not bind linked implementation. The frozen V2 packet received independent
same-host Astra High CLEAN for evidence accuracy and integrity. Manifest
SHA-256: `37dc544430a5a7ec335cb42cf4ba2848eba174803ea1703f7fdf0efeb57b2566`
(1,340 entries). This review did not grant full-cycle or release readiness.
No new Jev/TypeSafe judgment occurred. Earlier preflight diagnostics delivery
remains unknown; inspected optout controls are not network telemetry.

## Native Swift observations

NetNewsWire baseline: `626f08c3e5bf542a37f2bd59c65e13ffe0417bdf`.
The approved hosted test slice recorded **five methods/seven invocations PASS**,
zero failures or skips, on **Xcode 26.4.1 / iOS 26.4.1**. This is historical and
was not rerun or reinterpreted under Xcode 27. Hosted startup was approved to
create default account/feed state; newly created temporary containers were
retained. Owned app processes and private MCP were observed absent afterward.
The original checkout remained clean. These existing tests do not establish
an implemented Swift feature/bug task, red-green proof or a driven user path.

Receipt: `2026-10-05-native-expanded-scope`, corrected V3 manifest SHA-256
`d504e996f8b6c87fe926318b09a22ad88d7e3f6ee631a4b9fb083afb752cd60d`
(190 entries), independent same-host Astra High CLEAN for corrected historical
evidence accuracy/integrity. Original and intermediate receipts are preserved.

## Native Kotlin observations and changed conditions

Now in Android baseline: `a49ed253d75e61a2b6ab80a8da677b57437b08eb`.
Its original checkout remains clean. The offline demo APK build is historical.
Later direct approval superseded the initial automatic-review blocker for
additional pinned dependency roots. The root-level blocked outcome remains a
historical snapshot; the later attempt receipts carry actual execution results.
Nine existing **SearchViewModel tests PASS**, zero failures/errors/skips, in
attempt receipt `20261005T213353-additional-android-offline-unit-4vhbekgq`.
JUnit XML SHA-256: `a6a2dfa5ded1d424583317374f1b389b18ddfb5ce73691790f6b0de38de25cb7`;
assessment: `d645139ebce8fa27979981ee019df9e44fcfc2737e3c367c10a5073a127497ae`.
These unit tests were not rerun in the later UI rounds.

Retained dependency/build attempts exposed additional cache prerequisites.
The original Espresso 3.5 UI round then executed five selected methods, all
**FAIL** during initialization on actual Android 16/SDK 36. The instrumentation
command's exit 0 was not a test pass. Its 173-entry manifest SHA-256 is
`2aad9a9c8905358a4cc3919f16aa95781f612181e625695b68c0d55543dc7371`;
independent CLEAN reviewed the failure packet's reporting, not UI success.

Receipt `2026-10-06-espresso37-round-v1` records a new, changed-APK round:
**five PASS, zero FAIL/SKIP/UNRUN/INCOMPLETE/INVALID**, in a single instrumentation
attempt on **Android 16 / SDK 36, empty SDK minor field**. Only the isolated
`feature/search/impl/build.gradle.kts` AndroidTest implementation configuration
changed, with exact strict Espresso core/idling **3.7.0**; production, unit and
UI source remained unchanged. The original configuration backup was retained.
The new APK SHA-256 is
`ee6fd16b10109f57b33ad13ddde42b45975d55c11a007c9ff37d986f351ffaf0`.
Original five failures remain preserved; this changed configuration/artifact
is a distinct run, not a flaky retry of the original APK.

The dependency receipt reopens **21 artifact rows, 25 reachable components
and 15 core dependency edges**; these are graph/artifact counts, not new download
counts. Offline APK assembly passed (369 tasks: 170 executed, 199 from cache).
The **159 local mocked resolver/guard fixtures** are preparation checks, distinct
from **120 historical framework tests** and the five actual native UI methods.
Two image methods were intentionally excluded. Analytics optout is code-verified,
while analytics classes remain; no zero-network observation is claimed.

Owned package uninstall and positive absence, owned emulator-process absence
and source preservation are retained in frozen receipts. Final independent
same-host Astra High review was CLEAN for bounded result/evidence integrity;
its fresh process query was sandbox-blocked, so cleanup confirmation relies on
frozen exact-process receipts. The final manifest contains 295 entries,
SHA-256 `a9422e4f32f73a368b3c94e31eb7bb5ca6edd50502982b78e00d5486396878d8`;
assessment SHA-256 `a9859e2d6870c3f234c069ae3dcf359e1d8ecddbdde0a741b777d66873cdc8e0`.
No native feature completion, cross-host or release-readiness proof is inferred.

## Current RC2 scope and evidence limits

The shipped package is **35 skills, fourteen playbooks and one worker**, with
**79 plugin files**. The owner approved eight retained leaves for 0.1.0 on 6 October 2026:
`how`, `why`, `architect`, `arena`, `tdd`, `blast-radius`,
`maintain-verification-skill` and `correct`. All eight are authored and
static-tested, with direct playbook handoffs in RC2. The same approval defers
`swarm`, `show-me-your-work` and `setup-huguesstack` to 0.2. Feature maps,
CLI-first verification and Layer 2 retain their existing deferred scope.
Bounded synthetic observations cover portions of five retained tools; full
eight-workflow adherence remains unproven. Later [native feature proof](rc2-native-feature-proof.md)
adds bounded Swift execution and Kotlin logic/build evidence.

Native Swift and Kotlin RED/GREEN tasks and actual checkpoint-only pickup are
observed. Kotlin device proof, four-domain task completeness, full mode execution,
compaction/native persistent todos and a clean generated cycle remain incomplete.
S1 recipe assertions passed; the historical shared-guide cycle keeps its own gaps.
Historical cross-host reviews retain their exact scope; new same-host reviews
cannot supply fresh cross-host workflow proof. Historical RC1 host previews and bounded scratch delegation are recorded in the
[receipt](rc-validation.md), bound to its 54 files at `21a82942019292f7212ff1185e9ef187ac96e86d`.
Those RC1 observations leave full execution unrun and cover no changed RC2 body.
The later [RC2 receipt](rc2-host-validation.md) records fresh loading, previews,
bounded synthetic work, historical lane-evidence comparison failures and later
[repaired schema previews](rc2-host-validation.md#repaired-schema-probes). Full eight-workflow
adherence remains unproven. The [integration receipt](retained-integration.md)
records package heads and static contracts. Record RC2 exact-head checks and
independent review in its separate draft proposal before publication; no future
SHA or verdict is assumed. The revised [plan](PLAN.md) allows labelled gap
reasons at the owner's checkpoint, without converting them to support.
No merge, tag or release is established by this RC. Deadline remains
**9 October 2026, end of day GMT+7**.
