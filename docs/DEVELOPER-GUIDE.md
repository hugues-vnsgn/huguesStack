# Use the native consolidation candidate

This is an unreleased adaptation of huguesStack 0.2.0. Your app stays in its own
repository. Skills are instruction files for specific jobs; playbooks order the
steps of a larger task. Start with `hugues-mode` and describe the result you want.
It retains the generic workflows and applicable Swift/iOS, Kotlin/Android,
KMP and CMP proof rules.

## Before you start

Use an already installed and signed-in Claude Code or Codex. Read your app's own
instructions and preserve existing work. A source preview requires no simulator.
Executing an app requires its actual build/test tooling and your authorization.
The Python planning/audit helper requires Python 3.9+ and Git; plan validation
also requires Node. Advanced helpers may require Bun and dependencies. This guide
performs no installation or authentication setup.

## Install in Claude Code

This candidate is not published. Keep the existing release while reviewing it.
For a session-only candidate load, start from your app directory:

```sh
claude --plugin-dir "/absolute/path/to/huguesStack/plugin"
```

Check native discovery before invoking `/hugues-stack:hugues-mode`. A package
manifest check is not evidence that invocation succeeded. Do not modify global
settings to force discovery or bypass an owner-disabled skill.

For the unchanged published release, use its [0.2.0 release notes](RELEASE-0.2.0.md)
and instructions at that tag. Its historical manual-loading instructions do not
apply to this candidate's native invocation contract.

## Use Codex

Codex supports explicit skill invocation and project-native discovery. This
candidate supplies canonical skills plus `agents/openai.yaml` invocation metadata.
Its exact package installation route has not been validated in a live Codex session.
Use your host's supported native discovery route, and check that `hugues-mode`
is available before invoking `$hugues-mode`. Keep the complete resource layout.

If discovery or invocation is unavailable, disabled, denied or unknown, stop the
dependent workflow. Do not paste the absolute SKILL.md path as a loading fallback,
copy a disabled body under another name, or change owner settings to evade it.
See the [official skill documentation](https://learn.chatgpt.com/docs/build-skills)
for host-specific discovery and invocation controls; this guide does not invent
a plugin loader or claim a tested installation method.

## Your first task: fix a small search bug

First invoke the mode natively, then give a bounded preview request:

```text
Preview only: inspect this project's instructions and explain how search
submission works. Name the relevant files, selected playbook and unresolved
questions. Do not edit or run the app.
```

Review the explanation before authorizing the change:

```text
Fix the search field clearing before submission succeeds. Use this task's
worktree. You may edit the relevant source and run the repository's existing
local tests. Preserve unrelated work. Report the reproduction, changed behavior,
checks and any proof you could not run. Do not push or publish.
```

The workflow retains its evidence and worker requirements. When another skill is
needed, it uses supported native invocation. A separate command is needed only
if the host requires explicit user invocation. A disabled or denied dependency
holds its phase; the agent must not silently replace it with direct file reads.
These handoffs are conditional, not a proven limitation in every session.

Inspect the actual diff and test evidence. A compilation result does not establish
screen behavior; shared changes may need both affected targets. Missing device,
tool, model or execution authority stays visible as a gap.

## Choose other work

Ask for investigation, design, review, a plan or a specific implementation result.
Give the consumer path/revision, scope and expected observable outcome. Mode
routing preserves intent before mobile domain. Specific skills remain directly
available through their native names. Generic review retains its own model panel;
this repository's Astra PR policy is not imposed on your app.

## Pause and resume

Use the pause/pickup workflow to record branch, head, completed work, evidence,
remaining gates and actual worker state. In a fresh session, invoke the needed
skills natively again. A saved path or parent worker's claim does not establish
current invocation eligibility. Do not scan unrelated chat histories.

## Updating

Keep the old install while an active task is bound to it. Public skill names and
relative entry paths are retained; a changed installation root may still affect
owner settings that use absolute paths. Reconcile these explicitly through the
host's supported controls. Never silently re-enable a previously disabled skill.

Old 0.2.0 installed-payload bindings are intentionally rejected. Review the changed
workflow and plan, then create a new binding as described in
[host tools](../plugin/adapters/host-tools.md). Ordinary resource rereads remain
binding-guarded; public skill bodies require native invocation. The plan translator
holds on obsolete raw-skill reads so the author can correct the plan explicitly.

## Removing it

A session-only Claude candidate load ends with that session. Persistent installs
must be removed through the host mechanism that installed them, under your scope.
Keep checkouts or evidence still referenced by unfinished tasks; this guide does
not delete worktrees, active/pinned chats or user data.

## Troubleshooting

Missing native entry: check the host's supported discovery surface; stop rather
than using a raw-body fallback. Binding drift: reconcile the installation and
program, never regenerate hashes to conceal an unexpected change. Missing activity
or PR metadata: the read-only cleanup report holds candidates. No report grants
deletion authority, and active/pinned-chat verification is a separate gate.

## What has been verified

Current source, contract, integrity and helper checks are described in
[test accounting](TEST-COVERAGE.md) and [migration notes](NATIVE-CONSOLIDATION.md).
They use disposable local consumers and synthetic activity. The earlier bounded
host trials were blocked before complete planning/invocation; this candidate adds
no new live-host evidence. Native runtime parity, persisted-transcript coverage,
mobile devices and live forge/cloud/loop workflows remain unverified.
