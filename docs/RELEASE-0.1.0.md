# 0.1.0 release candidate

**Candidate: `0.1.0-rc.1`, 6 October 2026.** This is prerelease metadata and
review documentation for a separate draft RC PR based on merged main
`94560c43bd4a5a062177870188f60a7ebafb5028`. It does not create or approve a merge,
0.1.0 tag, GitHub release or first-release readiness. Target remains
**9 October 2026, end of day GMT+7**.

## What is included

Layer 1 contains 27 skills: `hugues-mode`, `interrogate`,
`create-verification-skill` and 24 verbatim pstack principles. The router includes
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
| Fresh RC host probes | **UNRUN pending recorded results**; must bind actual candidate bytes and host version. No future head or pass is assumed |
| Approved generated-recipe cycle | Guide body applied; fresh 12 Android/eight iOS tests and five local journey passes. Failures/fallback retained; final iOS boot-state preservation unresolved, revised guide native invocation unrun. No full clean-cycle PASS |
| Swift native slice | NetNewsWire five methods/seven invocations PASS, zero failures/skips on historical Xcode 26.4.1/iOS 26.4.1. Approved startup created retained default feed/account containers; not rerun on Xcode 27 |
| Kotlin native slice | Historical nine SearchViewModel unit tests PASS; new strict Espresso core/idling 3.7 round: five non-image UI methods PASS in one instrumentation attempt on Android 16/SDK 36, empty minor field. Original Espresso 3.5 five failures preserved; changed APK is a distinct run |
| Kotlin preparation | 21 artifact rows/25 components/15 core edges and offline APK build; 159 local mocked guard/resolver fixtures, distinct from framework and native assertion counts |

Native tests in this table exercise existing tests. They do not establish new
Swift/Kotlin features, bug fixes or feature red-green proof. Local shared UI
journeys and the single historical Android Jev label judgment have bounded
scope; iOS Jev remains blocked by the consumer's tool policy. No new external
judgment, consumer run or consumer edit occurs in this documentation package.

## Decisions and remaining gaps

The owner plan includes functional leaves that are still **unshipped**:
`how`, `why`, `architect`, `arena`, `tdd`, `blast-radius`, `swarm`,
`maintain-verification-skill`, `show-me-your-work`, `correct` and
`setup-huguesstack`. Accepting a reduced 0.1.0 scope requires an owner decision;
these planned leaves are not silently reclassified as approved deferred work.

Four-domain feature-task completeness and native Swift/Kotlin red-green/driven
paths remain incomplete. Complete mode routing, native delegation, todo
integration and multi-turn/compaction persistence remain unproven. Fresh revised
guide invocation and a clean applied cycle remain unproven. Cross-host reviews
retain their historical scope; same-host independent review supplies process
independence only. The owner's personal-workflow checkpoint may retain labelled
gaps, but correctness of reporting remains required.

## Candidate validation record

Fresh static checks, host receipts and independent final-head review must be
recorded against the actual RC. Historical 119/120 framework counts and native
results cannot be promoted to fresh candidate checks. Until those receipts are
attached, this section records **pending coordinator validation**, with fresh
host probes **UNRUN**. Use the [host-loading methods](host-loading.md) and run:

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
