# Support evidence

WP2 adds authored routing, playbooks and mobile proof requirements. Static tests
check the package contracts; observed host and mobile support require separate
runs. Results below cover development version `0.1.0-dev.2` on 4 October 2026.
The initial WP2 checks and six-case preview describe head
`17ba517058e1f56b0ead6a53587cda375312bc45`; the Claude review and its follow-up
are recorded separately. The completed eleven-case preview covers
`25c7a8a77af4c5f7fe8f23fe16c14c98127647bf`, before the low-severity routing
clarification. Current static results and the final tested head are recorded in
[PR #3](https://github.com/hugues-vnsgn/huguesStack/pull/3). WP1 loader results
are historical evidence for WP1.

| Cell | State | Evidence or gap |
|---|---|---|
| WP2 manifests, skill metadata, paths and authored local links | static-tested | `./scripts/check-plugin.sh` passed on the WP2 working tree, 4 October 2026; 26 skills. One unchanged upstream benchmark-helper link is explicitly deferred and its bytes and provenance verified |
| WP1 package regressions | static-tested | All 27 original tests remain and passed with the WP2 package |
| WP2 routing table, 14 playbooks, four lanes and bounded worker | static-tested | 45 WP2 static contract and mutation tests passed; 72 total stdlib tests passed after the routing clarification, 4 October 2026. These check guidance, not model behavior |
| WP2 upstream source receipts and verbatim copies | static-tested | All 41 source receipts independently verified against the pstack 0.15.9 pin; 28 files copied verbatim, including all 24 principles. Full inline index and adapted mappings checked |
| WP2 Claude Code manifest acceptance | static-tested | Strict Claude plugin and marketplace metadata validators passed for `0.1.0-dev.2`; metadata acceptance only; see the separate static code review below |
| WP2 Codex planning-only routing at `25c7a8a` | observed-pass | Codex 0.160.0, fresh manual project-skill session, exit 0: all eleven expected routes and domains matched, all 61 numbered playbook steps copied byte-for-byte; thirteen successful read-only skill-file reads, no delegates, writes or consumer commands. All 48 plugin fingerprints at that head matched the preview; the later routing clarification changed those bytes |
| WP2 Codex affected-intent preview after WP2-R7 | observed-pass | Fresh Codex 0.160.0 manual project-skill session, exit 0: explanation selected investigation, verify-only selected mobile-proof; both domains matched and all nine numbered steps matched byte-for-byte. Two successful read-only commands read four skill/reference files; all 48 current plugin fingerprints matched. Displayed JSON checklist fallback only; no delegates, writes or consumer commands. A full eleven-case repeat timed out after 300 seconds before final JSON and was incomplete |
| WP2 native todo integration | blocked | The Codex CLI preview exposed no native todo/plan tool. Its displayed JSON checklist fallback passed; native todo integration was unrun |
| WP2 Claude Code routing | deferred | Unrun. The owner now authorizes Claude Code review; a static code review does not establish routing behavior |
| WP2 fresh delegate and mode persistence | authored | Contracts supplied; native delegation and multi-turn persistence were unrun |
| WP1 Claude Code cold load and probe invocation | observed-pass | Claude Code 2.1.286, fresh `--plugin-dir` session, exact read-only probe reply, exit 0; historical WP1 body |
| WP1 Codex native marketplace discovery | observed-pass | [PR #1 reviewer](https://github.com/hugues-vnsgn/huguesStack/pull/1), 4 October 2026, Codex 0.160.0: local per-invocation override listed `hugues-stack@hugues-stack` as not installed; config unchanged; see [host loading](host-loading.md#codex) |
| Codex native install and skill invocation | blocked | Global installation is outside the present scope; native invocation remains unverified |
| WP1 Codex manual project skill probe | observed-pass | Codex 0.160.0, fresh scratch project and temporary `.agents/skills` discovery, exact read-only probe reply, exit 0; historical WP1 body |
| Swift/iOS consumer proof | authored | Swift/XCTest/simulator lane supplied; observed app proof remains WP3/WP4 and needs consumer authority |
| Kotlin/Android consumer proof | authored | Kotlin/JUnit/emulator lane supplied; observed app proof remains WP3/WP4 |
| KMP shared logic proof on each target | authored | Common tests and native callers required separately on Android and iOS; no consumer run |
| CMP shared UI proof on each target | authored | Android and iOS UI observations plus semantics or text scaling required; no consumer run |
| Cross-host static code review | observed-performed | Claude Code 2.1.286 / `claude-opus-5-5`, plan permission mode: initial head `17ba517` returned `material-findings`; re-review of `25c7a8a` resolved all six findings and returned `no-material-findings`, with one low-severity routing clarification accepted. Both invocations exited 0. Completion and verdict are separate facts; see [review audit](reviews/wp2-claude-review.md). The final reviewed head and verification are recorded in [PR #3](https://github.com/hugues-vnsgn/huguesStack/pull/3) |
| WP5 full upstream inventory and sync tooling | static-tested | Public Git commits independently fetched: complete 158/161-file trees verify the exact 3 added / 18 changed / 0 removed delta. All 161 responsibilities reconciled with reasons and explicit implementation states; deterministic reports and pending proposals preserve adaptations. [Sync procedure](upstream/README.md) |
| WP5 cross-host static code review | observed-performed | Claude Code 2.1.286 / `claude-fable-5-1`, high effort, read-only public-code snapshot: initial `c29eeb3` review exited 0 with no material findings and four accepted low-severity corrections. Exact final-head verdict is recorded with the draft PR; see [review audit](reviews/wp5-claude-review.md). Static review does not establish mobile support |
| WP5 pending upstream delta | deferred | None at the independently checked 0.15.9 main head `e43c7ee26e0038c6c1fa8380dd34ce86ff94cb2a`; future main changes require weekly manual triage and a new reviewed pin |

Use the plan's support states: authored, static-tested, observed-pass,
observed-fail, blocked and deferred. The review row uses observed-performed to
record review completion; its verdict is stated separately. Record run outcomes
as pass, fail, flaky, skipped or incomplete. The development package is not the 0.1.0 release candidate.

The owner authorizes the implementation → Claude Code review → adjudicated
fixes → tests → re-review workflow through first-release readiness. PR #2 and
PR #3 remain unmerged pending authorization; release publishing and consumer
selection, edits or execution require their own authorization.

See [WP1 validation](wp1-validation.md) for historical probe evidence and
[WP2 validation](wp2-validation.md) for current acceptance boundaries. Feature
maps and the CLI-first verification addition remain post-first-release work;
current native, test and UI proof requirements stay in place.
