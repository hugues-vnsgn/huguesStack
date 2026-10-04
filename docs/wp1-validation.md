# WP1 validation

Validation on 4 October 2026 covers package structure and loader probes. It does
not establish request routing, mobile execution, consumer task proof, delegation,
or mode persistence. Raw logs remain outside this repository; this page records
the coordinator's observed outcomes and attributed reviewer evidence without
personal machine paths.

| Check | Outcome | Evidence |
|---|---|---|
| Static package checker | pass | `./scripts/check-plugin.sh`: manifests, one skill, paths and authored Markdown links |
| Regression suite | pass | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v`: 27 tests passed |
| Shell syntax | pass | `sh -n scripts/check-plugin.sh` exited 0 |
| Claude static manifest checks | pass | Strict plugin and marketplace validation passed |
| Claude Code 2.1.286 fresh session | pass | `--plugin-dir` plus direct `/hugues-stack:hugues-mode` with `--print`; exact two-line response matched, exit 0 |
| Codex 0.160.0 fresh session, manual project skill | pass | Temporary scratch `.agents/skills` symlink discovery, read-only `cat` of discovered skill, `$hugues-mode` response matched, exit 0 |
| Codex native marketplace discovery | observed-pass | [PR #1 reviewer](https://github.com/hugues-vnsgn/huguesStack/pull/1), 4 October 2026, Codex 0.160.0: per-invocation override listed marketplace `hugues-stack` at `$REPO/.claude-plugin/marketplace.json` and `hugues-stack@hugues-stack  not installed  $REPO/plugin`; config byte-identical before and after |
| Codex native install and `$hugues-mode` invocation | blocked | WP1 excludes global installation; `codex plugin add` installs globally and was not run |

Initial probes with overly restrictive permissions were incomplete. A Claude
Skill-tool invocation was rejected by `disable-model-invocation`; changing to the
direct slash command corrected the probe method and required no package change.
Those attempts were not counted as passes. The successful Codex fallback proves
manual project skill discovery only. Neither host probe installed global skills
or exercised a consumer application.

The reviewer's native marketplace discovery command and output are recorded in
[host loading](host-loading.md#codex). The marketplace name comes from the
manifest's `name`, rather than the override key `hs`. This review follow-up cites
that observation without rerunning or nesting Codex.

## Independent review correction

The reviewer identified a P2 frontmatter parsing defect: an unterminated
single-quoted description was accepted as a plain scalar. The checker now
requires a closing single quote and accepts interior apostrophes only as doubled
quotes. Four new regression tests cover unterminated values, unescaped quotes,
trailing content, accepted quoting, and decoded-value equivalence. Backslashes
remain literal within single quotes. Before the fix, six negative regression
subcases failed; after the fix, all 24 tests passed.

The PR #1 follow-up removes the redundant manifest and its drift test, moves the
Python checker into `scripts/check_plugin.py`, and makes the no-argument
cwd-independence test run the copied repository's shell wrapper. Four regression
tests cover blank lines, comment lines, YAML list rejection with the new
diagnostic, and duplicate keys with the existing diagnostic. Before the parser
change, six subcases failed across the blank, comment, and list tests; afterward,
those cases passed and duplicate-key rejection still passed. The complete suite
now contains 27 tests. `docs/PLAN.md` is byte-identical to `origin/main`.

The checker supports the single-line scalar subset described in
[host loading](host-loading.md). Live loader results and remaining support gaps
are listed in [support evidence](support.md). WP2 and later work packages still
require their own implementation and verification.
