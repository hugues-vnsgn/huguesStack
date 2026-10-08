# Python test roots and evidence limits

The candidate collects **337 top-level unittest cases**. One is a driver that
separately executes **50 frozen 0.2.0 restoration cases**. Do not add the driver
and its children as independent coverage, or describe historical passes as current
native workflow proof. Subtests are not added to case totals.

| Group | Collected cases | Evidence |
|---|---:|---|
| Historical 0.1.0 contracts | 131 | Unchanged SHA256-bound release archive |
| Current checker, historical 0.1.0 fixtures | 27 | Explicit historical validation mode and package mutations |
| Historical 0.2.0 restoration driver | 1 | Executes 50 cases inside a separate hash-bound archive |
| Current source/provenance checks | 44 | test_upstream_sync (33), test_retained_provenance (11) |
| Current installed adapters and regressions | 97 | test_host_adapters (72), test_review_regressions (12), test_rereview_regressions (13) |
| Current native-layout contracts | 29 | test_native_layout; canonical source, permissions, invocation boundaries and budgets |
| Current progressive-disclosure contracts | 8 | test_context_disclosure; retained rules, mandatory phase reads, complete declared source inventories and bound resources |
| Total collected | 337 | Current, mixed and historical scopes remain distinct |

The 131 historical modules are test_wp2_contract (45), test_wp3_contract (15),
test_retained_design (7), test_retained_research (8), test_retained_verification (6),
test_retained_integration (26) and test_lane_evidence (24). Their root is
`release_root()`. No frozen archive was modified to make a current test pass.
The newly retained 0.2.0 archive is the original `509cbec` Git tree, not the
candidate layout. Its 50 restored-contract cases remain historical evidence.
Main collected 349 cases. Moving those 50 behind one driver and adding 29
native-layout plus eight disclosure cases gives 337, without dropping the frozen
50 executions or counting them twice. The preceding native candidate had 329.

Current adapter cases execute the public installed Python entrypoint in disposable
external consumer directories, including Node plan validation when available.
Bindings cover canonical files, metadata, adapters, policies, runtime code and
full permission modes. Tests reject missing/extra files, symlinks, changed modes,
bootstrap execution before verification, poisoned bytecode caches, consumer path
ownership errors and unsupported shell shapes. Public SKILL.md reads and aliases
are explicitly rejected in favor of native invocation; tests do not simulate a
successful host permission decision.

The unchanged activity parser is exercised with synthetic Claude/Codex records,
relative contexts, malformed/unsupported inputs, empty sources, duplicate/deep
JSON and unknown PR metadata. Candidate-specific holds and exit 2 remain required.
The active/pinned-chat gate stays separate. No real transcript was read and no
real worktree was deleted.

Native-layout cases compare all 50 public names and modes, archive/source identity,
canonical mapping, workflow phase/cardinality/fallback constraints, immutable
manual-only policy, consumer boundaries and a measured source-context budget.
Hash resealing cannot approve a lost phase gate or changed invocation policy.
Invocation metadata checks use effective fields, rejecting duplicate fields and
comment decoys. Plans containing only bound workflow reads pass the plan gate
without an incidental consumer Git read; missing binding markers still fail.
The budget uses bytes and characters/4; it is not measured host context.

Current host discovery/invocation, complete persisted-transcript compatibility,
worker dispatch, mobile device journeys and forge/cloud/loop execution remain
unverified. Earlier native observations are bound to their original revisions.
Historical Bun/TypeScript helper results remain separate from any new candidate
run recorded in the implementation evidence.
Their source and dependency inputs remain unchanged; the Node plan checker did
change and has current Python/Node integration coverage. The current Bun/TypeScript
run was blocked before execution by sandbox preflight `EPERM`. See the
[helper input receipt](HELPER-INPUTS.json) and [context report](CONTEXT-FOOTPRINT.md).
