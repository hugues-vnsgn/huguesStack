# WP1 validation

Validation on 4 October 2026 covers package structure and loader probes. It does
not establish request routing, mobile execution, consumer task proof, delegation,
or mode persistence. Raw logs remain outside this repository; this page records
the coordinator's observed outcomes without personal machine paths.

| Check | Outcome | Evidence |
|---|---|---|
| Static package checker | pass | `./scripts/check-plugin.sh`: manifests, one skill, paths and authored Markdown links |
| Regression suite | pass | `python3 -m unittest discover -s tests -v`: 24 tests passed |
| Shell syntax | pass | `sh -n scripts/check-plugin.sh` exited 0 |
| Claude static manifest checks | pass | Strict plugin and marketplace validation passed |
| Claude Code 2.1.286 fresh session | pass | `--plugin-dir` plus direct `/hugues-stack:hugues-mode` with `--print`; exact two-line response matched, exit 0 |
| Codex 0.160.0 fresh session, manual project skill | pass | Temporary scratch `.agents/skills` symlink discovery, read-only `cat` of discovered skill, `$hugues-mode` response matched, exit 0 |
| Codex native marketplace load | incomplete | Blocked and unverified; inspected CLI had no session-local plugin directory flag |

Initial probes with overly restrictive permissions were incomplete. A Claude
Skill-tool invocation was rejected by `disable-model-invocation`; changing to the
direct slash command corrected the probe method and required no package change.
Those attempts were not counted as passes. The successful Codex fallback proves
manual project skill discovery only. Neither host probe installed global skills
or exercised a consumer application.

## Independent review correction

The reviewer identified a P2 frontmatter parsing defect: an unterminated
single-quoted description was accepted as a plain scalar. The checker now
requires a closing single quote and accepts interior apostrophes only as doubled
quotes. Four new regression tests cover unterminated values, unescaped quotes,
trailing content, accepted quoting, and decoded-value equivalence. Backslashes
remain literal within single quotes. Before the fix, six negative regression
subcases failed; after the fix, all 24 tests passed.

The checker supports the single-line scalar subset described in
[host loading](host-loading.md). Live loader results and remaining support gaps
are listed in [support evidence](support.md). WP2 and later work packages still
require their own implementation and verification.
