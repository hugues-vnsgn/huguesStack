# 0.1.0 release candidate

**Candidate: `0.1.0-rc.2`, 6 October 2026.** This is prerelease metadata and
review documentation for owner-selected combined draft
[PR #13](https://github.com/hugues-vnsgn/huguesStack/pull/13), based on merged main
`94560c43bd4a5a062177870188f60a7ebafb5028`. It does not create or approve a merge,
0.1.0 tag, GitHub release or first-release readiness. Target remains
**9 October 2026, end of day GMT+7**.

## What is included

Layer 1 contains 35 skills: `hugues-mode`, `interrogate`,
`create-verification-skill`, eight approved retained tools and 24 verbatim pstack
principles. [Retained integration](retained-integration.md) records their
playbook handoffs and separately reviewed package heads. The router includes
fourteen playbooks; `hugues-agent` supplies the fresh-worker guidance. Package
and upstream-check scripts, workflow documentation and the responsibility ledger
are included. Consumer app source stays outside the plugin. MIT attribution and
pstack's license notice are preserved; upstream pin remains pstack 0.15.9 at
`e43c7ee26e0038c6c1fa8380dd34ce86ff94cb2a`.

PRs #1, #3, #4, #5, #6 and #7 are merged. PR #2 remains an open draft at
`4f032119f887407885a5e90851633d1887cc57cc`: consumer feature maps and CLI-first
verification remain post-first-release work. Layer 2 managed workers and the
other explicit deferred responsibilities remain outside this candidate.

## Evidence at this checkpoint

The [evidence index](evidence-index.md) preserves exact historical bindings and
packet hashes. The [support matrix](support.md) distinguishes observed behavior
from authored guidance and gaps.

| Evidence | Scope and limit |
|---|---|
| Merged integration | Historical 120 framework tests and seven checks PASS on the reviewed tree; independent Astra High CLEAN. These are not fresh RC results |
| Host observations | Historical Claude cold load/project recipe/generator and Codex manual planning/discovery passes retain their original revisions |
| Historical RC1 initial static validation/review | `5af676e7486291fbfac1fb81263c2aecec629476`: fresh 120 framework tests and seven checks PASS; independent Astra High CLEAN. This is historical RC1 evidence, not RC2 validation |
| Historical RC1 host previews | Claude 2.1.290 native session-local load / actual `claude-opus-5-5`; Codex 0.160.1 manual fallback, actual served model unconfirmed. Each 16 cases/15 routes/87 exact numbered steps; original eleven fixture domain/proof matches. Supplemental Android language limitation and displayed checklist fallback retained |
| Historical RC1 bounded synthetic delegation | Fresh registered Claude worker wrote one scratch function; fresh Explore reviewer read actual source, no behavior defects. 22 outer-worker assertions and 14 independent coordinator checks PASS separately on the same artifact. Initial ineffective permission rule/denial retained as setup failure; no platform automatic-review rejection. No full mode/mobile/red-green/persistence proof |
| Approved generated-recipe cycle | Guide body applied; fresh 12 Android/eight iOS tests and five local journey passes. Failures/fallback retained; final iOS boot-state preservation unresolved, revised guide native invocation unrun. No full clean-cycle PASS |
| Swift native slice | NetNewsWire five methods/seven invocations PASS, zero failures/skips on historical Xcode 26.4.1/iOS 26.4.1. Approved startup created retained default feed/account containers; not rerun on Xcode 27 |
| Kotlin native slice | Historical nine SearchViewModel unit tests PASS; new strict Espresso core/idling 3.7 round: five non-image UI methods PASS in one instrumentation attempt on Android 16/SDK 36, empty minor field. Original Espresso 3.5 five failures preserved; changed APK is a distinct run |
| Kotlin preparation | 21 artifact rows/25 components/15 core edges and offline APK build; 159 local mocked guard/resolver fixtures, distinct from framework and native assertion counts |
| RC2 routing repair | `68cb710`: 194 framework tests/seven checks PASS, independent same-host Astra High CLEAN; all 79 repaired-probe plugin hashes bind to committed bytes. Six unique planning cases/36 steps per host; no clean-head invocation claim |
| RC2 S1 Swift feature | Actual seven-case RED/pause/fresh pickup, separate guarded Shift-Return change. GREEN/recipe/maintenance each 12 methods/14 invocations, zero fail/skip, four inspected native bar images, Xcode 27/iOS 26.4.1. Synthetic delegate/selector dispatch; cleanup/continuity limits prevent full clean-cycle acceptance |
| RC2 K1 Kotlin feature | Actual 15-case RED with three intended failures; pause/fresh pickup and separate normalization fix, 15/15 unit GREEN. Offline UI-test APK built after a retained compile failure and corrected retry. Six new native selectors/four checkpoints and recipe/maintenance all blocked/unrun |

Historical native slices exercise existing tests. The later
[RC2 feature receipt](rc2-native-feature-proof.md) records the separate S1/K1
RED/GREEN work and its bounded surfaces. Local shared UI
journeys and the single historical Android Jev label judgment have bounded
scope; iOS Jev remains blocked by the consumer's tool policy. No new external
judgment, consumer run or consumer edit occurs in this documentation package.

## Decisions and remaining gaps

The owner approved eight retained leaves for 0.1.0 on 6 October 2026:
`how`, `why`, `architect`, `arena`, `tdd`, `blast-radius`,
`maintain-verification-skill` and `correct`. All eight are authored and
static-tested, with direct playbook handoffs in RC2. The same approval defers
`swarm`, `show-me-your-work` and `setup-huguesstack` to 0.2. Feature maps,
CLI-first verification and Layer 2 retain their existing deferred scope.
Bounded native Swift execution and Kotlin logic/build proof are observed; full
adherence of the eight workflows remains unproven.

Kotlin device proof and four-domain feature-task completeness remain incomplete.
Actual pause/checkpoint-only pickup and resumed GREEN are observed; full mode
execution, native todo integration and compaction/general persistence remain
unproven. S1 recipe assertions passed, with original data continuity and
simulator boot-state restoration unresolved. A full clean applied cycle remains
unproven; the historical shared-guide invocation gap is separate. Cross-host reviews
retain their historical scope; same-host independent review supplies process
independence only. The owner's personal-workflow checkpoint may retain labelled
gaps, but correctness of reporting remains required.

## Candidate validation record

The [RC validation receipt](rc-validation.md) records historical RC1 host observations,
plugin fingerprint binding and historical RC1 initial-candidate static checks/review. Historical
119/120 framework counts and native results remain distinct. Host probes began
with an uncommitted RC manifest; their 54-file fingerprints identify the tested
RC1 plugin bytes at `21a82942019292f7212ff1185e9ef187ac96e86d`, rather
than the recorded base SHA alone. RC2 has 79 plugin files and changed mode and
playbooks. The [RC2 host receipt](rc2-host-validation.md) records fresh bounded
loading, planning and synthetic observations plus repaired-probe byte binding
to `68cb710`. That routing head passed 194 framework tests/seven checks and
independent Astra High review. The later documentation candidate remains local
and unpublished; its exact-head checks, independent Astra High review and any
fresh host probes are UNRUN at this writing. Publication is blocked pending
direct owner authorization. [Delivery alternatives](retained-integration.md#delivery-path)
remain separate. No future head or final pass is assumed. Use the
[host-loading methods](host-loading.md) and run:

```sh
./scripts/check-plugin.sh
python3 -m unittest discover -s tests -v
python3 scripts/upstream-diff.py check
claude plugin validate --strict ./plugin
claude plugin validate --strict ./.claude-plugin/marketplace.json
```

Raw receipts, test reports, screenshots, machine paths and device identifiers
remain private. Historical `wp*-validation` and verification-continuation files
are provenance snapshots; current status is here and in the evidence index.
