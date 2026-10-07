# huguesStack maintainer reference

This reference describes the core restoration shipped in 0.2.0. Start with the [developer guide](DEVELOPER-GUIDE.md) to install and use it. The 0.1.0 guide and release remain historical; their host/mobile evidence does not cover these loaders. The pin remains pstack 0.15.9 at `e43c7ee26e0038c6c1fa8380dd34ce86ff94cb2a`.

## Load the intended checkout

Use a fresh Claude Code session in the intended consumer repository:

```sh
claude --plugin-dir /absolute/path/to/huguesStack/plugin
```

Verify discovery of hugues-mode and use the registered command the host exposes. The manifest name is hugues-stack. The 0.2.0 manifest identifies this release; verify the actual checkout path/revision as well as the cache/version label. Bounded development Claude discovery has been observed at its recorded head; a later checkout still needs its own invocation evidence.

For Codex, use an already-authorized native loader when available. Otherwise read `/absolute/path/to/huguesStack/plugin/skills/hugues-mode/SKILL.md` and all required links in full. Label direct reads separately from native discovery. These instructions authorize no host configuration changes or installations.

Functional entrypoints load host adapter → mobile applicability → full pinned core. Principles remain verbatim. Reread relevant files after compaction if the contract is no longer available in context.

## State a task and follow its route

```text
/hugues-mode reproduce the Swift list jump on the named iOS simulator, then fix it
/hugues-mode explain why this Kotlin search code uses that boundary
/hugues-mode change this KMP boundary; prove Android and iOS callers
/hugues-mode compare this CMP screen on both targets including text scaling
```

Give the consumer path/revision, authorized actions and observable result. Intent precedes language: lifecycle, authoring, review, investigation and verification retain their routes. Native implementation uses core playbooks; KMP/CMP use named extensions. Large/cross-cutting/unmatched work uses figure-it-out; standing programs use Orchestrate. Mobile proof becomes a phase of that designed workflow.

The coordinator reads the selected public bridge and full core, copies ordered todos, grounds/designs, delegates fresh rounds and independently checks actual artifacts. Feature work with multiple valid shapes requires arena. For mobile arena work, candidates get sanitized fresh contexts and isolated write paths; the judge gets neutral artifacts/rubric after writers finish. Missing isolation blocks blind judging.

## Configure roles explicitly

Pinned defaults remain defaults. Optional project-local `.huguesstack/models.md` overrides roles; deleting a role restores its source default. `/setup-huguesstack` detects exposed models, loads state, asks for budget/role choices, validates and writes only after confirmation and authority. Restoring the plugin does not execute setup.

Budgets remain unlimited/max, large/xhigh, medium/high and small/medium. Panel lists launch one worker per entry, aliases included. Explicit auto/inherit-parent aliases omit model overrides; they never silently replace all defaults. Rejected slugs follow the core fallback using confirmed capabilities. Report actual models/efforts, blocked seats and process independence separately from family diversity.

Generic interrogate keeps its pinned Claude/GPT/Grok panel or configured list, sends the same prompt/rubric, synthesizes adjudicated findings and does not auto-fix. PR-bound huguesStack work adds the [two-seat Astra High policy](../plugin/policies/astra-pr-review.md): exact candidate head, fixes, checks and fresh re-review. Launch acceptance does not attest to backend settings or completion.

## Prove the actual mobile behavior

Establish language, native/shared ownership and target from source and the request. Preserve unknowns; Gradle syntax alone does not establish language. Record plugin/consumer revisions, target/runner, actual commands/exits and surviving artifacts. A build is not behavior proof; skipped tests and wrong targets do not pass.

Mobile bug work uses a fresh regression worker and independently observed RED against unfixed production, then a separate production worker and GREEN on the same regression. The core practical-test exception retains a concrete reason and closest useful verification. Shared changes need both affected targets.

Generation interviews the repository and writes launch/doctor/drive/evidence/cleanup/helpers. It seeds features/README.md and the top 3–5 user-facing feature files, then proves one mapped feature end to end. Translate the Cursor example layout to the existing `.claude/skills` or `.agents/skills` convention. Preserve user edits. An unexecuted recipe remains a draft.

Maintenance covers the whole map: source readers, reconciliation/source-only omissions, serial live proof of every mapped feature, doctor/recovery, one drift retry and evidence-preserving cleanup. Outcomes are clean/changed/blocked. An opt-in one-journey diagnostic is bounded-mobile coverage and cannot satisfy whole-map maintenance.

Read [lane rules](../plugin/skills/hugues-mode/references/mobile-lanes.md), [evidence guide](../plugin/skills/hugues-mode/references/evidence-guide.md) and [Jev transmission rules](../plugin/skills/hugues-mode/references/jev-drive.md). Consumer edits/execution and data transmission use current owner scope. No consumer app is bundled.

## Long work and publication

Long/autonomous work keeps the pinned append-only TSV trail, ownership start rows, evidence pointers and superseding corrections. Audit only the current run against its available transcript. Missing native transcript/cross-family review is an explicit audit gap. Use pause-safely/session-pickup to reconstruct actual state and preserve evidence.

Helpers live in the immutable core. Inspect local runtime/cache/authority first. Bun bootstrap may install packages; do not run it without installation scope. Missing cloud, loop, forge or model capability blocks dependent work. Shipping does not gain merge authority from green tests.

For planning and cleanup, use the [installed host commands](../plugin/adapters/host-tools.md). Save the approved payload binding when authoring a program. Fill and translate bundled plan operands, validate with `plan-check`, and reread workflows through that binding at every required tick. Payload/adapter drift blocks the program; consumer-owned files still come from consumer trunk. The native worktree audit takes an explicit authorized source manifest and local PR snapshot. Incomplete activity coverage holds candidates. The separate active/pinned-chat gate remains required before any prune decision; the helper never deletes or discovers private transcript directories.

Opening a PR retains ready-PR and stack/base mechanics. Prepare local commits/body when authorized; push/publication/merge/release need separate scope. Do not replace a blocked ready gate with a draft fallback.

## Change and validate the plugin

Edit adapters/project policy for host/mobile translations, never the pinned source. Core upgrades are separate. Render loaders with `python3 scripts/render_core.py`; update provenance/reviewed adapter receipts deliberately, then test and review semantic boundaries.

```sh
python3 -m unittest discover -s tests -v
./scripts/check-plugin.sh
python3 scripts/check_core.py
python3 scripts/upstream-diff.py check
python3 scripts/check_whitespace.py
```

Source checks reconstruct the pinned Git snapshot and verify all 161 names/modes/hashes plus the shipped runtime manifest and reviewed adapter assets. Development tests cover source, phases/cardinality/fallback, active wiring, bounded overrides and helpers. Installed adapter tests use external disposable consumer directories and synthetic native transcripts. Frozen release tests cover historical contracts only; [test accounting](TEST-COVERAGE.md) separates these roots. Passing static checks cannot attest to unrun host/mobile journeys.

See [restoration scope](CORE-RESTORATION.md) and [historical support](support.md). All upstream responsibilities stay in the ledger, including all 50 registered top-level skills, both native agent definitions and the separate Benny service source. Registration of automate-me or make-bot-ui grants no authority for personal transcript processing or bot/webhook execution. TypeScript guidance remains available alongside mobile adapters.

The native Comment Sicko wrapper loads its complete pinned rules for no-comments. KMP/CMP extensions compose the selected core action procedure and require implementation arena within step 3 when Feature has multiple valid shapes; design-only arena cannot satisfy that gate. Both wiring failures have phase-local mutation regressions.
