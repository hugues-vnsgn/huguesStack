# Host notes

Read these notes before delegation. Use the host's actual tool schema and available models. This package does not install or configure hosts.

## Claude Code

The plugin manifest registers [hugues-agent](../../../agents/hugues-agent.md). When the Agent tool exposes that definition, spawn a fresh instance for each implementation round and include the absolute path to this mode's `SKILL.md` and the absolute plugin skills directory in its scoped brief. Use background execution only when the actual tool supports it. Omit the model argument to inherit the parent model. Honor a user-selected role model only if the current host accepts it; disclose a rejection and continue with inherit-parent if the user did not require that model.

If the definition is unavailable, read the wrapper file in full and provide its complete contents plus the scoped brief, including the absolute mode `SKILL.md` path and absolute plugin skills directory, to a fresh native general-purpose subagent. Label this as a wrapper fallback rather than a successful custom-agent load.

## Codex

Use Codex's native subagent tool. Read [hugues-agent](../../../agents/hugues-agent.md) in full and place its complete contents before the scoped assignment in the new agent's prompt. Give the absolute path to this mode's `SKILL.md` and the absolute plugin skills directory in that prompt. Omit model and reasoning overrides so the subagent inherits the parent. This is a prompt adapter, not a claim that Codex supports a custom `hugues-agent` type.

Use the available subagent lifecycle tools to wait for completion. Start a fresh subagent for each new implementation round. Supply the full consolidated brief instead of depending on an old worker's retained context.

## Common handoff

Set a bounded scope and writable paths. Every handoff, including a registered Claude agent or either wrapper adapter, must include the absolute path to this mode's `SKILL.md` and the absolute plugin skills directory, plus the consumer, domain, proof surface, current human authority and evidence required. Workers read the mode and relevant principle files using those supplied paths. Relative source links identify package files, not runtime addresses in a consumer checkout. Read skills with `disable-model-invocation: true` directly from disk; workers cannot invoke them through the Skill tool. If a supplied path is missing or unreadable, report the handoff gap before implementation instead of guessing from the working directory. Instruct the worker to perform that assignment directly, without recursively delegating itself. Reviewers are fresh read-only native subagents and receive the same intent, diff and rubric.

If native subagents are unavailable or delegation is prohibited by current instructions, finish read-only investigation or route preview and report implementation delegation as blocked. Never claim a delegated implementation or independent review that did not occur. Keep scoped worker outputs as evidence for the coordinator's own checks.

Missing model-role configuration means `inherit-parent`. No setup command is required in WP2. Same-host reviewers provide process independence only. The user arranges any cross-host review; never contact another host or external agent automatically.
