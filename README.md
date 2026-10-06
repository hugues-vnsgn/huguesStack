# huguesStack

huguesStack adapts pstack for mobile work in Claude Code and Codex: Swift/iOS,
Kotlin/Android, KMP shared logic and CMP shared UI. Consumer apps remain in
separate repositories.

This checkout includes the WP1 package, WP2 mode/playbooks, WP3 proof lane,
WP5 upstream sync and **WP6 workflow/evidence documentation**.
`hugues-mode` selects one of fourteen playbooks, copies its steps into a todo list and names
the mobile proof required. The package includes a fresh-task worker,
`interrogate` review guidance and the 24 verbatim upstream principles.
The eight approved retained tools add research, design, regression proof, downstream
safety checks, bounded recipe maintenance and recurring-mistake enforcement. The
package now ships 35 skills; read [retained integration](docs/retained-integration.md)
for direct playbook handoffs and source receipts. WP3 adds a project-local verification generator, jev Drive guidance and a durable
Markdown evidence outline. Version **`0.1.0`** contains this Layer 1 package.
See the [release notes](docs/RELEASE-0.1.0.md) for evidence and gaps.
Combined [PR #13](https://github.com/hugues-vnsgn/huguesStack/pull/13) merged
into main at `18c73d183f19ed9b401f4b58c6743705a6bfc3da`.
Consult [GitHub Releases](https://github.com/hugues-vnsgn/huguesStack/releases)
for publication and final-check receipts.

New PR reviews use independent GPT-6 Astra reviewers with High effort. Read the
[PR review policy](plugin/skills/hugues-mode/references/pr-review-policy.md) before
launching a reviewer or re-reviewing a final head. Historical Claude review
receipts and Claude host compatibility checks retain their stated scope.

Start with the short [workflow guide](docs/WORKFLOW.md) and
[support matrix](docs/support.md). Use `/hugues-stack:hugues-mode` in Claude Code,
or the documented Codex manual project-skill/direct-read fallback in
[host loading](docs/host-loading.md); native Codex installation/invocation remains
unverified. Historical RC1 read-only previews matched 16 cases across all fourteen
playbooks and `interrogate` in both hosts, with displayed checklists, on
`21a82942019292f7212ff1185e9ef187ac96e86d` plugin bytes. RC2 changes those
bodies and adds eight tools. Later repaired planning previews passed six unique
cases and 36 copied steps per host; all 79 tested RC2 plugin fingerprints match
committed `68cb710`. The 0.1.0 manifest changes version metadata only within the
plugin; these historical probes establish no fresh 0.1.0 host load.
See [RC2 host validation](docs/rc2-host-validation.md) and the bounded
[Swift/Kotlin feature proof](docs/rc2-native-feature-proof.md). The
[RC validation receipt](docs/rc-validation.md) records the domain limits and
bounded synthetic delegation pass, including its initial setup failure.
Give it a goal and a way to check it. For example:

```text
The discount boundary is wrong in shared code. Fix it once and show me it passing on Android and iOS.
```

For a planning-only check, request a **route preview**. The mode reads the chosen
playbook and returns its numbered steps, domain and proof requirements, then
stops before delegating or running consumer commands.

Run the static checks with Python 3 and a POSIX shell:

```sh
./scripts/check-plugin.sh
python3 -m unittest discover -s tests -v
```

The [evidence index](docs/evidence-index.md) separates merged packages, the deferred draft,
historical passed checks and current blocked/unrun proof. See
[WP3 validation](docs/wp3-validation.md) for the proof-lane scope and
[WP2 validation](docs/wp2-validation.md) for acceptance cases and check boundaries.
The [public plan](docs/PLAN.md) summarizes the release scope; private planning
snapshots remain local in ignored `docs/planning`. The deadline remains
9 October 2026, end of day GMT+7. Consumer feature maps and the proposed CLI-first
verification feature remain deferred until after the first release.

## License and attribution

Original huguesStack files use the [MIT license](LICENSE), copyright 2026
hugues-vnsgn. The workflow is adapted from
[pstack by Lauren Tan](https://github.com/cursor/plugins/tree/main/pstack),
MIT copyright 2026 Lauren Tan. Its notice is preserved in
[PSTACK-LICENSE](PSTACK-LICENSE).

WP2 uses pstack 0.15.9 at
`e43c7ee26e0038c6c1fa8380dd34ce86ff94cb2a`. All 24 principle files are copied
verbatim. Adapted guidance and per-file source hashes are recorded in
[upstream provenance](docs/upstream/wp2-provenance.json). This records the
WP2 inputs; the complete responsibility inventory and weekly procedure are
recorded in the WP5 sync package below.

[Upstream sync](docs/upstream/README.md) records the pstack 0.15.9 pin, full
responsibility ledger and deterministic delta. Validate it with
`python3 scripts/upstream-diff.py check`; weekly triage never overwrites the fork.

WP3 adapts the verification generator from the verified pstack 0.15.5 local
snapshot, omitting its feature-map phase as deferred by the current plan.
Its exact source inputs and adaptation limits are in
[WP3 source receipts](docs/wp3-source-receipts.json). These historical WP3 inputs
remain distinct from the complete WP5 inventory at pstack 0.15.9.
