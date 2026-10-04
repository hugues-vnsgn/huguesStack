# Support evidence

WP1 supplies the plugin package and a read-only loader probe. The coordinator
records live host outcomes here when evidence exists. Static validation does
not establish observed support.

| Cell | State | Evidence or gap |
|---|---|---|
| Manifests, paths, skill metadata and authored local links | static-tested | `./scripts/check-plugin.sh` passed; all 27 stdlib regression tests passed on 4 October 2026 |
| Claude Code manifest acceptance | static-tested | `claude plugin validate --strict ./plugin` and marketplace validation passed on 4 October 2026 |
| Claude Code cold load and probe invocation | observed-pass | Claude Code 2.1.286, fresh session, direct `/hugues-stack:hugues-mode` invocation via `--plugin-dir` and `--print`; exact probe reply, exit 0 |
| Codex native marketplace discovery | observed-pass | [PR #1 reviewer](https://github.com/hugues-vnsgn/huguesStack/pull/1), 4 October 2026, Codex 0.160.0: per-invocation local marketplace override listed `hugues-stack@hugues-stack` as not installed at `$REPO/plugin`; config byte-identical before and after; see [host loading](host-loading.md#codex) |
| Codex native install and `$hugues-mode` invocation | blocked | WP1 excludes global installation; `codex plugin add` installs globally and was not run |
| Codex manual project skill probe | observed-pass | Codex 0.160.0, fresh scratch project, temporary `.agents/skills` symlink discovery and read-only skill inspection; `$hugues-mode` reply matched, exit 0 |
| Request routing and playbooks, both hosts | deferred | WP2 |
| Fresh delegate and mode persistence, both hosts | deferred | WP2 and later live tasks |
| Swift/iOS consumer proof | deferred | WP3 and WP4; no consumer access authorized for WP1 |
| Kotlin/Android consumer proof | deferred | WP3 and WP4 |
| KMP shared logic proof on each target | deferred | WP3 and WP4 |
| CMP shared UI proof on each target | deferred | WP3 and WP4 |
| Cross-host review | deferred | Later package; independent WP1 code review is a separate static check |
| Upstream pin and inventory reconciliation | deferred | WP5; target pin is recorded in the immutable plan |

Use the plan's states: authored, static-tested, observed-pass, observed-fail,
blocked and deferred. Record run outcomes separately as pass, fail, flaky,
skipped or incomplete. The current scaffold is not the 0.1.0 release candidate.

See [WP1 validation](wp1-validation.md) for probe limitations, incomplete attempts,
and the independent review fixes. Codex marketplace discovery and the manual
project skill probe have separate observed passes; native installation and skill
invocation remain blocked by WP1 scope.
