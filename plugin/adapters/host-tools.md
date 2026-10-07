# Installed planning and worktree audit commands

These are mechanical translations of bundled operands in the pinned playbooks.
Read the full selected core first and preserve its todo order, verification rules,
explicit execution go and active/pinned-chat gate. Python 3 and Git must already
be available; plan validation also needs Node. Missing tools block the gate.
The adapters do not install dependencies, fetch, query a forge or delete anything.

## Bind and reread the approved installed payload

Resolve `<plugin>` from the loaded public entrypoint, not the consumer directory.
Use absolute paths below. The plugin may be an installed directory without Git.
At program authoring, save a binding in the authorized program evidence directory:

```sh
python3 "<plugin>/adapters/host_tools.py" bind > "<program>/plugin-binding.json"
```

The binding records pstack's approved revision, the shipped 161-file hash/mode
manifest, installation path and every non-core plugin file’s hash and full permission mode.
Extra core files also block the binding. Record the plugin's
Git commit separately when the installation has one. At every required tick,
reread bundled files through the same saved binding:

```sh
python3 "<plugin>/adapters/host_tools.py" read-workflow --binding "<program>/plugin-binding.json" pstack/skills/swarm/SKILL.md
```

Replace each filled `git show origin/main:pstack/...` operand in multi-phase-plan,
autopilot-full and autopilot-stack with that command for its exact pinned path.
This translates the bundled workflow source from consumer trunk to the approved
installed payload. Keep consumer-owned `git show origin/main:<control skill path>`
and plan/source reads on consumer trunk. Fill skeleton placeholders first, then
translate a plan to a different output file for inspection:

```sh
python3 "<plugin>/adapters/host_tools.py" translate-plan --binding "<program>/plugin-binding.json" "<program>/plan-draft.md" > "<program>/plan.md"
python3 "<plugin>/adapters/host_tools.py" plan-check --binding "<program>/plugin-binding.json" "<program>/plan.md"
```

The latter replaces `node pstack/skills/poteto-mode/scripts/check-plan.mjs <plan.md>`.
It runs the unchanged installed Node helper with an absolute consumer plan path
and preserves its exit code/diagnostics. Translation resolves executable bundled operands and plain pinned paths
to the installed payload; plain paths are references, and executable rereads must
still use `read-workflow` with the saved binding; inspect the resulting plan and use those commands during each
tick. Any binding, hash, mode or required-file drift blocks rereading/validation.
Reconcile changed payloads with the operator; never silently rebind a live program.
These commands do not arm loops or start implementation.

## Audit explicit authorized native activity sources

In worktree-cleanup step 1, replace the Cursor-only upstream shell helper with:

```sh
python3 "<plugin>/adapters/host_tools.py" worktree-audit --binding "<program>/plugin-binding.json" --repo "<consumer>" --sources "<program>/sources.json" --pr-snapshot "<program>/prs.json"
```

The adapter reads paths from the consumer's local Git worktree list, handles paths
with spaces, and inspects local dirty/merge state. `--base` defaults to the local
`refs/remotes/origin/main`; no fetch occurs and freshness is reported unverified.
It does not enumerate native history directories. Supply only roots or individual
files covered by the user's current authority, including authorized subagent
records. Never discover private history to fill a missing source. For example:

```json
{
  "schema_version": 1,
  "coverage": "complete",
  "sources": [
    {"provider": "claude", "files": ["/absolute/authorized/session.jsonl"], "authorization": "owner-approved source scope", "coverage": "complete"},
    {"provider": "codex", "root": "/absolute/authorized/session-directory", "authorization": "owner-approved source scope including subagents", "coverage": "complete"}
  ]
}
```

The supported hosts are Claude Code and Codex. Cursor sources are ignored without
reading them; they contribute no evidence or coverage for these hosts. A manifest
containing only ignored sources remains unavailable. Supported sources determine
coverage independently; no Cursor source is required.

`complete` is the owner's explicit assertion that the supplied set covers all
relevant supported-host chats and sibling trees; a successful scan cannot establish that
assertion. Mark either level `partial` when coverage is uncertain. No sources,
partial coverage, unreadable/missing/changed files, symlinks, unsupported envelopes
or malformed records produce unavailable coverage and a hold (exit 2). A complete
empty root, empty file list, or empty/whitespace-only transcript also holds.
Duplicate JSON keys and JSON nesting over 64 levels hold instead of hiding records. Valid complete sources with no recent evidence report that limited result.

