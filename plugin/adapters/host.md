# Claude Code and Codex host adapter

Apply this adapter and the mobile applicability section before the canonical workflow. Follow the consumer project’s own PR policy. These adapters translate host
mechanisms and limit authority; the canonical skill owns workflow
phases, mandatory gates, panel cardinality, fallback and stop rules. A constraint
can block execution. It cannot turn an omitted gate into success.

## Loading and routing

Native discovery uses each canonical `skills/<name>/SKILL.md`. There is no
custom runtime registry or custom host loader. `poteto-mode` maps to `hugues-mode`,
`poteto-agent` to `hugues-agent`, `Comment Sicko` to `hugues-comment-sicko`,
and `setup-pstack` to `setup-huguesstack`; other public names are unchanged.

Invoke each bundled, consumer or external skill through the host's supported native mechanism. Respect
manual-only selection, owner-disabled entries and native denials; never use a file read as an invocation fallback.
Unavailable, disabled, denied or unknown invocation stops the dependent step.
When supported execution requires explicit user invocation, provide the exact
native command and wait; do not imply this handoff is always required. A model's
printed slash or dollar command is not proof that a native invocation occurred.
An available file or a successful binding check establishes no skill permission.
Read ordinary references owned by the invoked skill only when its phase needs them.
Resolve relative resources from their owning file or the stated mode root, never
from the consumer cwd. Do not recursively traverse navigation links or eagerly
invoke all linked skills. This contract overrides inherited raw sibling-read wording.
For a principles consultation from figure-it-out, use already-loaded mode context
or a supported native invocation scoped to principles only: never restart task routing.
A fresh worker must obtain its own native context; a parent's claim of permission
is insufficient. Missing capability holds the phase without scanning user settings.

For executable operands in planning and cleanup, use the installed
[host tools](host-tools.md) and [entrypoint](host_tools.py). In multi-phase-plan,
replace the consumer-relative Node command with `plan-check`. Translate bundled
`git show origin/main:pstack/...` reads in that plan and autopilot-full/stack to
`read-workflow` using the program's saved installed-payload binding at every tick.
Consumer-owned trunk reads stay on consumer Git. In worktree-cleanup step 1 use
`worktree-audit` with explicit authorized native source inputs. Unknown activity
coverage holds candidates; the separate active/pinned-chat gate remains required.
The supported native hosts are Claude Code and Codex. Ignore Cursor transcript
sources without reading them or counting them as supported-host coverage.
These are mechanical operand translations, not new execution or deletion scope.

The mode applies the pinned router, including figure-it-out for large,
cross-cutting or unmatched work and Orchestrate for standing programs. For a
selected playbook, read its canonical file in full. Copy its ordered todos verbatim.
Keep every skipped todo with its reason.

All 50 top-level skills are registered, including automate-me, make-bot-ui and
typescript-best-practices. Resolve recall's habit-to-skill handoff through the
native automate-me entry. Registration grants no permission to process personal transcripts,
author a personal mode, create bot/webhook integrations, transmit data, request
credentials, expose a server or install/configure Tailscale. Execute those steps
only under the user's current explicit scope and the pinned confirmation rules.
Unavailable tools block their dependent phase without changing its contract.
Benny is a separate nested service bundle and is not a top-level skill or agent.
Its source is preserved only in the nondiscoverable upstream provenance archive;
it is not a supported native service or helper.

Translate Cursor skill placement to the consumer's established `.agents/skills`
or `.claude/skills` convention. Preserve existing personal-mode categories and
user edits; global placement or configuration needs explicit scope. Use only the
active workspace's supplied transcript paths, never unrelated project history.
Without an authorized transcript source, automate-me history mining remains blocked;
do not fabricate preferences or claim personal-mode execution from a routing check.
Reflect retains the pinned current-session digest fallback when no transcript path
resolves. Use only the authorized conversation already available to the coordinator;
label the digest's source and coverage limits. A digest grants no access to personal
history and no permission to apply Reflect's proposed edits. Preserve Recall's
explicit state-capsule shortcut; do not pretend a digest proves a transcript audit
for show-me-your-work or supplies automate-me's repeated historical evidence.
TypeScript paths remain `**/*.ts` and `**/*.tsx`; apply its registered guidance
when reading or editing those files and invoke principle-type-system-discipline first.
The original path metadata is preserved in the canonical entry. If a host ignores it,
select the skill explicitly by the actual file type. Mobile specialization adds
applicable guidance through the mobile adapter without deleting other languages.

## Native workers and role models

Translate Cursor Task to the current host's native agent tool. Each new work
round gets a fresh worker. Preserve the core's narrow resume exceptions and the
scoped-worker direct implementation exception; do not recursively delegate the
same assignment. A core `poteto-agent` call uses the registered hugues-agent in
Claude Code; Codex uses the role instructions through its supported fresh-worker mechanism. Supply absolute paths
to the public mode, plugin skills directory and the host adapter and applicable mobile adapter,
the exact base/head, writable scope, success predicate and evidence destination.
Obtain the mode and applicable principles through supported native invocation before work. If the host
cannot preserve required context isolation or parallelism, mark that phase blocked.

For routed research/review calls, preserve `generalPurpose` and the workflow's
own prompt, readonly/agent-mode requirement, model, cardinality and handoff order.
Do not replace these workers with `hugues-agent`.
Cursor's `generalPurpose` maps to Claude Code's native `general-purpose` agent;
Codex uses a fresh native worker with that role's prompt. Use the actual native
tool's exposed agent type rather than sending an unsupported Cursor spelling.
Each owning skill names its complete worker prompts alongside its workflow.
The maintainer provenance receipt records 15 role mappings; it is not a host registry.
Read the selected role's ordinary prompt reference, fill its named placeholders,
and preserve the owning workflow's order, cardinality and context isolation.
For simple how, omit explorer findings exactly as directed. Why retains its
category playbooks; reflect synthesis receives all three full outputs. Architect
passes its runner brief through arena. Native-invoke that dependency when supported;
never read arena's body as a substitute. Inline briefs remain with their owner.
General-purpose native workers receive absolute source,
adapter and fixture paths, scope and success predicate, without a mode persona.
Agent mode preserves available tool access; it never grants permission to write
or query external sources. Missing authorized tools remain explicit coverage gaps.

The no-comments Task role `Comment Sicko` uses the registered
`hugues-comment-sicko` agent in Claude Code. Codex supplies that canonical specialized role through its supported fresh-worker mechanism before work. Do not substitute a generic worker without those rules. Preserve its exact
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
for explicit scope. Only this huguesStack repository’s AGENTS.md activates its
Astra High PR profile. Installing the plugin does not impose it on consumers.
Consumer policies and generic interrogate defaults remain in force.
