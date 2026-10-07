# huguesStack 0.2.0

Version 0.2.0 restores the complete pinned pstack 0.15.9 source and connects it to Claude Code and Codex through explicit host adapters. It adds a human developer tutorial for installation on another machine and a first mobile bug fix. The 0.1.0 release remains unchanged.

## Changes

- Preserve all 161 upstream files, paths and executable modes at pstack commit `e43c7ee26e0038c6c1fa8380dd34ce86ff94cb2a`, tree `54dfdd87fd191ddda7fce01dd354d220adaeeacc`.
- Register all 50 skills, 23 core playbooks and two agents. Four mobile playbooks compose mobile checks with the core procedures. Mobile-specific regression workers and blind comparison rules apply only to mobile tasks.
- Bind installed planning to the approved plugin files. Translate supported bundled paths into guarded workflow reads; preserve consumer-owned reads and reject unsupported command syntax.
- Make read-only worktree audits hold when activity is empty, malformed, unsupported or incomplete, or candidate PR/merge state is unknown. Recognize supported punctuation, encoded paths and filesystem case identity. Detect duplicate JSON keys, excessive nesting, added core files and changed permissions.
- Keep the two-Astra-reviewer PR policy scoped to development of huguesStack itself. Installing it does not impose that policy on another project.

Start with the [developer guide](DEVELOPER-GUIDE.md). Existing users should install the new tag or use a separate 0.2.0 checkout, then open a fresh host session. A live program bound to older plugin files must be paused and reconciled before changing its installation.

## Validation and limits

The package validation baseline is 349 Python tests, separated into 131 frozen 0.1.0 contracts, 27 current-checker cases with historical fixtures, 94 current source/contract/helper cases and 97 installed adapter/regression cases. The release verification asset records the exact release candidate, final checks and independent reviews. Core and upstream checks verify the immutable source; strict Claude validation checks both manifests. The separate offline helper suite contains 52 Bun tests and strict TypeScript checking for watch-pr, using local fixtures and approved cached dependencies.

The bounded native trial at restored-source head `de6f1ec7231ea5771fbc37c016fae6df0b17839a` used Claude Code 2.1.290 and Codex 0.160.1. Claude discovered all 50 plugin commands, but isolated startup/authentication prevented complete planning. Codex failed during startup. Raw Claude CLI stream output and empty Codex output produced conservative audit holds; neither established compatibility with real persisted host transcripts. Controller-driven workflow rereads passed separately and are not native planning evidence. No private history was scanned and no worktree was deleted.

Complete restored workflow execution, native Codex plugin installation, fresh-machine final-release loading, mobile device/simulator behavior, whole-map verification maintenance and live forge/cloud/loop work remain unverified. Historical mobile observations in 0.1.0 apply only to their recorded revisions. The owner approved this release with these limits documented; additional native trials are not a release gate. Source equality is not runtime equality.

The cleanup helper is read-only. Complete inputs still confer no deletion authority, and a separate active/pinned-chat check remains required. Missing dependencies or unavailable model/tool capabilities remain blocked steps, not implied support. No dependency installation, device change or external action follows merely from installing the instructions.

## Downloads

The release includes a source archive, this developer guide as a standalone Markdown file, a source hash inventory, a validation receipt and `SHA256SUMS`. Verify the downloaded assets before using them:

```sh
shasum -a 256 -c SHA256SUMS
```

Run that command from the folder containing all listed release assets. The hashes detect download changes; they are not a separate signing or trust service. See the [test accounting](TEST-COVERAGE.md) and [restoration contract](CORE-RESTORATION.md) for detailed boundaries.
