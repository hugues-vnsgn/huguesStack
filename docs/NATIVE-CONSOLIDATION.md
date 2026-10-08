# Native skill consolidation candidate

This unreleased candidate consolidates the 0.2.0 layout at `4ae13bb` without
changing the public set of 50 skills, 23 generic playbooks, four mobile playbooks,
two agents or 15 specialized worker roles. No release, installation or live host
execution is implied by this document.

## Layout and ownership

Each `plugin/skills/<name>/SKILL.md` owns its native metadata and full workflow.
Owned references and scripts remain alongside it. `agents/openai.yaml` contains
Codex invocation metadata only. There is no second procedure body, runtime core
mirror, symlink shadow or custom discovery registry. The former generated
entrypoints are authored files now; `render_core.py` refuses to regenerate them.

The two historical aliases remain `poteto-mode` → `hugues-mode` and
`setup-pstack` → `setup-huguesstack`. Public native paths remain stable, including
paths an owner may have used to disable skills. Different installation roots can
still affect path-based host settings; reconcile those explicitly during an update.

All 161 original source files, their modes and bytes are retained in
`provenance/upstream/pstack-0.15.9.tar.gz`, outside runtime discovery. The
Git-object snapshot independently checks the archive. The current adaptation
map is `docs/upstream/consolidation.json`. The original releases and their frozen
tests are retained. `docs/upstream/core-restoration.json` remains the historical
0.2.0 restoration receipt; `consolidation.json` is the current installed receipt. Upstream byte equality applies to the archive; it is no
longer a claim about the adapted runtime tree.

The upstream human guide lives under `docs/pstack/`. Benny's Cursor automation,
the Cursor manifest and the legacy history-scanning cleanup shell script remain
provenance-only. The installed artifact includes the original MIT notice.

## Invocation and resources

Use native skill invocation for a consumer or external skill. Read ordinary
owned references only when the current phase needs them. A consumer or
external skill is not a reference-file fallback: unavailable, owner-disabled,
denied or unknown invocation stops its dependent phase. A manual handoff is
needed only when the host requires explicit user invocation; it is not a
proven universal limitation in this setup.

Upstream Cursor metadata marks 49 skills manual-only; `poteto-mode` is the one
exception. huguesStack restores that design instead of the earlier native
table that made 46 skills model-invocable: only `hugues-mode` and
`setup-huguesstack` are model-invocable now, so only their descriptions enter
startup context on Claude Code. The other 48 bundled skills are user-only; the
owner can still type any of them by name, and the mode reaches each one as its
router's reference, reading its SKILL.md in full instead of invoking it
natively. `hugues-agent` preloads `hugues-mode` through the Claude Code agent
`skills` field and invokes it natively when the preload is absent; whether the
plugin-scoped name `hugues-stack:hugues-mode` resolves is unobserved. Generated
project verification skills stay consumer-local and model-invocable so proof
steps can drive them; that tier is unrelated to the bundled table above.

The host adapter takes precedence over inherited sibling-read wording. It also
prevents unconditional traversal of navigation links. A figure-it-out consultation
of mode principles must not restart mode routing. This is an instruction contract,
not a filesystem security boundary or proof of every possible runtime trace.

The shared contract now loads specialized adapter references only before their
named phases. Mobile applicability is a small separate entry; explicit mobile
work must load the complete mobile rules before routing or execution. All prior
adapter requirements are retained. See [progressive disclosure](CONTEXT-FOOTPRINT.md)
for the partition and comparable required-read inventories.

The installed `read-workflow` helper refuses public `SKILL.md` files and their
legacy aliases. `translate-plan` also rejects such reads. Plans must name native
skill invocation explicitly; owned playbook/reference rereads stay binding-guarded.
The translator preserves consumer-owned Git reads and supports only its documented
bounded literal shapes. It does not become a host dispatcher or shell interpreter.

## Integrity and cleanup

The installed manifest covers canonical instructions, metadata, helpers, adapters
and policies, with complete file inventory and permission modes. Three linked
trust anchors avoid a circular self-hash: the bootstrap verifies runtime source,
the verifier binds the manifest, and the saved binding records every plugin file
including those anchors. A changed install, file, permission or inventory holds.
The bootstrap is still the trusted entrypoint; this is drift detection, not a
signature system against replacement of all code and trust anchors.

Run `python3 scripts/seal_payload.py` after intentional edits, review its diff,
update source-provenance receipts for changed retained families, then run all
checks. Sealing refuses a changed canonical destination unless each reviewed
file is named with `--accept <repository path>`; an edit is not re-approved by
hash regeneration alone. `docs/HELPER-INPUTS.json` is checked against the
installed helpers, so its byte-identity claims cannot go stale. The receipts live
in this repository: `--accept` makes a canonical change deliberate and visible in
review, it is not an external signature. Hash regeneration cannot approve lost
workflow gates. Never regenerate
receipts as a consumer workaround for drift. Old 0.2.0 program bindings fail;
review and explicitly rebind migrated programs.

The activity parser and audit logic are unchanged. Missing/empty/unsupported
activity and unknown PR state remain holds with exit 2. The audit grants no
deletion authority; active/pinned-chat verification remains a separate gate.
Only synthetic transcripts and disposable Git consumers are used in current tests.

## Validation and limitations

See [test accounting](TEST-COVERAGE.md) for current versus historical totals.
Current checks exercise actual installed helpers, negative inventory/mode/body
mutations, native-body read rejection, public names, workflow phase contracts,
owned links and parser/audit safety. Context budgets are measured source bytes
and characters, with characters/4 as an explicit token estimate; they are not
observed host prompt usage. Initial bug-fix routing, including its full playbook,
todos and required unslop reply guidance, is now 34,456 bytes versus 45,289 before
disclosure, about 8,604 versus 11,308 estimated tokens. The larger workflow inventories include their required
transitive skills and resources. Native frontmatter is 13,431 bytes after the host
invocation table removed 45 inherited manual-only lines and the setup description
named the native model-role file. Workflow bodies excluding frontmatter change only
where nine skills replace Cursor model-role wiring. These are source budgets;
actual startup exposure, full execution cost and runtime savings remain unknown.

Live discovery/invocation, disabled-skill and planning behavior remain
UNVERIFIED for this consolidation candidate. Separate prior-layout trials cannot
validate this source revision. No native host session was run against this candidate. Generic workflow content and mobile scope rules are retained; mobile
redesign and optional automatic cross-skill composition are separate future work.

Implementation review can proceed on this finite contract. A green static suite
does not establish full runtime parity, unattended execution, native transcript
compatibility, or mobile device/forge/cloud/loop behavior.
