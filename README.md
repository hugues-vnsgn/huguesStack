# huguesStack

A personal mobile workflow for Claude Code and Codex, based on pstack 0.15.9 at `e43c7ee26e0038c6c1fa8380dd34ce86ff94cb2a`.

This checkout is the **unreleased core restoration**. The 0.1.0 tag and its evidence are preserved. The manifest still carries 0.1.0; that is packaging metadata, not a release or runtime certification of this development branch.

The plugin preserves all 161 upstream source files, registers 47 skills and 23 core playbooks, and adds four mobile playbooks. Entry loaders read the pinned workflow in full after explicit host/mobile adapters and the owner's Astra High PR policy. All 24 principles remain verbatim. No consumer app lives here.

```text
/hugues-mode fix the Swift article list jump; reproduce on the iOS simulator
/hugues-mode investigate this Kotlin search failure and show the code path
/hugues-mode change this KMP boundary; prove Android and iOS callers
/interrogate this diff and distinguish regressions from preferences
```

Read the [developer guide](docs/DEVELOPER-GUIDE.md) for loading, model-role configuration, routing and evidence. [Workflow](docs/WORKFLOW.md) is the short daily reference. [Restoration contracts](docs/CORE-RESTORATION.md) describe preserved contracts, explicit overrides, exclusions and unobserved behavior.

```sh
python3 -m unittest discover -s tests -v
./scripts/check-plugin.sh
python3 scripts/check_core.py
python3 scripts/upstream-diff.py check
python3 scripts/check_whitespace.py
```

The original release contract suite uses an immutable fixture and is historical coverage. Development tests separately verify actual source bytes, ordered phases, loader wiring, override boundaries and local helper behavior. Static checks do not establish restored host/mobile runtime equivalence. [Support receipts](docs/support.md) apply only to their recorded released revisions.

Automate-me, make-bot-ui, typescript-best-practices and Benny remain inactive source. External control tools and unavailable models are capability gaps. Restoring helpers does not authorize installers, remote actions, device changes or consumer execution. Push, publication, merge and a new release are outside this work.

Forked under MIT; preserve [pstack's notice](PSTACK-LICENSE) and the [pin and ledger](docs/upstream/README.md). A newer upstream version is a separate upgrade.
