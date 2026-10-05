# Upstream sync

WP5 pins [cursor/plugins pstack 0.15.9](https://github.com/cursor/plugins/tree/e43c7ee26e0038c6c1fa8380dd34ce86ff94cb2a/pstack)
at `e43c7ee26e0038c6c1fa8380dd34ce86ff94cb2a`, committed
4 October 2026 at 00:06:48 UTC. [pin.json](pin.json) binds the version, date,
161-file inventory and pstack tree hash to the checked-in snapshot bytes.
The 0.15.5 [baseline pin](baseline-pin.json) accounts for 158 files.
Fresh public Git fetches reproduced the plan's exact **3 added / 18 changed /
0 removed** paths in [the delta](delta-2eb7ed46-e43c7ee2.md).

[The current ledger](huguesStack-dispositions.json), also available as
[CSV](huguesStack-dispositions.csv), has one active row per upstream file.
The 158 earlier responsibilities and proposals remain in
[baseline-dispositions.json](baseline-dispositions.json); the current ledger
retains their `earlier_proposal` fields and the previous decisions for the
18 changed files. Current decisions follow [the revised plan](../PLAN.md).
The inaccessible prototype ZIP contributes no rows or implementation claims.

Each row distinguishes its decision (`port verbatim`, `port with adaptation`,
`ignore with reason`) from its release target and implementation state.
`present` means the named file exists in this repository; it does not claim
observed host or app behavior. Planned destinations may not exist yet.
`external` means reference an installed skill, subject to availability.
Deferred and omitted responsibilities remain visible with reasons. In
particular, benchmark wiring, feature maps, automatic workflows and Layer 2
helpers are deferred; mobile native/test/UI proof requirements stay intact.

## Reproduce offline

Python 3.9+ and Git are sufficient. No dependency install or upstream code
execution is needed. From the repository root:

```sh
python3 scripts/upstream-diff.py check
python3 scripts/upstream-diff.py diff \
  --from-snapshot docs/upstream/snapshots/pstack-0.15.5.json \
  --to-snapshot docs/upstream/snapshots/pstack-0.15.9.json \
  --ledger docs/upstream/huguesStack-dispositions.json \
  --output docs/upstream/delta-2eb7ed46-e43c7ee2.md --check
python3 -m unittest discover -s tests -v
./scripts/check-plugin.sh
```

Snapshots retain the raw Git commit, root tree and manifest, plus sorted
pstack blob fingerprints (mode, SHA-1, byte SHA-256 and size). Capture reads
every blob and verifies its Git object hash. Offline validation reconstructs
the complete pstack tree and binds it through the root tree to the commit;
it also verifies manifest bytes, version and commit date. The pin's snapshot
SHA-256 anchors the recorded byte fingerprints. Offline validation cannot
rehash unretained blob bodies; a fresh capture verifies those bodies again.
Unsupported symlinks, submodules, incomplete trees, duplicate paths/JSON keys,
stale ledger fingerprints and missing reasons fail closed.

To recapture from public Git, use a separate bare clone outside the plugin:

```sh
git clone --bare https://github.com/cursor/plugins.git /tmp/pstack-upstream.git
python3 scripts/upstream-diff.py snapshot --repo /tmp/pstack-upstream.git \
  --revision e43c7ee26e0038c6c1fa8380dd34ce86ff94cb2a \
  --output docs/upstream/snapshots/pstack-0.15.9.json --check
```

Capture resolves a ref once and records its full commit SHA. Git replacement
objects are disabled. No checkout, filter, upstream script or consumer app runs.

## Weekly triage

Triage at most once a week. This is a manual maintenance procedure, with no
scheduler or unattended publishing. Compare the current pin with public main:

```sh
python3 scripts/upstream-diff.py diff
```

This fetches main into temporary bare Git storage, validates complete evidence
and writes `docs/upstream/delta-<from>-<to>.md`. Paths are sorted; blob changes
and executable-mode changes are reported. Every newly discovered row is
`pending`. Equal input produces equal bytes; existing output is accepted only
when identical. Different existing content is never overwritten, including
human triage notes. Supply a new `--output` path to preserve an earlier report.
Network/fetch failures stop before report generation.

For a candidate re-pin, capture the candidate snapshot as above at its full SHA
and generate a separate ledger proposal:

```sh
python3 scripts/upstream-diff.py reconcile \
  --from-snapshot docs/upstream/snapshots/pstack-0.15.9.json \
  --to-snapshot /tmp/pstack-candidate.json \
  --ledger docs/upstream/huguesStack-dispositions.json \
  --output /tmp/pstack-ledger-proposal.json
```

Unchanged rows keep their decisions. Added and changed rows become pending,
with prior decisions preserved. Removed rows move into `retired_items`, retaining
their fingerprints and decisions; a revived path requires fresh triage.
Review every delta row and supply a disposition, concrete reason, release target,
implementation state and intended destinations. Port principles verbatim.
Read playbook and mode diffs before adapting them; never replace the fork with
upstream files. The tool writes only reports or separate evidence/proposals;
it never updates the pin, ledger or plugin automatically.

Commit the reviewed snapshot, ledger, CSV, pin digest and corresponding delta
in a separately reviewed change. The current `check` command validates the
maintained baseline-to-current report and rejects pending active rows. Export
CSV to a new output path with the validated command below, then include it in
the reviewed update. Existing human edits are never overwritten. Until triage and
checks finish, list the candidate delta as pending in [support](../support.md).
```sh
python3 scripts/upstream-diff.py csv \
  --ledger /tmp/pstack-ledger-proposal.json \
  --snapshot /tmp/pstack-candidate.json \
  --output /tmp/pstack-ledger-candidate.csv
```

A changed pin requires matching WP2 receipts and WP3 generator source
fingerprints, or a reviewed update to those receipts. The WP3 receipt retains
its historical 0.15.5 input revision; its generator blob and byte SHA-256 must
match the current ledger because that input is unchanged at the 0.15.9 pin.
A future changed generator requires source review before re-pinning; stale
provenance is rejected rather than silently accepted.

## Attribution

Keep [PSTACK-LICENSE](../../PSTACK-LICENSE) and the fork's
[LICENSE](../../LICENSE). [WP2 provenance](wp2-provenance.json) names the
source and destination of imported plugin files. Adapted skills/playbooks
retain `source:` annotations. The 24 principles and four interrogate references
remain byte-for-byte upstream copies, with attribution in the receipts instead
of altered frontmatter. The checker binds all WP2 receipts and the present WP3
generator's source fingerprints, adaptation disposition and ledger destinations
to the complete inventory. It verifies bytes at every present verbatim ledger destination.
This sync package adds no skills or mobile app code.
