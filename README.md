# huguesStack

huguesStack adapts pstack for mobile work in Claude Code and Codex: Swift/iOS,
Kotlin/Android, KMP shared logic and CMP shared UI. Consumer apps remain in
separate repositories.

This checkout implements **WP1: package and loaders** from the
[public plan](docs/PLAN.md). It is a development scaffold, version
`0.1.0-dev.1`. The only shipped skill, `hugues-mode`, returns a read-only loader
probe. WP2 will implement the router and playbooks.

Run the static checks with Python 3 and a POSIX shell:

```sh
./scripts/check-plugin.sh
python3 -m unittest discover -s tests -v
```

See [host loading](docs/host-loading.md) for session-local checks and the Codex
fallback, and [support](docs/support.md) for the evidence states. The owner's planning snapshots remain local in ignored `docs/planning`; the public plan
summarizes the authorized scope. The deadline in the plan remains 9 October 2026,
end of day GMT+7.

## License and attribution

Original huguesStack files use the [MIT license](LICENSE), copyright 2026
hugues-vnsgn. The workflow is adapted from
[pstack by Lauren Tan](https://github.com/cursor/plugins/tree/main/pstack),
MIT copyright 2026 Lauren Tan; its notice is preserved in
[PSTACK-LICENSE](PSTACK-LICENSE). WP1 contains no copied upstream skill bodies.

The notice was copied byte-for-byte from pstack's `LICENSE` in a local upstream
checkout at `70b2dc8b4b85c8d5648624ca40d692c421fff32f`, SHA-256
`bc957ca6bee02792566a1a028d105e02e247c6e77cf057061674273da77b200e`.
The plan targets pstack `e43c7ee26e0038c6c1fa8380dd34ce86ff94cb2a`;
WP5 still needs to retrieve and verify that pin and reconcile the inventory.