Supported inputs are Claude JSONL user/assistant records and string summaries
and Codex JSONL session/turn/response records including JSON-encoded function
arguments. Claude content blocks are text, tool_use, tool_result and plaintext
thinking, with required content fields. Tool-result content is a string
or a list of text leaves with only `type` and string `text` fields; nested,
malformed or opaque result blocks hold coverage. Codex messages require a known
role and a content list of input_text/output_text blocks with
their required fields. Missing, malformed or unknown blocks hold.
Nested progress envelopes and unknown block/tool types hold
coverage for inspection. Codex tool outputs require a nonempty call identifier
and string output. Reasoning permits only reviewed plaintext summary/content
blocks; encrypted reasoning holds. Textual agent/user events require string
content and no opaque attachments. Other events, web-search responses, Claude
system/history/queue records and redacted thinking have no reviewed content
schema and hold. Unsupported records/files keep coverage unavailable while
independent later records/files can retain activity hints. Those hints are
labeled as validated records or unparsed path hints, never as deletion safety.
Opaque records invalidate inherited relative context until a reviewed context
resets it. Envelope/message metadata also uses bounded fields and types;
unknown metadata, including unreviewed usage structures, holds. Other formats hold.
The scan is conservative: exact worktree paths,
child paths and session working directories count as activity even in quoted
messages. Encoded function arguments are decoded; relative path operations need
session or tool working-directory context. Each operation retains its own context;
relative tool working directories resolve against their enclosing session.
Codex operation-local directories never replace persistent session/turn context.
Session/turn contexts need an absolute working directory and reviewed string
metadata fields; unknown context fields or opaque metadata hold. Operations without a
resolvable working directory or absolute operation path hold.
Simple shell operands and bounded native patch
file headers resolve relative to that context, including sibling worktrees and
parent-directory scopes and sequential `git -C` directory changes. Shell support is deliberately bounded to cat, ls, head,
tail, wc, stat, rg, grep, git status, pwd, readlink and realpath with literal
operands and a finite option allowlist. Unknown options, command paths outside
the reviewed bare/system forms and preprocessors hold. Compound commands,
expansions, arbitrary programs and unknown tool
operations hold coverage for inspection; the adapter never executes transcript
commands. Patch envelopes, operation headers, moves and hunk/body lines must
fit the bounded grammar; unknown directives or unconsumed content hold.
Sed, find and other embedded programs hold. Claude file operations support
Read/Write/Edit with required `file_path` and tool-specific fields; unknown fields
or wrong types hold. Glob/Grep/MultiEdit and unknown file tools hold for inspection.
Missing/malformed
function arguments or tool inputs also hold. This is a conservative operand scan,
not a prediction of every program's implicit filesystem access or side effects.
Record timestamps take priority; missing timestamps use file
mtime conservatively and label that evidence. Recent means within four days.
This is supported-format synthetic evidence, not attestation of every host version.

Optional PR input is a local owner-supplied snapshot, for example
`{"coverage":"complete","states":{"branch-name":"NONE"}}`. States are
`OPEN`, `CLOSED`, `MERGED` or `NONE`; omitted/unknown PR or merge state holds. A
snapshot's freshness and completeness must be checked separately before pruning.
Missing, unreadable, invalid or incomplete PR metadata returns exit 2 even when
activity coverage is complete; `metadata_coverage` and `pr_snapshot_error` explain
that result. Unknown PR/merge state holds scratch candidates as well.
The report retains source paths and timestamps, never transcript bodies. Size
and disk measurements remain the separate core `df`/local disk inspection steps.

Buckets are advice. Dirty tracked work, open PRs and unavailable activity hold;
recent activity requires verification. A clean merged candidate with complete
no-recent evidence reaches `verify-active-pinned`, never deletion permission.
Obtain the real active/pinned-chat set separately, including sibling worktrees,
and apply core steps 2–4. Every row says `deletion_authorized: false`. This adapter
never prunes or deletes, and no automated deletion is established by its tests.
