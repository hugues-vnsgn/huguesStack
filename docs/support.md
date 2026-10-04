# Support evidence

WP2 adds authored routing, playbooks and mobile proof requirements. Static tests
check the package contracts; observed host and mobile support require separate
runs. Current results below cover development version `0.1.0-dev.2` on
4 October 2026. WP1 loader results are historical evidence for the WP1 revision.

| Cell | State | Evidence or gap |
|---|---|---|
| WP2 manifests, skill metadata, paths and authored local links | static-tested | `./scripts/check-plugin.sh` passed on the WP2 working tree, 4 October 2026; 26 skills. One unchanged upstream benchmark-helper link is explicitly deferred and its bytes and provenance verified |
| WP1 package regressions | static-tested | All 27 original tests remain and passed with the WP2 package |
| WP2 routing table, 14 playbooks, four lanes and bounded worker | static-tested | 27 new static contract and mutation tests passed; 54 total stdlib tests passed on the WP2 working tree, 4 October 2026. These check guidance, not model behavior |
| WP2 upstream source receipts and verbatim copies | static-tested | All 41 source receipts independently verified against the pstack 0.15.9 pin; 28 files copied verbatim, including all 24 principles. Full inline index and adapted mappings checked |
| WP2 Claude Code manifest acceptance | static-tested | Strict Claude plugin and marketplace metadata validators passed for `0.1.0-dev.2`; no external Claude model run |
| WP2 Codex planning-only routing | observed-pass | Codex 0.160.0, fresh manual project-skill session, exit 0: all six expected routes and domains matched, all 38 numbered playbook steps copied byte-for-byte; eight read-only skill-file reads, no delegates or consumer commands |
| WP2 native todo integration | blocked | The Codex CLI preview exposed no native todo/plan tool. Its displayed JSON checklist fallback passed; native todo integration was unrun |
| WP2 Claude Code routing | deferred | Unrun; external Claude model invocation is outside this work package's authority |
| WP2 fresh delegate and mode persistence | authored | Contracts supplied; native delegation and multi-turn persistence were unrun |
| WP1 Claude Code cold load and probe invocation | observed-pass | Claude Code 2.1.286, fresh `--plugin-dir` session, exact read-only probe reply, exit 0; historical WP1 body |
| WP1 Codex native marketplace discovery | observed-pass | [PR #1 reviewer](https://github.com/hugues-vnsgn/huguesStack/pull/1), 4 October 2026, Codex 0.160.0: local per-invocation override listed `hugues-stack@hugues-stack` as not installed; config unchanged; see [host loading](host-loading.md#codex) |
| Codex native install and skill invocation | blocked | Global installation is outside the present scope; native invocation remains unverified |
| WP1 Codex manual project skill probe | observed-pass | Codex 0.160.0, fresh scratch project and temporary `.agents/skills` discovery, exact read-only probe reply, exit 0; historical WP1 body |
| Swift/iOS consumer proof | authored | Swift/XCTest/simulator lane supplied; observed app proof remains WP3/WP4 and needs consumer authority |
| Kotlin/Android consumer proof | authored | Kotlin/JUnit/emulator lane supplied; observed app proof remains WP3/WP4 |
| KMP shared logic proof on each target | authored | Common tests and native callers required separately on Android and iOS; no consumer run |
| CMP shared UI proof on each target | authored | Android and iOS UI observations plus semantics or text scaling required; no consumer run |
| Cross-host review | deferred | Guidance supplied; no other-host review run. Fresh same-host review establishes process independence only |
| Full upstream inventory and weekly sync | deferred | WP2 inputs verified at `e43c7ee26e0038c6c1fa8380dd34ce86ff94cb2a`; full reconciliation remains WP5 |

Use the plan's states: authored, static-tested, observed-pass, observed-fail,
blocked and deferred. Record run outcomes separately as pass, fail, flaky,
skipped or incomplete. The development package is not the 0.1.0 release candidate.

See [WP1 validation](wp1-validation.md) for historical probe evidence and
[WP2 validation](wp2-validation.md) for current acceptance boundaries. Feature
maps and the CLI-first verification addition remain post-first-release work;
current native, test and UI proof requirements stay in place.
