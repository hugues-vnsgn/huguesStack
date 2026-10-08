# huguesStack

huguesStack gives Claude Code and Codex a set of workflows for investigating, changing and checking code. It adds guidance for Swift/iOS, Kotlin/Android, Kotlin Multiplatform (KMP) shared logic and Compose Multiplatform (CMP) shared UI. Your app stays in its own repository.

This **unreleased native-layout candidate** keeps 50 public skills, 23 generic
playbooks, two agents and four mobile playbooks. Each skill now owns one canonical
`SKILL.md`. Exact pstack 0.15.9 source remains in a provenance archive outside
runtime discovery. The published 0.2.0 release and its evidence are unchanged.

## Start with Claude Code

For an already installed, signed-in CLI, load this candidate for one session from
your app directory (replace the absolute path):

```sh
claude --plugin-dir "/absolute/path/to/huguesStack/plugin"
```

Confirm native discovery, then invoke `/hugues-stack:hugues-mode` with a small
read-only request. Session-only package loading is documented host behavior;
complete execution of this candidate has not been observed.

## Start with Codex

Use a supported native discovery/invocation route and confirm that `hugues-mode`
appears before using `$hugues-mode`. Package-specific native installation remains
unverified. If it is unavailable or disabled, stop; direct-reading its body is
not an invocation fallback. The [developer guide](docs/DEVELOPER-GUIDE.md#use-codex)
explains the boundary and a first-task workflow.

## What to expect

The workflows ask the agent to inspect the project, keep a task checklist, use focused workers where required, verify the result and report missing evidence. Mobile changes need checks on the affected targets. huguesStack does not supply Xcode, Android tooling, model access or device control.

The earlier 0.2.0 bounded trial confirmed Claude command discovery, but complete planning was blocked by isolated host startup/authentication. It did not establish full Claude/Codex workflow execution, native transcript compatibility, mobile behavior or unattended cleanup. Read the [0.2.0 release notes](docs/RELEASE-0.2.0.md) for the evidence and limits.

## Reference and maintenance

- [Daily workflow](docs/WORKFLOW.md)
- [Maintainer reference](docs/MAINTAINER-GUIDE.md)
- [Native consolidation and migration](docs/NATIVE-CONSOLIDATION.md)
- [Source and workflow contracts](docs/CORE-RESTORATION.md)
- [Test accounting](docs/TEST-COVERAGE.md)
- [Installed planning and read-only worktree audit](plugin/adapters/host-tools.md)

To check a source checkout, run these commands from the huguesStack folder:

```sh
python3 -m unittest discover -s tests -v
./scripts/check-plugin.sh
python3 scripts/check_core.py
python3 scripts/upstream-diff.py check
python3 scripts/check_whitespace.py
```

The 0.1.0 release and its evidence remain available. Its frozen tests are historical coverage, separate from the current adapter tests. Forked under MIT; see [pstack's notice](PSTACK-LICENSE) and the [upstream pin and ledger](docs/upstream/README.md).
