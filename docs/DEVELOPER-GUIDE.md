# Use huguesStack 0.2.0

huguesStack is a collection of instructions for your coding agent. You describe a result, such as "fix the search field clearing too early," and it selects a workflow for investigating, implementing and checking that result. It is useful when you want the agent to follow a repeatable process and show what it verified.

It runs through **Claude Code or Codex**. Your application stays in its own folder; huguesStack is not an app framework or a mobile SDK. The package adds mobile guidance for Swift/iOS, Kotlin/Android, Kotlin Multiplatform (KMP) shared logic and Compose Multiplatform (CMP) shared UI.

This guide is for [version 0.2.0](https://github.com/hugues-vnsgn/huguesStack/releases/tag/v0.2.0). Start with a small task in an app you already know how to build.

## Before you start

Have the following ready on the new machine:

- **Git**, plus an installed and signed-in **Claude Code or Codex**. Use the host's own installation and sign-in instructions: [Claude Code setup](https://code.claude.com/docs/en/setup) or [Codex CLI](https://developers.openai.com/codex/cli/).
- **Your application's source checkout.** Know which folder contains it. If you will edit code, use a branch or worktree for that task and preserve existing changes.
- **The app's build and test tools** before asking for execution. For iOS this normally means macOS and the project's Xcode version; for Android, its JDK, Android SDK and Gradle wrapper. Shared mobile changes may need both toolchains.
- **Python 3.9 or newer** for huguesStack's package and installed planning/audit helpers. Plan validation also needs Node.js. Some advanced upstream helpers need Bun and additional packages; they are not installed by this guide.

Check the basics in a terminal:

```sh
git --version
python3 --version
```

Then run `claude --version` or `codex --version` for the host you chose. If a command is missing, finish that tool's setup before continuing. A preview only reads source; it does not need a running simulator or emulator.

The examples below use a POSIX shell, such as macOS Terminal. Replace paths beginning with `/absolute/path/to/` with real paths on your machine. Keep the quotation marks when a path contains spaces.

## Choose how to load it

| Host | Recommended starting point | What it changes |
|---|---|---|
| Claude Code | Install the pinned release with the commands below | Adds the plugin to your Claude user configuration on this machine |
| Claude Code, one session | Clone the release and use `--plugin-dir` | Loads the plugin only for that session |
| Codex | Clone the release and ask Codex to read its main skill | No native plugin installation or persistent configuration change |

A *skill* is an instruction file for one kind of work. A *playbook* is a sequence of steps for a larger task. The main skill, `hugues-mode`, chooses the playbook from your request. You do not need to learn all 50 skills first.

## Install in Claude Code

### 1. Add the release and install it

Run this in a **terminal**, from any folder:

```sh
claude plugin marketplace add hugues-vnsgn/huguesStack#v0.2.0
claude plugin install hugues-stack@hugues-stack --scope user
claude plugin list
```

The marketplace is the repository's list of plugins. Both its name and this plugin's name are `hugues-stack`, so the full installation name is `hugues-stack@hugues-stack`. The `#v0.2.0` suffix selects a fixed release instead of a moving branch.

The list should show `hugues-stack`, version `0.2.0`, enabled in user scope. User scope makes it available across your projects on this machine. To restrict installation to yourself in one project, run the install command from that app's folder with `--scope local` instead. Use `--scope project` only when you intend to record plugin configuration for collaborators in the project.

If a marketplace named `hugues-stack` already exists, open `/plugin` in Claude and inspect its source before proceeding. Follow [Updating](#updating) if it points at an older release; do not assume a second add command changed the pin.

### 2. Open your application

Start a **new Claude session from the application folder**, not the huguesStack folder:

```sh
cd "/absolute/path/to/your-app"
claude
```

Type `/hugues-stack:hugues-mode` in Claude. It should appear as a plugin command. If it does not, see [Troubleshooting](#troubleshooting).

### Alternative: load for one session

Use this if you prefer not to install the plugin in your user configuration. In a terminal, choose a tools folder outside your app and a new clone destination:

```sh
cd "/absolute/path/to/your-tools-folder"
git clone --branch v0.2.0 --depth 1 https://github.com/hugues-vnsgn/huguesStack.git huguesStack-0.2.0
cd huguesStack-0.2.0
HUGUESSTACK_ROOT="$(pwd -P)"
./scripts/check-plugin.sh
claude plugin validate --strict ./plugin
cd "/absolute/path/to/your-app"
claude --plugin-dir "$HUGUESSTACK_ROOT/plugin"
```

The checks should print a passing result. Keep this terminal open: `HUGUESSTACK_ROOT` is a shell variable for this terminal only. In a new terminal, set it to the actual clone path again. Avoid loading a second installed copy of the same plugin in this session; disable the other copy in `/plugin` first if needed.

## Use Codex

Native huguesStack plugin installation and namespaced commands in Codex have not been verified for this release. Use the following manual method. It asks Codex to read the shipped instructions directly; it is not evidence of native plugin discovery.

### 1. Get the pinned files

In a **terminal**, clone the release outside your app. Skip the clone if you already made it in the Claude session-only instructions:

```sh
cd "/absolute/path/to/your-tools-folder"
git clone --branch v0.2.0 --depth 1 https://github.com/hugues-vnsgn/huguesStack.git huguesStack-0.2.0
cd huguesStack-0.2.0
./scripts/check-plugin.sh
pwd -P
```

Copy the absolute path printed by `pwd -P`. Keep the whole checkout: the main skill links to adapters, playbooks and other skills, so copying only its `SKILL.md` will break those links.

### 2. Open the app and load the instructions

In the terminal:

```sh
cd "/absolute/path/to/your-app"
codex
```

In **Codex**, paste this message after replacing the example path with the clone path you copied:

```text
Read /absolute/path/to/huguesStack-0.2.0/plugin/skills/hugues-mode/SKILL.md
in full, then read its required linked instructions in order. Use hugues-mode
for this task through this manual loading method. Preview only: inspect this
app's instructions and build setup, explain how search submission works, and
show the playbook, relevant files and unresolved questions. Do not edit or run
the app. If you cannot read a required file, report which one.
```

A path pasted into a chat message does not expand shell variables such as `$HUGUESSTACK_ROOT`. Paste the real absolute path. If the host asks for access to the separate tools checkout, grant only the access needed to read those files through its normal controls. Repeat the loading message in a fresh session.

Codex also supports [project skills and symlinked skill folders](https://learn.chatgpt.com/docs/build-skills), but that is optional configuration. You can use the direct-read method without changing your app's existing skills.

## Your first task: fix a small search bug

This example uses a Kotlin/Compose Android app with a recent-search feature. Use it only if it matches your app's intended behavior; otherwise substitute a similarly small bug you can reproduce. The aim is to complete one change and inspect the evidence yourself.

### 1. Preview the work

In **Claude**, enter the command on the first line and the message below it. In **Codex**, first load the instructions as above, then paste the message without the slash-command line.

```text
/hugues-stack:hugues-mode
Preview this bug fix. Submitting "  kotlin  " should save "kotlin" in recent
searches. A whitespace-only submission should add nothing. Keep the text the
user is currently typing unchanged until submission.

Read this project's instructions and source. Show where submission and storage
happen, the selected playbook and its steps, the relevant tests, the build
and emulator checks you propose, and a folder for saved evidence. Identify anything you cannot determine.
Do not edit files, install dependencies, build or run the app yet.
```

Expected result: a `bug-fix` plan grounded in actual source files, a short checklist, the tests it intends to run, and any missing prerequisites. It should establish whether this is native or shared code, and identify the actual build variant and target instead of guessing a Gradle task or emulator name.

Read the plan. Correct the intended behavior or scope before asking it to implement. If you only wanted to understand the code, stop here.

### 2. Authorize the change you want

After checking the plan, send a message such as the following. Replace the bracketed items with the test command and emulator identity from the preview; do not paste the brackets unchanged.

```text
Proceed with the reviewed plan. You may edit the search feature and its focused
tests, preserving existing changes. Run [the agreed test command] and build
[the agreed variant]. You may use [the agreed task-owned emulator] to exercise
submission and recent-search selection. Do not download dependencies, change
accounts or global settings. Keep changes uncommitted; do not open a PR or
publish anything. Report blocked steps.

Show the regression failing against the original code, then passing after the
fix. Keep the reports and any screenshots in the evidence folder we agreed on.
If a focused regression test is impractical, explain why and show the closest
useful verification of the original problem and the fix.
```

For mobile bugs, the instructions require a fresh worker for the regression test and a separate worker for production changes, with the failing and passing results independently checked. This depends on your host's worker capabilities. Missing workers or model access should be reported, not silently counted as completed work.

### 3. Inspect the result

Before accepting the change, check these results:

1. **The diff matches the request.** The submission behavior changes; text editing and unrelated code remain intact.
2. **The regression is relevant.** It failed because of the original bug and passed after the fix. A test that never ran or tested a different path is not enough.
3. **The app behavior was checked.** The report identifies the build and emulator actually used, then shows padded submission, blank submission and selection from recent searches. A successful build alone does not establish these behaviors.
4. **The report is honest about gaps.** It lists commands, exit results and saved evidence, including blocked or skipped checks. Shared KMP/CMP changes need the affected Android and iOS checks.

You decide when to commit, open a PR or publish. Installing huguesStack does not grant permission for those actions. Your project's own instructions and policies still apply.

## Choose other work

Start with `hugues-mode` and describe the outcome in ordinary language. These examples are **messages to your agent** after loading the mode:

| What you need | Example message |
|---|---|
| Understand code | "Explain how this Swift list computes its scroll position. Read-only investigation." |
| Add behavior | "Add Shift-Return to select the previous search result. Preserve Escape and touch behavior." |
| Diagnose tooling | "Find why this Android build fails. Show the cause before changing configuration." |
| Check a change | "Verify this existing Kotlin change using the project's current test and emulator recipe." |
| Change shared logic | "Update this KMP boundary and check the affected native caller on Android and iOS." |
| Review a diff | "Use interrogate to review this diff. Report bugs separately from preferences; do not fix files." |

For a specific skill in Claude, use its namespaced command, such as `/hugues-stack:interrogate`. In the Codex manual method, ask it to read that skill's `plugin/skills/<name>/SKILL.md` and required links. Missing review models remain a reported capability gap. This repository's two-Astra-reviewer policy does not automatically apply to your app.

Optional model-role configuration lives in your app's `.huguesstack/models.md`. Ask for `setup-huguesstack` if you want help choosing available models and a budget; review the proposed configuration before it is written. You do not need to configure roles to try a preview. See the [maintainer reference](MAINTAINER-GUIDE.md) for the full role and workflow contracts.

## Pause and resume

Before closing a long session, send:

```text
Pause safely at the next complete step. Write a local checkpoint containing the
goal, allowed actions, branch and commit, uncommitted changes, completed checks,
evidence paths, blockers and the next action. Preserve the work. Do not push
or remove worktrees.
```

In a fresh session, load hugues-mode again and supply the checkpoint's actual path:

```text
Resume from /absolute/path/to/checkpoint.md. Compare it with the current Git
state and saved evidence before continuing. Keep blocked and skipped checks
visible, and tell me if the task or files no longer match the checkpoint.
```

For long-running programs, the [installed planning helpers](../plugin/adapters/host-tools.md) save a binding to the approved plugin files and reread workflows through it. An update changes that binding. Finish or pause such a program before updating; do not silently replace its approved files.

## Updating

**Claude marketplace installation:** the commands above pin `v0.2.0`, so refreshing a marketplace is not an instruction to follow a newer release. Read the new release notes first. In `/plugin`, inspect the installed scope and the `hugues-stack` marketplace source. To select a different tag, uninstall this plugin in its original scope, remove its marketplace entry, then add `hugues-vnsgn/huguesStack#<new-tag>` and install again in that scope. Replace `<new-tag>` with a published tag. This affects sessions using that installation; close them first. Check the new version with `claude plugin list` and start a fresh session.

**Session-only Claude or manual Codex:** clone the new tag into a new tools folder, run its package check, and use the new absolute path in the launch command or loading message. Keep the old checkout while a task still references it. Do not run a blind `git pull` in a checkout pinned to a release tag.

## Removing it

For the user-scope Claude installation, run this in a terminal:

```sh
claude plugin uninstall hugues-stack@hugues-stack --scope user
claude plugin list
```

For a local or project installation, run it from that app's folder and use the same scope you selected when installing. Remove the `hugues-stack` marketplace through `/plugin` if you no longer want its catalog. Restart Claude and check that the command is gone.

For session-only Claude, end the session and stop passing `--plugin-dir`. For manual Codex, stop loading the files. You can remove the tools checkout after confirming that no task, checkpoint or project skill link still needs it. This does not require deleting your app, its changes or its evidence.

## Troubleshooting

| Problem | What to check |
|---|---|
| `claude`, `codex`, Git or Python is not found | Finish that tool's installation and open a new terminal. Check its version before retrying. |
| Claude says the marketplace already exists | Inspect its current source in `/plugin`; follow Updating if the tag is wrong. |
| `/hugues-stack:hugues-mode` is missing | Check `claude plugin list`, the installed scope and enabled status, then restart Claude. For session loading, check that `--plugin-dir` points to the clone's `plugin` folder. |
| Codex cannot read a required file | Check the absolute clone path and host access controls. Keep the entire checkout; do not copy only one skill file. |
| The agent works in the wrong repository | Stop it and reopen the host from your application's folder. The plugin checkout is only the instruction source. |
| A requested model, test runner or device is unavailable | Keep that step blocked. Choose an available, project-approved alternative explicitly, or set up the prerequisite yourself. |
| Tests pass but the visible bug was not checked | Ask for the same user interaction on the agreed build and target. Keep the missing check in the report. |
| Planning reports changed plugin files | Compare the recorded binding with the intended version. Reconcile the change before continuing the program. |
| The worktree audit returns exit 2 or a hold | Activity or PR metadata is incomplete or unsupported. Supply only authorized evidence; do not scan private chat history to fill the gap. |

## What has been verified

The 0.2.0 package includes all 161 pinned pstack 0.15.9 source files unchanged. Package tests cover the loaders, mobile/host boundaries and installed planning/audit adapters with disposable projects and synthetic activity records. Historical 0.1.0 tests are counted separately.

A bounded trial used Claude Code 2.1.290 and Codex 0.160.1. Claude discovered all 50 commands; full native planning was blocked by isolated startup/authentication, and Codex failed during startup. These are observed versions, not minimum-version guarantees. The installation commands in this guide follow host documentation and CLI help; a fresh-machine 0.2.0 install has not been run.

Complete native workflow execution, actual persisted transcript compatibility, mobile device behavior and live cloud/forge/loop work remain unverified for this restored package. The read-only cleanup report can conservatively hold on unsupported records, empty sources or unknown PR state. It never authorizes deletion and still requires a separate active/pinned-chat check. Upstream source equality does not prove host runtime equality.

For details, read the [0.2.0 release notes](RELEASE-0.2.0.md), [test accounting](TEST-COVERAGE.md), [daily reference](WORKFLOW.md) or [maintainer reference](MAINTAINER-GUIDE.md). The [0.1.0 release notes](RELEASE-0.1.0.md) retain the evidence for that older version.
