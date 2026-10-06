# Host notes

Read these notes before delegation. Use the host's actual tool schema and available models. This package does not install or configure hosts.

## Claude Code

The plugin manifest registers [hugues-agent](../../../agents/hugues-agent.md). When the Agent tool exposes that definition, spawn a fresh instance for each implementation round and include the absolute path to this mode's `SKILL.md` and the absolute plugin skills directory in its scoped brief. Use background execution only when the actual tool supports it. Omit the model argument to inherit the parent model. Honor a user-selected role model only if the current host accepts it; disclose a rejection and continue with inherit-parent if the user did not require that model.

If the definition is unavailable, read the wrapper file in full and provide its complete contents plus the scoped brief, including the absolute mode `SKILL.md` path and absolute plugin skills directory, to a fresh native general-purpose subagent. Label this as a wrapper fallback rather than a successful custom-agent load.

## Codex

Use Codex's native subagent tool. Read [hugues-agent](../../../agents/hugues-agent.md) in full and place its complete contents before the scoped assignment in the new agent's prompt. Give the absolute path to this mode's `SKILL.md` and the absolute plugin skills directory in that prompt. Omit model and reasoning overrides so the subagent inherits the parent. This is a prompt adapter, not a claim that Codex supports a custom `hugues-agent` type.

Use the available subagent lifecycle tools to wait for completion. Start a fresh subagent for each new implementation round. Supply the full consolidated brief instead of depending on an old worker's retained context.

## Retained pstack tool contracts

Translate upstream `Task` calls through the Claude Agent or Codex native adapters above. Preserve each role's prompt, scoped input, references and required output; carry read-only intent as an explicit writable-scope restriction. Inspect the actual tool schema before selecting worker type, background mode, wait or result retrieval. For a registered Claude worker, provide the scoped role prompt with the common handoff. For a wrapper fallback or Codex prompt adapter, prepend the complete wrapper contents to that prompt. Read-only source research may need authorized connector reads; choose the available worker capability that preserves those reads while prohibiting writes, rather than assuming a host's `readonly` flag preserves connector access.

Replace upstream Cursor model-role rules and default slugs with the current human-selected role model when the host accepts it; otherwise use the inherited-parent behavior above. Preserve explicit model requirements as a blocker if unavailable. Record the actual model choice and rejected override. Distinct prompts on the same host establish process independence only; claim model diversity only when the actual model identities establish it.

Map upstream todolists to the host's available todo or plan tool. Preserve the ordered phases and completion states. When that tool is absent, show the same checklist and disclose the limit. Map `Read` and direct reference loads to the host's actual file-read tool or authorized local read command, using the resolved plugin paths; read the complete selected reference before constructing its role prompt.

Discover tools from the active host tool catalog, supported tool search and authorized connector metadata. Inspect each discovered tool's schema before calling it. Classify available evidence sources by their actual read capabilities and record absent, inaccessible or ambiguous categories. Check local Git and any source-control CLI availability instead of assuming them. A Cursor `mcps/` path, an upstream example tool name or a model error message does not establish a callable tool or permitted runtime here. Select runtime, framework and target examples only after reading the current project; report missing evidence rather than guessing.

## Common handoff

Set a bounded scope and writable paths. Every handoff, including a registered Claude agent or either wrapper adapter, must include the absolute path to this mode's `SKILL.md` and the absolute plugin skills directory, plus the consumer, domain, proof surface, current human authority and evidence required. Workers read the mode and relevant principle files using those supplied paths. Relative source links identify package files, not runtime addresses in a consumer checkout. Read skills with `disable-model-invocation: true` directly from disk; workers cannot invoke them through the Skill tool. If a supplied path is missing or unreadable, report the handoff gap before implementation instead of guessing from the working directory. Instruct the worker to perform that assignment directly, without recursively delegating itself. Reviewers are fresh read-only native subagents and receive the same intent, diff and rubric.

If native subagents are unavailable or delegation is prohibited by current instructions, finish read-only investigation or route preview and report implementation delegation as blocked. Never claim a delegated implementation or independent review that did not occur. Keep scoped worker outputs as evidence for the coordinator's own checks.

Missing model-role configuration means `inherit-parent`. For new huguesStack PR reviews, apply the owner's explicit Astra High choice through the [PR review policy](pr-review-policy.md); implementation defaults stay unchanged. No setup command is required in WP2. Same-host reviewers provide process independence only. The user arranges any cross-host review; never contact another host or external agent automatically.
