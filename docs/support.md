# Support evidence

WP2 adds authored routing, playbooks and mobile proof requirements. Static tests
check the package contracts; observed host and mobile support require separate
runs. Results below cover development version `0.1.0-dev.2` on 4 October 2026.
The initial WP2 checks and six-case preview describe head
`17ba517058e1f56b0ead6a53587cda375312bc45`; the Claude review and its follow-up
are recorded separately. Corrected WP2 static checks and the eleven-case preview cover the working
tree containing the six review fixes; the final tested head is recorded in
[PR #3](https://github.com/hugues-vnsgn/huguesStack/pull/3). WP1 loader results are historical evidence for WP1.

| Cell | State | Evidence or gap |
|---|---|---|
| WP2 manifests, skill metadata, paths and authored local links | static-tested | `./scripts/check-plugin.sh` passed on the WP2 working tree, 4 October 2026; 26 skills. One unchanged upstream benchmark-helper link is explicitly deferred and its bytes and provenance verified |
| WP1 package regressions | static-tested | All 27 original tests remain and passed with the WP2 package |
| WP2 routing table, 14 playbooks, four lanes and bounded worker | static-tested | 44 WP2 static contract and mutation tests passed; 71 total stdlib tests passed on the corrected WP2 working tree, 4 October 2026. These check guidance, not model behavior |
| WP2 upstream source receipts and verbatim copies | static-tested | All 41 source receipts independently verified against the pstack 0.15.9 pin; 28 files copied verbatim, including all 24 principles. Full inline index and adapted mappings checked |
| WP2 Claude Code manifest acceptance | static-tested | Strict Claude plugin and marketplace metadata validators passed for `0.1.0-dev.2`; metadata acceptance only; see the separate static code review below |
| WP2 Codex planning-only routing | observed-pass | Codex 0.160.0, fresh manual project-skill session, exit 0: all eleven expected routes and domains matched, all 61 numbered playbook steps copied byte-for-byte; thirteen successful read-only skill-file reads, no delegates, writes or consumer commands. Current plugin fingerprints matched the preview |
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
| Cross-host static code review | observed-pass | Claude Code 2.1.286 / `claude-opus-5-5` reviewed head `17ba517` in plan permission mode: exit 0, 30 Read/Glob/Grep calls, no tool errors. Six findings were accepted for correction. The exact final reviewed head and verdict are recorded in [PR #3](https://github.com/hugues-vnsgn/huguesStack/pull/3); see [review audit](reviews/wp2-claude-review.md) |
| Full upstream inventory and weekly sync | deferred | WP2 inputs verified at `e43c7ee26e0038c6c1fa8380dd34ce86ff94cb2a`; full reconciliation remains WP5 |

Use the plan's states: authored, static-tested, observed-pass, observed-fail,
blocked and deferred. Record run outcomes separately as pass, fail, flaky,
skipped or incomplete. The development package is not the 0.1.0 release candidate.

The owner authorizes the implementation → Claude Code review → adjudicated
fixes → tests → re-review workflow through first-release readiness. PR #2 and
PR #3 remain unmerged pending authorization; release publishing and consumer
selection, edits or execution require their own authorization.

See [WP1 validation](wp1-validation.md) for historical probe evidence and
[WP2 validation](wp2-validation.md) for current acceptance boundaries. Feature
maps and the CLI-first verification addition remain post-first-release work;
current native, test and UI proof requirements stay in place.
