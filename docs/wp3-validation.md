# WP3 proof lane validation

WP3 adds `create-verification-skill` and connects the existing mobile-proof and
build-doctor playbooks to durable evidence and jev Drive guidance. It ships
Markdown, with no result parser, runtime or evidence schema. Consumer-local
recipes, scripts and private proof artifacts stay outside this public package.

## Scope

Use `/hugues-stack:create-verification-skill` in Claude Code or read the leaf
directly through the loaded Codex project skill path. The generator honors the
consumer's canonical skill layout under `.claude/skills` or `.agents/skills`,
preserves existing files, writes one agreed journey and requires execution before reporting the
recipe as observed on a target. Registration is checked separately from file
creation. Existing project recipes are read directly by mobile-proof, with
commands and selectors checked against current authority. Repository-supported
symlinks require resolution and loader checks; regular copies require hash
synchronization. A missing compliant tool leaves the check blocked.

The existing mobile-proof and build-doctor playbooks remain the mode's routes;
WP3 adds no duplicate routing leaves. Screen proof composes the installed
jev-ios-bridge `test-ios` and `test-android` skills. Repository tool restrictions
govern every fallback. Screen text may go to TypeSafe under the bridge's data
policy only within existing explicit authority or newly obtained acceptance;
private reports and screenshots remain local. A jev text verdict and a
visual layout observation support different claims.

## Static checks

Run:

```sh
./scripts/check-plugin.sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
sh -n scripts/check-plugin.sh
claude plugin validate --strict ./plugin
claude plugin validate --strict ./.claude-plugin/marketplace.json
git diff --check
```

WP3 regression tests run the actual package checker on copied packages. They
verify that the new leaf registers with valid metadata and that its local guide,
evidence and playbook links stay reachable. Mutations remove a required linked
file, corrupt the generator's frontmatter or break an anchor; the checker must
reject each altered package. These are static package regressions, not native
execution, semantic model behavior or an evidence validator.

The existing 72 tests continue to check WP1/WP2 metadata, routing contracts,
verbatim principle bytes, lane requirements and bounded delegation. Exact
working-tree results and later exact-head reviews belong in the PR; this
document supplies the reproducible checks rather than claiming a future pass.

The WP3 working tree before WP5 integration had 86 passing tests. This records
that historical run; integrated checks, final commits and exact-head reviews
must be recorded separately before a clean review or release claim.

## Scoped host and native acceptance

Exercise these cases in a fresh host session and inspect the actual output:

| Case | Expected behavior |
|---|---|
| Create a project-local verification recipe for one agreed journey | Discover repo facts, choose the current host loader directory, preserve existing work, write bounded Launch/Doctor/Drive/Evidence/Cleanup sections |
| Tool config names an MCP server but no tools are exposed | Record access as unproven; do not infer a working connection |
| Repository requires an Xcode MCP tool and that tool is unavailable | Keep iOS blocked; do not use prohibited raw CLI commands |
| Existing permitted CLI exposes the required tool operation | Discover its documented entry point and use it only within repo instructions and task scope |
| Jev is unavailable but repository permits a UI harness | Drive with that harness, retain action/outcome evidence, label no judged verdict |
| Only one KMP/CMP native host runs | Claim only its observed checks; retain the other host and independent Swift/Kotlin features as unproven |
| Exit zero, skipped tests, a flaky retry or wrong-target report | Inspect assertion/target provenance; retain incomplete/skipped/flaky/excluded results rather than claiming clean passing assertions |
| Cleanup follows an observed journey | Remove only authorized owned state, then reopen retained logs/reports/screenshots |

A host preview tests planning behavior only. Native proof requires the selected
app artifact, target tests, user actions and observations on the actual native
hosts. Current consumer selection and authorization come from the active task,
not historical plan examples. Per-task native results remain in private evidence;
public updates contain only separately authorized sanitized framework claims.

## Observed bounded proof

The initial bounded-proof snapshot from 5 October 2026 records an existing shared
navigation journey and a bounded shared-header change exercised through an
Android emulator and two iOS simulator runtimes. Retained native journey attempts
passed. Android asserted the selected return state; the iOS
harness did not export a selected flag, so retained screenshots support that
observation. The inspected test reports contain 11 Android JVM assertions and
8 iOS simulator assertions, with zero skips. Both target compilations and
Android APK assembly passed. Later test counts, review heads, verdicts and final
checks are recorded separately in the WP3 PR and private evidence; these
observations do not establish independent Swift or native Kotlin
feature implementations, or general KMP/CMP support.

The header was observed without clipping at the tested iOS widths under normal
and app-local enlarged text. Android JVM regression checks use a 320 dp width,
font scale 2 and a synthetic long title to exercise ellipsis and geometry, along
with the accessible back control, its 48 dp minimum and its callback. These checks
cover the header only. Narrow/enlarged-text iOS observations also exposed
bottom-tab label clipping outside the approved change scope; the whole UI is
not reported as passing.

Raw proof remains private, including screenshots, target provenance and the
failed or incomplete attempts before the final passes. Those attempts include
an Android System UI ANR and harness errors. A successful final attempt does
not turn that sequence into a clean first-attempt pass. There is **no judged
verdict**: bridge credentials were unavailable to the process and no jev MCP
tools were exposed. The authorized native harness observations therefore
remain separate from jev screen judgments.

A fresh read-only Codex project-guide probe exited 0, read the canonical guide
and checked its Claude-directory symlink relationship. The native Skill tool
was unavailable, so the probe used the documented direct-read fallback. It did
not exercise native Skill-tool invocation or invoke the generator to create a
recipe. Claude Code Fable High performed an initial framework review; its five
findings were adjudicated and fixed. Final review heads, verdicts and checks are
recorded separately in the WP3 PR and private evidence; this document does not
claim a clean final verdict.

## Provenance and limits

[Source receipts](wp3-source-receipts.json) record the exact readable inputs.
The generator adapts the verified local pstack 0.15.5 snapshot; WP5 owns the full
0.15.9 re-pin and ledger. Its feature-map phase is intentionally omitted because
feature maps remain post-first-release work. The hstack references are conceptual
inputs only; no managed-worker machinery is imported. The jev integration reads
version 1.3.0 installed skills but executes against the current available bridge.

This package alone does not establish host loader behavior, judged verdicts,
mobile runtime support or first-release readiness. Record each observed run,
blocked prerequisite and review separately. No consumer publication, automatic
merge, release publication, installation or system changes follow from these
instructions.
