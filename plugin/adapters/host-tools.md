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
manifest, installation path and effective adapter hashes. Record the plugin's
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
and preserves its exit code/diagnostics. Translation changes only executable
bundled operands; inspect the resulting plan and use those commands during each
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

`complete` is the owner's explicit assertion that the supplied set covers all
relevant hosts/chats and sibling trees; a successful scan cannot establish that
assertion. Mark either level `partial` when coverage is uncertain. No sources,
partial coverage, unreadable/missing/changed files, symlinks, unsupported envelopes
or malformed records produce unavailable coverage and a hold (exit 2). A complete
empty set of files in an existing authorized root differs from an unavailable
root. Valid complete sources with no recent evidence report that limited result.

Supported inputs are Claude JSONL user/assistant/system/progress/summary/history
records; Codex JSONL session/turn/event/response records including JSON-encoded
function arguments. Cursor complete coverage requires the bounded structured
JSONL envelope: an absolute `cwd`, optional `timestamp`/`role`/`type`, and `message`
with optional `role` and a `content` list of typed text/tool_use/tool_result items.
Recognized tool_use inputs receive the same operation validation as Claude.
Extra envelope fields and unrecognized tool-call encodings hold for inspection.
Cursor text with `user:`, `assistant:` or `[Tool call]`/`[Tool result]` markers and
opaque JSONL messages can supply absolute activity hints, but always report
unavailable coverage. Their unstructured operations cannot establish no-recent
evidence, even if the source manifest asserts complete coverage. Other formats
also hold. The scan is conservative: exact worktree paths,
child paths and session working directories count as activity even in quoted
messages. Encoded function arguments are decoded; relative path operations need
session or tool working-directory context. Simple shell operands and native patch
file headers resolve relative to that context, including sibling worktrees and
parent-directory scopes. Shell support is deliberately bounded to cat, ls, head,
tail, wc, stat, rg, grep, sed, find, git, pwd, readlink and realpath with literal
operands. Compound commands, expansions, arbitrary programs and unknown tool
operations hold coverage for inspection; the adapter never executes transcript
commands. File operations support Read/Write/Edit/MultiEdit/Glob/Grep and
read_file/write_file/list_directory with explicit path fields. Missing/malformed
function arguments or tool inputs also hold. This is a conservative operand scan,
not a prediction of every program's implicit filesystem access or side effects.
Record timestamps take priority; missing timestamps use file
mtime conservatively and label that evidence. Recent means within four days.
This is supported-format synthetic evidence, not attestation of every host version.

Optional PR input is a local owner-supplied snapshot, for example
`{"coverage":"complete","states":{"branch-name":"NONE"}}`. States are
`OPEN`, `CLOSED`, `MERGED` or `NONE`; omitted/unknown PR or merge state holds. A
snapshot's freshness and completeness must be checked separately before pruning.
The report retains source paths and timestamps, never transcript bodies. Size
and disk measurements remain the separate core `df`/local disk inspection steps.

Buckets are advice. Dirty tracked work, open PRs and unavailable activity hold;
recent activity requires verification. A clean merged candidate with complete
no-recent evidence reaches `verify-active-pinned`, never deletion permission.
Obtain the real active/pinned-chat set separately, including sibling worktrees,
and apply core steps 2–4. Every row says `deletion_authorized: false`. This adapter
never prunes or deletes, and no automated deletion is established by its tests.
