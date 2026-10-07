# Python test roots and evidence limits

The suite has 317 independently collected unittest cases. Its previous 252-case
result and this result must not be described as wholly current native workflow
coverage. Subtest scenarios are not added to the case total.

| Group | Cases | Root and evidence |
|---|---:|---|
| Historical release contracts | 131 | Frozen SHA256-bound 0.1.0 archive; historical behavior only |
| Current checker with historical fixtures | 27 | Current package checker over release-derived mutation fixtures |
| Development contracts and helpers | 94 | Current checkout, provenance and source/wiring mutations; some compare released contracts |
| New installed operational adapters | 65 | Current plugin copied to an installed directory; disposable external consumers and synthetic transcript sources |
| Total | 317 | Sum of the four distinct groups |

The historical modules are test_wp2_contract (45), test_wp3_contract (15),
test_retained_design (7), test_retained_research (8), test_retained_verification
(6), test_retained_integration (26) and test_lane_evidence (24). Their module-level
root is `release_root()`. test_check_plugin contributes the 27 mixed checker cases.
test_core_restoration (50), test_retained_provenance (11) and test_upstream_sync
(33) contribute the 94 current development cases.

test_host_adapters contributes 14 installed planning/binding cases, 40 synthetic
activity/parser cases and eleven actual Git consumer audit integration cases. It
exercises unchanged Node validation through the public helper, bound workflow
rereads and translations from outside the plugin, paths with spaces, installations
without Git, payload/adapter drift and required-file/runtime failures. Activity
fixtures cover Claude Code and Codex independently and together, nested
subagents, encoded function arguments, relative context, timestamps, exact path
boundaries, missing/malformed/unsupported/partial sources, simulated permission
errors, relative sibling shell/patch operands, per-operation/relative working directories, chained Git directory changes, nested-progress, unknown-tool, message/file-input, nested-result and nonoperative content schema holds, opaque sed programs, unsupported-host ignore/coverage guards, opaque-command holds, malformed tool/source inputs, symlinks, WIP/PR holds and the separate active/pinned-chat gate.

All native transcript fixtures are task-owned synthetic files. Permission errors
are injected; denied private paths are never accessed. No real history is scanned
and no worktree is deleted. These cases establish supported adapter behavior,
not every native host format, complete real-world activity coverage or automatic
deletion safety. Full worker/workflow dispatch, arena, native mobile RED/GREEN,
whole-map maintenance and live forge/cloud/loop journeys require their own
authorized, revision-bound proof.

The separate Bun result is 52 tests (not 52 plus the earlier 40-test subset).
Strict TypeScript checking covers watch-pr. The offline helper tests use fake
forge readers/local Git fixtures, so their result is not live forge evidence.
