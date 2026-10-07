# huguesStack

huguesStack gives Claude Code and Codex a set of workflows for investigating, changing and checking code. It adds guidance for Swift/iOS, Kotlin/Android, Kotlin Multiplatform (KMP) shared logic and Compose Multiplatform (CMP) shared UI. Your app stays in its own repository.

Version **0.2.0** includes the complete pinned pstack 0.15.9 source: 50 skills, 23 core playbooks and two agent definitions, plus four mobile playbooks. A *skill* is an instruction file for a particular job; a *playbook* orders the steps of a larger task. Start with `hugues-mode` and describe your goal. It chooses a playbook.

## Start with Claude Code

You need Git and an installed, signed-in Claude Code CLI. Run these commands in a terminal:

```sh
claude plugin marketplace add hugues-vnsgn/huguesStack#v0.2.0
claude plugin install hugues-stack@hugues-stack --scope user
claude plugin list
```

Check that the list shows `hugues-stack`, version `0.2.0`, enabled in user scope. This makes it available to your Claude sessions on this machine. Then start a new session **in your app's folder**, replacing the example path:

```sh
cd "/absolute/path/to/your-app"
claude
```

Type this in Claude, not in the terminal:

```text
/hugues-stack:hugues-mode
Preview only: inspect this project's instructions and build setup. Explain how
search submission works and which playbook you would use to investigate it.
Show the relevant files and unresolved questions. Do not edit or run the app.
```

The [step-by-step developer guide](docs/DEVELOPER-GUIDE.md) covers installation on another machine, a complete first bug fix, updates, removal and troubleshooting. It also shows a session-only loading option.

## Start with Codex

Use the guide's [Codex instructions](docs/DEVELOPER-GUIDE.md#use-codex). Clone the release into a separate tools folder, open Codex in your app and ask it to read the absolute path to `plugin/skills/hugues-mode/SKILL.md`. Native huguesStack plugin installation in Codex has not been verified; the guide explains this manual loading method.

## What to expect

The workflows ask the agent to inspect the project, keep a task checklist, use focused workers where required, verify the result and report missing evidence. Mobile changes need checks on the affected targets. huguesStack does not supply Xcode, Android tooling, model access or device control.

The package passes source and adapter checks. A bounded native trial confirmed Claude command discovery, but complete planning was blocked by isolated host startup/authentication. It did not establish full Claude/Codex workflow execution, native transcript compatibility, mobile behavior or unattended cleanup. Read the [0.2.0 release notes](docs/RELEASE-0.2.0.md) for the evidence and limits.

## Reference and maintenance

- [Daily workflow](docs/WORKFLOW.md)
- [Maintainer reference](docs/MAINTAINER-GUIDE.md)
- [Core restoration contracts](docs/CORE-RESTORATION.md)
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
