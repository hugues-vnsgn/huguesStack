# Progressive disclosure and source footprint

The canonical mode still loads in full. Its native invocation, authority and
routing rules remain mandatory. The shared adapter now requires its worker,
helper, history/integration, TypeScript and publication references only before
their named actions. A small mobile applicability file requires the complete
mobile adapter before any explicit mobile task; non-mobile work stops at the
applicability decision. This uses ordinary file reads, not a new native loader.

Every original host instruction is retained in one of those files, and the full
mobile adapter is byte-identical to the previous candidate. The
[partition receipt](ADAPTER-DISCLOSURE.json) and regression checks account for
every original paragraph. Deferral changes when guidance is read, not whether
its triggered requirements apply. Unknown native invocation still holds; a
reference cannot substitute for a skill invocation.

## Comparable source scenarios

The table counts UTF-8 source bytes and estimates tokens as Unicode characters
divided by four. These deterministic counts have no runtime sampling noise.
They measure required bundled instruction inventories, not latency, actual
host prompt usage, or a complete executable workflow cost.

The release column uses frozen `509cbec` source. Before disclosure uses frozen
`7db3e80`, the first reviewed native consolidation. After uses current files.
Each column uses the same scenario and counting method. Full paths, hashes,
assumptions and mandatory transitive inputs are in the
[scenario definitions](CONTEXT-SCENARIOS.json) and
[generated inventory](CONTEXT-BUDGET.json). Regenerate with
`python3 scripts/measure_context.py`.

| Scenario | Released 0.2.0, estimated tokens | Before disclosure | After disclosure | Bytes before → after |
|---|---:|---:|---:|---:|
| Declared startup metadata, all 50 frontmatter blocks | 3,940.25 | 3,700 | 3,357 | 14,803 → 13,431 |
| Initial bug-fix routing, full playbook, todos and unslop reply | 11,331.75 | 11,307.75 | 8,603.5 | 45,289 → 34,456 |
| One-function CLI bug fix with cheap regression test | 35,078 | 33,956 | 32,807 | 135,888 → 131,290 |
| Three-module TypeScript feature with design and implementation arenas | 37,897.5 | 36,551.25 | 35,387.25 | 146,269 → 141,611 |

The routing inventory falls about 23.9% from the previous native candidate.
Complete bundled workflow inventories fall less, because worker dispatch,
verification and publication instructions still apply. The bug-fix profile
includes how, why, TDD, source-control investigation and synthesis prompts,
closing skills, specialized agents and applicable principles. The feature
profile includes complex how, architect, arena, swarm, design references,
TypeScript guidance, closing skills and its applicable principles.

The feature profile is a larger bounded workflow within one subsystem. A large
cross-cutting migration, unattended task or standing program follows the mode's
figure-it-out/Orchestrate routing; its designed phases determine a different
closure. Mobile work also loads additional guidance. Neither is hidden inside
the fixed profile or claimed covered by its total.

## What the counts include and leave unknown

Three canonical skill files remain byte-identical to `7db3e80`: the user-only
automate-me, make-bot-ui and recall entries. Forty-five drop the inherited Cursor
`disable-model-invocation: true` line under the host invocation table. Nine,
including reflect and `setup-huguesstack`, replace Cursor model-role wiring with
project-local `.huguesstack/models.md` and `inherit-parent` defaults. Their
combined whole-file size is 188,701 bytes; bodies excluding frontmatter and
delimiters total 174,970 bytes. The mode file is 20,824 bytes, including its
20,446-byte body. Model-invocable descriptions enter startup
context on Claude Code, where manual-only ones did not, so the declared startup
metadata of 46 skills is now real exposure; its runtime size remains unobserved.
The reduction comes from avoiding unrelated adapter reads, not shrinking or
omitting the procedures. Reducing the mode further by making its own mandatory
sections optional would change its agreed full-body loading contract.

The old 9,182-versus-9,111 comparison counted only mode entry plus unconditional
adapters, before a reply or task. That narrower read set is now 25,980 bytes,
about 6,485 estimated tokens. It must not replace the routing-reply row above,
which also includes the selected bug-fix playbook and mandatory unslop dependency.

Startup metadata is unchanged by this phase split. The table counts all declared
frontmatter as an upper bound; actual host exposure, suppression and framing
remain unobserved. Codex policy files add 2,149 source bytes, unchanged, but those
bytes are not assumed to enter model context. Startup and full-body numbers
overlap and must not be added as though they were independent reads.

The workflow rows count each bundled path once across all participants. Fresh
workers can load it again. The scenarios state five workers for the bug fix,
including one mode worker, and fifteen for the feature, including eight mode
workers. A separately reported mode-worker floor counts the required mode,
agent and applicable shared guidance once per fresh mode worker. It falls from
9,403.5 to 7,784 estimated tokens for the bug-fix worker, and from 75,228 to
62,272 for the eight feature workers. These partial floors exclude other worker
skills, role inputs and evidence; they are not additive to the unique inventories.

External control/deslop/agent-writing instructions, consumer configuration,
source evidence, generated prompts, tool output, retries and native host
overhead have unknown size. Every modeled dependency is counted even if its
invocation would hold in a real host. Complete execution totals remain null.
No live session established the intended on-demand behavior or token savings.

## Helper inputs and evidence limits

The [helper input receipt](HELPER-INPUTS.json) records all 20 original mode-helper
files. Nineteen remain installed; the legacy history-scanning audit is preserved
only as provenance. The installed helpers are unchanged by this disclosure pass.
Eighteen remain byte-identical to upstream. The Node plan validator changed
earlier to accept bound workflow reads and is exercised by current installed
Python/Node tests. The Bun/TypeScript helpers and dependency files did not change
bytes. Their disclosure-pass runtime validation did not run because the harmless
offline sandbox preflight returned `EPERM`. The later review-fix pass ran it on a
scratch install of the candidate: Bun 1.4.2 installed the locked dependencies
through the session proxy, 52 of 52 `bun test orch watch-pr` cases passed and
strict `tsc --noEmit` passed for watch-pr. No result is inferred from prior-layout
trials, and a consumer install on another machine remains unobserved.

Python adapter behavior changed during consolidation and has its own current
tests. This disclosure pass updates its bound inventory/hash constants. Source
identity and old helper passes do not establish current runtime parity. See
[test accounting](TEST-COVERAGE.md) for current versus frozen coverage.
