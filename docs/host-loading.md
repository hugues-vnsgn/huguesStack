# Host loading for WP1

The marketplace entry points to `./plugin`. `plugin/plugin.json` follows the
owner's jev-ios-bridge packaging template. Claude's standard manifest lives at
`plugin/.claude-plugin/plugin.json`. Both files carry identical metadata; the
static checker rejects drift. Their paths resolve from the plugin root.

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

For a fresh session, use the local plugin directory without installing it:

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
The reply must contain the exact two lines defined in the
[probe skill](../plugin/skills/hugues-mode/SKILL.md). A model that merely repeats
a token from the user prompt has not proved skill discovery: invoke the skill
by name without supplying the token or its body.

## Codex

The inspected CLI exposes plugin installation and marketplace commands, but no
session-local `--plugin-dir` option. Native local marketplace loading remains
unverified. No global registration or installation is part of this package.

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

`check-plugin.sh` checks the WP1 manifest shape and mirror, relative component
paths, repository symlinks, single-line skill frontmatter, unique names and
descriptions, and local Markdown link files and heading fragments. It accepts
inline links and full/collapsed reference links. Keep authored frontmatter to
plain or quoted single-line scalar values; YAML blocks and nested values are
outside this checker. Single-quoted values require closing quotes and doubled
apostrophes (`''`); backslashes remain literal. The checker skips `.git` and leaves the immutable
`docs/planning` snapshots out of Markdown/frontmatter linting. It still rejects
symlinks there. External link availability is not checked.

Run the host's own validator as well as the static checker before claiming host
metadata compatibility. A successful static check is not an observed host load.

See [WP1 validation](wp1-validation.md) for the consolidated evidence and
incomplete initial probe attempts.
