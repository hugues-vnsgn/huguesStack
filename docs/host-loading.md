# Host loading

The marketplace entry points to `./plugin`. The plugin manifest lives at
`plugin/.claude-plugin/plugin.json`. Component paths resolve from the plugin root.

Claude's [manifest reference](https://code.claude.com/docs/en/plugins-reference)
places metadata in `.claude-plugin/plugin.json` and skills at the plugin root.
The local CLI help exposes `--plugin-dir` for session-local loading and
`plugin validate` for static validation. A copied template alone proves neither
host discovery nor skill invocation.

## Claude Code

From this repository, validate without starting a model session:

```sh
claude plugin validate --strict ./plugin
claude plugin validate --strict ./.claude-plugin/marketplace.json
```

The following was the WP1 fresh-session probe command:

```sh
claude --plugin-dir "$PLUGIN_DIRECTORY" --print '/hugues-stack:hugues-mode'
```

Set `PLUGIN_DIRECTORY` to the plugin directory for the checkout being tested.
Claude Code 2.1.286 passed this direct invocation in a fresh session on
4 October 2026: the exact probe reply matched and the command exited 0.
Invoking the probe through the Skill tool was rejected because the skill uses
`disable-model-invocation`; the direct command is the appropriate probe method.
Record the host version, plugin Git SHA,
argv, exit code, and full reply in an evidence folder outside this repository.
The WP1 probe reply contained the two fixed lines documented in
[WP1 validation](wp1-validation.md). WP2 replaces that probe with the router. A model that merely repeats
a token from the user prompt has not proved skill discovery: invoke the skill
by name without supplying the token or its body.

## Codex

**Codex native marketplace discovery** is **observed-pass**. The
[PR #1 reviewer](https://github.com/hugues-vnsgn/huguesStack/pull/1) reported this
per-invocation override on 4 October 2026 with Codex 0.160.0 (`$REPO` denotes the
reviewed checkout):

```sh
codex -c 'marketplaces.hs.source_type="local"' -c "marketplaces.hs.source=\"$REPO\"" plugin list
```

The output listed `` Marketplace `hugues-stack` `` at
`$REPO/.claude-plugin/marketplace.json` and the row
`hugues-stack@hugues-stack  not installed  $REPO/plugin`.
`~/.codex/config.toml` was byte-identical before and after. Codex names the
marketplace after the manifest's `name`, rather than the config key `hs`.
This records the reviewer's observation; the override was not rerun here.

**Codex native install and `$hugues-mode` invocation** is **blocked** by WP1 scope.
`codex plugin add` installs globally and was not run.

Use a disposable project skill fallback only when the coordinator authorizes
that host probe. In the observed Codex 0.160.0 run on 4 October 2026, a temporary
scratch project's `.agents/skills` symlink exposed the project skills. A fresh
session discovered `hugues-mode`, inspected its file with a read-only `cat`, and
invoked `$hugues-mode`; the exact probe reply matched and the session exited 0.
Label this result **manual project skill**. No global installation was performed.
Keep temporary symlinks outside the plugin repository: its static checker rejects
repository symlinks. Record the actual scratch setup with the run evidence.

A manual probe does not demonstrate the marketplace entry, plugin namespacing,
mode persistence, routing, delegation or mobile execution. Those checks have
separate cells in [support](support.md).

## Static checker boundary

`scripts/check-plugin.sh` delegates to `scripts/check_plugin.py` and keeps the same
`[repository-root]` argument and exit codes. With no argument, the Python checker
uses the repository containing the script, independently of the working directory.

It checks the manifest shape, relative component
paths, repository symlinks, single-line skill frontmatter, unique names and
descriptions, and local Markdown link files and heading fragments. It accepts
inline links and full/collapsed reference links. Blank or whitespace-only
frontmatter lines and `#` comment lines are accepted. Keep authored frontmatter to
plain or quoted single-line scalar values; YAML blocks and nested values are
outside this checker, and YAML lists are rejected. An unparseable line reports
`unsupported frontmatter line; WP1 accepts single-line "key: value" scalars`;
duplicate keys report `invalid or duplicate frontmatter field`.
Single-quoted values require closing quotes and doubled
apostrophes (`''`); backslashes remain literal. The checker skips `.git` and leaves the immutable
`docs/planning` snapshots out of Markdown/frontmatter linting. It still rejects
symlinks there. External link availability is not checked.

Run the host's own validator as well as the static checker before claiming host
metadata compatibility. A successful static check is not an observed host load.

WP2 preserves one upstream local link from `principle-explain-the-number` to the
unshipped `benchmark-checklist` skill. The checker accepts it only with the exact
known source and target, pstack pin, verbatim source SHA-256 and matching
[provenance receipt](upstream/wp2-provenance.json). It prints `DEFERRED` visibly.
Altered source bytes, a different broken link, excess or malformed exceptions,
a changed pin or a newly shipped target fail. This exception preserves the
upstream file; it does not claim the deferred helper is available.

## WP2 applicability

WP1 probe results establish the package and historical loader behavior for that
revision. WP2 changes the skill body, enables its routing guidance and adds a
worker plus principle and review skills. The old probe token is no longer a
WP2 acceptance test. Run the package checks and both Claude static validators
against the WP2 revision; record live routing separately.

For Codex, a fresh disposable project may expose this checkout's skills through
`.agents/skills` for a manual project-skill route preview. Record the exact plugin
SHA, setup, host version, selected file, copied steps, domain and proof, with
argv and exit status outside the repository. Use the six literal prompts in the
[WP2 fixture](../tests/fixtures/wp2-routing-prompts.json). The coordinator observed this manual path with Codex 0.160.0 on 4 October 2026:
six expected routes, domains and all 38 numbered steps matched, exit 0. The host
exposed no todo/plan tool, so the displayed checklist fallback was observed;
native todo integration remains unverified. Eight read-only skill-file reads
supplied the preview. A preview must stop before delegation or consumer execution. This tests planning behavior through
the manual path; it does not demonstrate native plugin invocation or delegated
execution. No external Claude review or model invocation is part of WP2's
recorded checks.

See [WP1 validation](wp1-validation.md) for historical evidence and incomplete
initial probe attempts, and [WP2 validation](wp2-validation.md) for current
acceptance boundaries.
