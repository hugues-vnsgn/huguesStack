# Claude Code and Codex host adapter

Read this adapter, the mobile adapter and the project PR policy before the pinned
core. They translate host mechanisms and limit authority; the core owns workflow
phases, mandatory gates, panel cardinality, fallback and stop rules. A constraint
can block execution. It cannot turn an omitted gate into success.

## Loading and routing

The active registry is [core-bindings.json](../core-bindings.json).
`poteto-mode` maps to `hugues-mode`, `poteto-agent` to `hugues-agent`,
`Comment Sicko` to `hugues-comment-sicko`, and `setup-pstack` to
`setup-huguesstack`. Every other active skill retains its name.
Load the registered entrypoint before executing a referenced skill. Read its
pinned source in full, including every reference required by the current phase.
Resolve source-relative references from that source file's directory. Resolve
public loader links from the loader's directory. Do not resolve either against
the consumer's working directory.

The mode applies the pinned router, including figure-it-out for large,
cross-cutting or unmatched work and Orchestrate for standing programs. For a
selected upstream playbook, read its registered public bridge and its pinned
source in full. Copy the source's ordered todos verbatim. Keep every skipped todo
with its reason; do not replace the procedure with the bridge's summary.

The three excluded leaf skills are automate-me, make-bot-ui and
typescript-best-practices. Their source is preserved for inventory completeness,
but they are not registered or authorized by this restoration. Benny's service
bundle is also inactive. Do not invoke inactive source as an installed capability.

## Native workers and role models

Translate Cursor Task to the current host's native agent tool. Each new work
round gets a fresh worker. Preserve the core's narrow resume exceptions and the
scoped-worker direct implementation exception; do not recursively delegate the
same assignment. Claude Code uses the registered hugues-agent when available.
Codex prepends that wrapper to the fresh worker's prompt. Supply absolute paths
to the public mode, plugin skills directory, pinned core and all three adapters,
the exact base/head, writable scope, success predicate and evidence destination.
Read the mode and applicable principle leaves in full before work. If the host
cannot preserve required context isolation or parallelism, mark that phase blocked.

The no-comments Task role `Comment Sicko` uses the registered
`hugues-comment-sicko` agent in Claude Code. Codex prepends that specialized
wrapper and reads the complete pinned comment-sicko agent before the fresh worker
acts. Do not substitute a generic worker without those rules. Preserve its exact
comment exceptions, scope fence, MUST KILL proof and no application-code edits;
the no-comments coordinator retains rejection, one rerun and failure rules.

The pinned per-role defaults remain defaults. A panel launches one worker per
configured entry, including each auto or inherit-parent alias. List length sets
cardinality. Aliases omit model overrides; they are explicit configuration,
never an implicit replacement for every default. Report same-model process
independence separately from family diversity.

Enumerate models actually exposed by the native tool. Preserve each core skill's
fallback sequence on rejected slugs, using only confirmed capabilities; record
the requested and actual family/model/effort. If no allowed equivalent is exposed,
mark the seat blocked and ask for an explicit configuration choice. Never invent
an available model or label a blocked seat completed. Do not update or publish a
default-fix PR without publication authority.

`setup-huguesstack` uses the pinned detect → load → budget/map/confirm → validate
→ write → confirm → optional verification sequence. Translate the Cursor global
rule path to project-local `.huguesstack/models.md`. Read it before all role
selection; deleting a role restores its pinned default. Write only after the
skill's confirmation and current filesystem authority. Keep every role and panel,
the four budget choices and availability validation. This file is guidance;
restoring the plugin does not execute setup or change any user's configuration.

## Tools and authority

Translate AskQuestion, todos, filesystem and Git operations to actual host tools.
No translation grants new authority. Consumer execution/edits, network data
transmission, installations, credentials, system settings, pushing, PR publication,
merging and releases use the user's current scope. Stop the dependent action when
authority or a necessary capability is absent and continue independent work.

The pinned Bun helpers include a bootstrap that can install dependencies.
Do not execute it without installation authority. First inspect local runtime and
cached dependencies. A missing runtime, dependency, cloud worker, forge API or
loop primitive blocks that operation; preserve its intended gate and report the
gap. Native local workers substitute for cloud only where the core permits local
execution; do not simulate a race sequentially. Nothing in Babysit, Shipping or
Orchestrate arms a remote action without explicit scope.

Cursor create-skill translates to an available agent-writing skill plus this
repository's package checks. Before commits, use an available deslop equivalent
and the pinned unslop and technical-writing skills; retain no-comments before
review. Missing external control-cli, control-ui, deslop or writing-for-agents is
reported as a capability gap, never silently marked performed. The bundled pinned
unslop remains the prose contract; an owner's differently worded skill is an
additional style preference, not a source-equivalent replacement.

Opening a PR retains the core's ready-PR and stack/base mechanics. Local commits
and a PR-ready body can be prepared under local-work authority. Publication waits
for explicit scope. The project PR policy adds Astra High review; it does not
change generic interrogate defaults or claim diversity from identical models.
