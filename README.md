# huguesStack

huguesStack adapts pstack for mobile work in Claude Code and Codex: Swift/iOS,
Kotlin/Android, KMP shared logic and CMP shared UI. Consumer apps remain in
separate repositories.

This checkout includes the WP1 package, WP2 mode/playbooks, WP3 proof lane,
WP5 upstream sync and **WP6 workflow/evidence documentation**.
`hugues-mode` selects one of fourteen playbooks, copies its steps into a todo list and names
the mobile proof required. The package includes a fresh-task worker,
`interrogate` review guidance and the 24 verbatim upstream principles.
WP3 adds a project-local verification generator, jev Drive guidance and a durable
Markdown evidence outline. Version `0.1.0-dev.3` is a development version;
first-release readiness remains unproven.

New PR reviews use independent GPT-6 Astra reviewers with High effort. Read the
[PR review policy](plugin/skills/hugues-mode/references/pr-review-policy.md) before
launching a reviewer or re-reviewing a final head. Historical Claude review
receipts and Claude host compatibility checks retain their stated scope.

Start with the short [workflow guide](docs/WORKFLOW.md) and
[support matrix](docs/support.md). Use `/hugues-stack:hugues-mode` in Claude Code,
or the documented Codex manual project-skill/direct-read fallback in
[host loading](docs/host-loading.md); native Codex installation/invocation remains
unverified. Give it a
goal and a way to check it. For example:

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

The [evidence index](docs/evidence-index.md) separates merged packages, open drafts,
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
