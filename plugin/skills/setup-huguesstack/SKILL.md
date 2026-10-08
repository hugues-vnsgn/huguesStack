---
name: setup-huguesstack
description: Configure which models pstack uses per role and at what reasoning budget. Detects the models your host's agent tool accepts and writes a project model-role file that overrides the skill defaults. Use for /setup-huguesstack, "configure pstack models", "pstack budget", or changing pstack's model choices.
---

## Host invocation contract

Before these workflow steps, apply the [host contract](../../adapters/host.md)
and [mobile applicability](../../adapters/mobile.md#applicability).
The host contract supersedes inherited sibling-body reads.

# Setup pstack

Write `.huguesstack/models.md` at the project root: the model-role file every pstack skill reads before it picks a worker's model.

## Role values

A role value is a model and an effort, such as `inherit-parent xhigh` or `opus max`.

- The model is `inherit-parent` or a real slug, a value the host's native agent tool accepts for `model`. `inherit-parent` leaves `model` unset, so the worker runs on the parent chat model. It is valid on every host.
- The effort is the last token, on the ladder `max` > `xhigh` > `high` > `medium` > `low`. It sets the agent tool's effort.
- A panel role (arena runners, architect runners, interrogate reviewers) holds a comma-separated list, and one subagent runs per entry, `inherit-parent` entries included, so the list length sets the count. A panel whose entries share one model gives process independence. Distinct models give it model diversity.
- `arena cross-judge pool` is also a list, but Arena selects one value from it whose model differs from the parent's when possible. `swarm workers` is the default model for every worker unless a race or comparison assigns another model per arm.

## Steps

### 1. Detect available models

Read the `model` and effort values your host's native agent tool accepts from its own schema in this session. In Claude Code that is the Agent tool's `model` enum (aliases such as `opus` or `sonnet`) and its `effort` enum. When the schema offers no model choice, the detected set is empty and every role stays on `inherit-parent`. Never write a real slug you have not confirmed is available.

### 2. Load current state

The default role values are the file shape shown in step 5 below. If `.huguesstack/models.md` already exists, read it and treat its `# budget` line and its role values as the current choices. Otherwise start from those defaults. A line whose role is not in step 5, such as `how critics`, is from a retired role. Drop it.

### 3. Budget, map, and confirm

**(a) Ask for a budget.** Prefer AskQuestion over free text. Offer these four options with these exact labels, and name the current budget when the file records one.

- `unlimited — keep max`
- `large — xhigh reasoning`
- `medium — high reasoning`
- `small — medium reasoning`

**(b) Apply it.** Build the working table from the skill defaults, and on a re-run keep the model or list of any role whose value differs from its default. `unlimited` leaves every effort as in that table. `large`, `medium`, and `small` set the effort of every entry, panel and `inherit-parent` entries included, to `xhigh`, `high`, or `medium`. If the agent tool does not accept that effort for that model, use its highest accepted effort below the target, else mark the role as needing a choice. So `small` turns `inherit-parent max` into `inherit-parent medium`.

**(c) Show the roles and confirm.** Show every role with its value, marking any real slug not in the detected set as needing a choice. Also list each line step 2 dropped. Ask whether to accept as-is or change specific roles, offering the detected models plus `inherit-parent` as the options. Prefer AskQuestion over free text.

### 4. Validate

Every real slug written must be in the detected set. `inherit-parent` always passes. If a chosen real slug is not available, stop and ask again.

### 5. Write the file

Write `.huguesstack/models.md` with a `# budget` line naming the chosen label and its target effort, and one line per role, using the same labels hugues-mode uses. Overwrite the whole file so re-runs stay idempotent. Shape:

```
# huguesStack model roles. One line per role. Delete a line to fall back to the skill default.
# Value: `<model> <effort>`. `inherit-parent` leaves the agent tool's `model` unset, so the role runs on the parent chat model. Each panel entry runs one subagent.
# budget: unlimited (max)
feature, refactoring: inherit-parent xhigh
bug-fix: inherit-parent xhigh
perf-issue: inherit-parent xhigh
hillclimb: inherit-parent xhigh
judgment and prose: inherit-parent max
hardest tasks: inherit-parent max
how explorer: inherit-parent xhigh
how explainer: inherit-parent max
why investigators: inherit-parent xhigh
why synthesizer: inherit-parent max
reflect tooling: inherit-parent max
reflect judgment, divergent, synthesizer: inherit-parent max
arena runners: inherit-parent max, inherit-parent max, inherit-parent max
arena cross-judge pool: inherit-parent max
swarm workers: inherit-parent xhigh
architect runners: inherit-parent max, inherit-parent max, inherit-parent max
interrogate reviewers: inherit-parent max, inherit-parent max, inherit-parent max
```

### 6. Confirm

Tell the user the file was written and that each skill reads it at its next role selection. Re-running this skill updates it. When the project is also worked on from the other host, a real slug that host's agent tool rejects runs there on the role default.

### 7. Offer a verification skill (optional)

Check whether the project has a way to drive the real app for proof (a `verify-*` skill, or an existing harness). If not, offer once: "want a project-local verification skill, so agents can drive the app the way a user does and prove changes work? I can generate one with /create-verification-skill." On yes, invoke `/create-verification-skill` (resolves wherever pstack is installed: workspace, user, or plugin). On no, move on without pushing.
