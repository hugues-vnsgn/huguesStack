# huguesStack 0.3.0

Version 0.3.0 gives each of the 50 skills one native `SKILL.md`, cuts huguesStack's share of the host's skill list from 9,844 characters to 366, restructures the `hugues-mode` router, hardens plan translation and replaces Cursor model rules with native model roles. It is a new layout, so it does not continue 0.2.0 installs or program bindings. Versions 0.1.0 and 0.2.0 and their evidence remain unchanged.

## Changes

- **Native layout (#17).** Each skill owns `plugin/skills/<name>/SKILL.md`, with its references and helpers beside it. The runtime core mirror, the generated loaders and the custom registry are gone. All 161 pstack 0.15.9 files keep their exact bytes and modes in a provenance archive outside runtime discovery, checked against the upstream Git objects. Public skill names, the two aliases, 23 generic playbooks, four mobile playbooks, two agents and 15 worker roles are unchanged. Payload schema 2 and the new layout are incompatible with 0.2.0: old program bindings are rejected and must be rebound after review.
- **Skill list (#23).** The model-invocable skills drop from 46 to 2, and their description characters from 9,844 to 366. Only `hugues-mode` and `setup-huguesstack` stay model-invocable. The other 48 are user-only: the owner can still type each one by name, and the router reads it as a file with the host's own file-read tool.
- **Router (#24).** The `hugues-mode` body is restructured within pstack's section layout and its four Cursor-only frontmatter fields are gone. The description puts mobile first and renders whole in Codex (236 of 236 characters; the earlier 312-character text was cut at 243). Section pointers and the principles index are checked.
- **Safety.** One reach rule in `plugin/adapters/host.md` states how an agent reaches each kind of skill: a host file read for a bundled user-only skill, native invocation for `hugues-mode`, `setup-huguesstack` and consumer or external skills. A native-reach lint in `check_core.py` rejects agent-facing text that contradicts it, with a corpus of reviewed contradictions. The installed runtime still rejects every `SKILL.md` read.
- **Plan translation (#25).** A plan line that names a `SKILL.md` through `./`, `../`, letter case, repeated slashes, quotes or backslashes is refused, for `cat`, `sed`, `git show` and the plan-check forms. Known limit: shell wildcards, braces, variables and command substitution still pass, because a string check cannot expand them. Issue #26 tracks an allow-list fix; it is not part of this release.
- **Models (#19, #20).** `/setup-huguesstack` writes a project-local `.huguesstack/models.md` instead of a Cursor rule. Roles take `<model> <effort>`, or several choices where each host runs the first it accepts. Setup starts on a Sonnet, Opus and Fable tier with Codex alternatives. A role with no line runs on `inherit-parent`. `check_core.py` rejects Cursor rule paths and vendor slugs in installed skills.
- **Repository docs (#18).** Issue tracker, triage labels and domain-doc settings for working on this repository. They do not ship in the plugin.
- **New evidence.** The [router interactive check](router-interactive-check.md) records one interactive Claude Code session of the router.

Start with the [developer guide](DEVELOPER-GUIDE.md). Existing users should use the new tag or a separate 0.3.0 checkout, then open a fresh host session. A live program bound to 0.2.0 files must be paused and reconciled before changing its installation. See [native consolidation](NATIVE-CONSOLIDATION.md) for the layout, migration and limits.

## Validation and limits

The package validation baseline is 385 Python tests: 131 frozen 0.1.0 contracts, 27 current-checker cases with historical fixtures, one driver that runs the 50 frozen 0.2.0 restoration cases from a hash-bound archive, 44 source and provenance cases, 97 installed adapter and regression cases, 48 native-layout cases, 13 progressive-disclosure cases and 24 installed-tolerance cases. The release adds no test. The package, core, upstream and whitespace checks pass, and so do strict Claude validation of both manifests. See the [test accounting](TEST-COVERAGE.md) for the roots and what each one proves.

Three receipts record host behavior:

- The [skill-list host validation](skill-list-host-validation.md): Claude Code 2.1.293 attached two more skills with the plugin loaded (63 without it, 65 with it), matching the two model-invocable skills in the source, and typing `/hugues-stack:tdd` still ran that user-only skill. Codex 0.161.0 rendered exactly two huguesStack entries, with the router description whole after the reorder.
- The [router eval](hugues-mode-router-eval.md): in print mode with Opus 5.5 at high effort, the router fired for three of four task prompts on the branch and for none on `main`. Each cell is one run.
- The [router interactive check](router-interactive-check.md): in one interactive Claude Code session on the release code, the router fired unprompted on the small-feature prompt, read its adapters, playbooks and bundled skills as files, wrote the Feature playbook's eight steps to the consumer's task tracker instead of TodoWrite, and spawned three `hugues-agent` arena candidates. Claude Code's first-turn skill list held exactly two huguesStack entries, both descriptions whole (236 and 130 characters). The check ran in a disposable copy of the consumer app. An earlier attempt in the real app, in plan mode, never fired the router and changed the real app; the changes were removed. The receipt records that as a lesson.

Not observed: the bug-fix prompt's interactive session never started, and the arena run stopped before any candidate finished, so there is no implementation outcome. Codex installation through its own plugin mechanism, a native `$name` invocation of a disabled skill, a live Codex model turn, a principle typed by name, installation from the `v0.3.0` tag on a fresh machine, mobile device or simulator behavior and live cloud, forge and loop work remain unverified. Persisted-transcript compatibility of the read-only audit and complete planning on the new layout are also unobserved. The 52 offline Bun tests and strict watch-pr type check were last recorded in the PR #17 review-fix pass; the helper sources have not changed since, and this release did not rerun them. The Astra High review policy is suspended for this repository, so no Astra review was run. The owner authorized this release.

The cleanup helper is read-only. Complete inputs still confer no deletion authority, and a separate active/pinned-chat check remains required. Source equality is not runtime equality.

## Downloads

The release includes a source archive, the developer guide as a standalone Markdown file, a source hash inventory, a validation receipt and `SHA256SUMS`. Verify the downloaded assets before using them:

```sh
shasum -a 256 -c SHA256SUMS
```

Run that command from the folder containing all listed release assets. The hashes detect download changes; they are not a separate signing or trust service. See the [test accounting](TEST-COVERAGE.md) and [native consolidation](NATIVE-CONSOLIDATION.md) for detailed boundaries.
