# Support evidence

WP3 development version `0.1.0-dev.3` adds the project verification-skill
generator, durable evidence guidance and jev integration contract. Package checks
establish static contracts; host discovery, judged verdicts and mobile support
require their own observed runs. The continuation results below are a bounded
5 October 2026 snapshot. WP3 and WP5 merged through
[PR #5](https://github.com/hugues-vnsgn/huguesStack/pull/5) and
[PR #4](https://github.com/hugues-vnsgn/huguesStack/pull/4). Their integrated main
`89e7125490a659a77381a3c12336abc56bb58dda` has tree
`280f42f14603f9e0b89b3a049ca8a3e831d43d88`, identical to reviewed integration
head `cdc44dc`. All 119 framework tests, upstream checks, package checks and
strict Claude validators passed; the integration Fable High re-review returned
CLEAN. [Verification continuation](verification-continuation.md) records the
later loader and Jev observations; [WP3 validation](wp3-validation.md) supplies
the reproducible package checks.

WP2 was merged through [PR #3](https://github.com/hugues-vnsgn/huguesStack/pull/3)
on 5 October 2026 at `b82431e46528b7b953f12ab35bc6c597993de934`.
Its merged tree equals tested head
`51ca48ef7a65751d7817f1fd5e985f986eaef6a2`. The 5 October full Codex
planning preview covered all eleven routes and all 61 numbered steps at that
head. Earlier previews below remain historical evidence for their stated heads;
they do not establish native mobile execution. WP1 loader results likewise cover
the historical WP1 package.

| Cell | State | Evidence or gap |
|---|---|---|
| WP1/WP2 manifests, skill metadata, paths and authored local links | static-tested | `./scripts/check-plugin.sh` passed on the WP2 working tree, 4 October 2026; 26 skills. One unchanged upstream benchmark-helper link is explicitly deferred and its bytes and provenance verified |
| WP3 generator metadata, project template and durable evidence links | static-tested | 86 framework tests passed on the WP3 working tree before WP5 integration, including package regressions for registration, metadata and reachable guides. These are historical static checks, not generated consumer recipe execution; exact-head checks belong in the WP3 PR |
| WP3 mobile-proof recipe handoff and build-doctor evidence contract | static-tested | Contract tests check direct reading of existing project recipes, evidence/jev links and authority boundaries; no model routing or repair behavior inferred |
| WP3 source receipts and jev operation names | static-tested | [Receipts](wp3-source-receipts.json) record the mixed input pins, installed 1.3.0 guide sections, tool names and observed CLI help; package-local destinations are checked. No callable bridge connection inferred |
| WP3 existing project recipe direct-read fallback | observed-pass | Fresh read-only Codex probe exited 0, read the canonical project guide and checked its Claude-directory symlink relationship. The native Skill tool was unavailable, so this establishes the direct-read fallback only |
| WP3 Claude project recipe native Skill invocation | observed-pass | Fresh Claude Code 2.1.286 session with project/local setting sources successfully invoked the existing recipe through the native Skill tool. Read-only loading only; no build or drive ran in that invocation. Two earlier isolated probes returned unknown-skill and remain failed attempts |
| WP3 Claude native generator invocation | observed-pass | Session-local plugin loading and direct `/hugues-stack:create-verification-skill` invocation exited 0 and authored a complete private candidate from the actual repository and template. No file write, build or drive ran in that invocation; candidate authorship and a full generated-recipe cycle remain separate |
| WP3 full generated-recipe execution cycle | authored | The private candidate has not been applied and driven through all generated Launch, Doctor, Drive, Evidence and Cleanup sections. Existing independently executed proof does not establish this cycle |
| WP3 Android Jev judged screen proof | observed-pass | Installed Jev 1.3.0 CLI completed one explicitly authorized version-1 run against the tested artifact: `ALL_CHECKPOINTS_PASSED`, 3/3 checkpoints and six label claims with claim probabilities 0.98 to 0.99, model `jev-1.13.0`. This covers placeholder navigation labels only; it does not judge clipping or selected state |
| WP3 iOS Jev judged screen proof | blocked | For the agreed WP3 consumer, the installed Jev driver uses MobileBuildMCP while that repository requires XcodeBuildMCP exclusively. Repository-compliant local iOS observations remain separate from a Jev verdict |
| WP1 package regressions | static-tested | All 27 original tests remain and passed with the WP2 package |
| WP2 routing table, 14 playbooks, four lanes and bounded worker | static-tested | 45 WP2 static contract and mutation tests passed; 72 total stdlib tests passed after the routing clarification, 4 October 2026. These check guidance, not model behavior |
| WP2 upstream source receipts and verbatim copies | static-tested | All 41 source receipts independently verified against the pstack 0.15.9 pin; 28 files copied verbatim, including all 24 principles. Full inline index and adapted mappings checked |
| WP2 Claude Code manifest acceptance | static-tested | Strict Claude plugin and marketplace metadata validators passed for `0.1.0-dev.2`; metadata acceptance only; see the separate static code review below |
| Historical WP2 Codex planning-only routing at `25c7a8a` | observed-pass | Codex 0.160.0, fresh manual project-skill session, exit 0: all eleven expected routes and domains matched, all 61 numbered playbook steps copied byte-for-byte; thirteen successful read-only skill-file reads, no delegates, writes or consumer commands. All 48 plugin fingerprints at that head matched the preview; the later routing clarification changed those bytes |
| Historical WP2 Codex affected-intent preview after WP2-R7 | observed-pass | Fresh Codex 0.160.0 manual project-skill session, exit 0: explanation selected investigation, verify-only selected mobile-proof; both domains matched and all nine numbered steps matched byte-for-byte. Two successful read-only commands read four skill/reference files; all 48 current plugin fingerprints matched. Displayed JSON checklist fallback only; no delegates, writes or consumer commands. A full eleven-case repeat timed out after 300 seconds before final JSON and was incomplete |
| WP2 exact-head full Codex preview at `51ca48e` | observed-pass | 5 October 2026, Codex 0.160.0 fresh manual project-skill session, exit 0: all eleven routes/domains and all 61 numbered steps matched byte-for-byte, thirteen successful read-only commands, all 48 plugin fingerprints matched. The merged PR #3 tree is identical. Displayed JSON checklist fallback; no delegates, writes or consumer commands |
| WP2 native todo integration | blocked | The Codex CLI preview exposed no native todo/plan tool. Its displayed JSON checklist fallback passed; native todo integration was unrun |
| WP2 Claude Code routing | deferred | Unrun. The owner now authorizes Claude Code review; a static code review does not establish routing behavior |
| WP2 fresh delegate and mode persistence | authored | Contracts supplied; native delegation and multi-turn persistence were unrun |
| WP1 Claude Code cold load and probe invocation | observed-pass | Claude Code 2.1.286, fresh `--plugin-dir` session, exact read-only probe reply, exit 0; historical WP1 body |
| WP1 Codex native marketplace discovery | observed-pass | [PR #1 reviewer](https://github.com/hugues-vnsgn/huguesStack/pull/1), 4 October 2026, Codex 0.160.0: local per-invocation override listed `hugues-stack@hugues-stack` as not installed; config unchanged; see [host loading](host-loading.md#codex) |
| Codex native install and skill invocation | blocked | Global installation is outside the present scope; native invocation remains unverified |
| WP1 Codex manual project skill probe | observed-pass | Codex 0.160.0, fresh scratch project and temporary `.agents/skills` discovery, exact read-only probe reply, exit 0; historical WP1 body |
| Swift/iOS independent app/test-bundle build | observed-pass | A separate existing native app and test bundle compiled through the permitted workflow with signing disabled on retry. Zero tests executed; no app install or launch occurred |
| Swift/iOS independent consumer feature proof | blocked | App-host startup would create default account/feed state and refresh. Additional startup authority is pending; a bundle build and the shared UI journey do not establish an independent Swift feature |
| Kotlin/Android independent demo build | observed-pass | A separate existing native app assembled its demo APK offline. No APK install or app startup occurred |
| Kotlin/Android independent consumer feature proof | blocked | The bounded offline test build requires three uncached pinned libraries. Zero unit or UI tests executed; dependency-download authority is pending. The demo build and shared UI journey do not establish an independent native Kotlin feature |
| WP3 bounded shared navigation/header tests on both targets | observed-pass | Initial bounded-proof snapshot, 5 October 2026: Android JVM: 11 assertions; iOS simulator: 8 assertions; zero skips in the inspected reports. Both target compilations and Android APK assembly passed. Results cover the agreed shared navigation/header task; later test counts, review heads, verdicts and final checks are recorded separately in the WP3 PR and private evidence |
| WP3 CMP journey through both native hosts | observed-pass | The existing shared navigation journey and bounded header change passed on an Android emulator and two iOS simulator runtimes. Android asserted the selected return state; iOS retained screenshots show it because that harness does not export a selected flag. Raw evidence remains private. Final passes follow retained failed/incomplete attempts, including an Android System UI ANR; this was not a clean first-attempt pass |
| WP3 bounded header layout and accessibility proof | observed-pass | iOS normal and app-local enlarged-text observations showed no header clipping at the tested widths. Android JVM regression checks used 320 dp, font scale 2 and a synthetic long title to check ellipsis, geometry, the accessible back control, its 48 dp minimum and its callback. These are bounded checks, not whole-UI certification; narrow/enlarged-text iOS observations exposed bottom-tab label clipping outside the approved header scope |
| WP3 cross-host static code review | observed-performed | Claude Code Fable High initial review completed; its five framework findings were adjudicated and fixed. Exact reviewed framework head `a7d64d3` returned CLEAN with Fable High after all five findings were fixed. The integrated tree received its own CLEAN re-review; static review does not establish native app support |
| Cross-host static code review | observed-performed | Claude Code 2.1.286 / `claude-opus-5-5`, plan permission mode: initial head `17ba517` returned `material-findings`; re-review of `25c7a8a` resolved all six findings and returned `no-material-findings`, with one low-severity routing clarification accepted. Both invocations exited 0. Completion and verdict are separate facts; see [review audit](reviews/wp2-claude-review.md). The final reviewed head and verification are recorded in [PR #3](https://github.com/hugues-vnsgn/huguesStack/pull/3) |
| WP5 full upstream inventory and sync tooling | static-tested | Public Git commits independently fetched: complete 158/161-file trees verify the exact 3 added / 18 changed / 0 removed delta. All 161 responsibilities reconciled with reasons and explicit implementation states; deterministic reports and pending proposals preserve adaptations. [Sync procedure](upstream/README.md) |
| WP5 cross-host static code review | observed-performed | Claude Code 2.1.286 / `claude-fable-5-1`, high effort, read-only public-code snapshot: initial `c29eeb3` review exited 0 with no material findings and four accepted low-severity corrections. Final reviewed head `7550c9e` returned no findings with Fable High and merged through PR #4; see [review audit](reviews/wp5-claude-review.md). Static review does not establish mobile support |
| WP5 pending upstream delta | deferred | None at the independently checked 0.15.9 main head `e43c7ee26e0038c6c1fa8380dd34ce86ff94cb2a`; future main changes require weekly manual triage and a new reviewed pin |

Use the plan's support states: authored, static-tested, observed-pass,
observed-fail, blocked and deferred. The review row uses observed-performed to
record review completion; its verdict is stated separately. Record run outcomes
as pass, fail, flaky, skipped or incomplete. The development package is not the 0.1.0 release candidate.

The owner authorizes the implementation → Claude Code review → adjudicated
fixes → tests → re-review workflow through first-release readiness. PRs #3, #4
and #5 merged with explicit authorization. PR #2 remains draft and unmerged.
The continuation authorizes bounded verification and separate new draft PRs.
Consumer publication, further PR merges and release publication remain outside
that scope. The four-domain personal-workflow bar is not yet established.

See [WP1 validation](wp1-validation.md) for historical probe evidence and
[WP2 validation](wp2-validation.md) for historical WP2 acceptance and
[WP3 validation](wp3-validation.md) for the current proof-lane boundaries. Feature
maps and the CLI-first verification addition remain post-first-release work;
current native, test and UI proof requirements stay in place.
