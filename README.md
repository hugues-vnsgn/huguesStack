# huguesStack

huguesStack adapts pstack for mobile work in Claude Code and Codex: Swift/iOS,
Kotlin/Android, KMP shared logic and CMP shared UI. Consumer apps remain in
separate repositories.

This checkout adds **WP2: mode and playbooks** to the WP1 package. `hugues-mode`
selects one of fourteen playbooks, copies its steps into a todo list and names
the mobile proof required. The package includes a fresh-task worker,
`interrogate` review guidance and the 24 verbatim upstream principles.
It is a development version, not the 0.1.0 release candidate.

Use `/hugues-stack:hugues-mode` in Claude Code, or `$hugues-mode` through the
Codex loading path described in [host loading](docs/host-loading.md). Give it a
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

See [WP2 validation](docs/wp2-validation.md) for acceptance cases and check
boundaries, and [support](docs/support.md) for observed evidence and gaps.
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
WP2 inputs; the full responsibility inventory and weekly sync remain WP5 work.

[Upstream sync](docs/upstream/README.md) records the pstack 0.15.9 pin, full
responsibility ledger and deterministic delta. Validate it with
`python3 scripts/upstream-diff.py check`; weekly triage never overwrites the fork.
