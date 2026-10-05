# CMP two-target change

source: huguesStack first-release requirements; conceptual reference to osxsystem/hstack at `99cc6129aea3f702ee6cd3b448e4f67700b4353c`, `packs/mobile/references/kmp-compose-pilot.md`, `packs/mobile/references/platforms.md` and `packs/mobile/references/evidence.md`. No fixture or consumer source is imported.

Own shared UI behavior and prove it on both runtimes.

## Steps

1. Establish the authorized consumer checkout and Android/iOS deployment targets using [mobile lanes](../references/mobile-lanes.md). Read shared UI and interop entry points; use the owner's available `compose-multiplatform-ui` and relevant platform skills, disclosing missing skills.
2. Pin the changed interaction, states and expected UI behavior. For a bug, preserve the failing observation first. Choose an explicit semantics or text-scaling case and device conditions before implementation.
3. Brief a fresh implementation subagent with owned shared/platform files, behavior, target builds/tests and UI success criteria. Account for input, navigation, accessibility and platform interop affected by the change. The worker owns its diff directly and does not recursively delegate; each correction round uses a fresh worker.
4. Inspect the actual diff and run [mobile proof](mobile-proof.md) yourself on an Android emulator and an iOS simulator. Preserve each target's build/tests, driven UI path and screenshots, plus the selected semantics or text-scaling observation. A successful JVM test or one target's screen cannot prove the other.
5. Obtain an independent fresh review of both UI paths and platform boundaries. Resolve findings, repeat coordinator proof and run [opening a PR](opening-a-pr.md) with separate per-target outcomes and remaining gaps.

**Reply:** shared UI behavior, Android and iOS proof, semantics/text-scaling result, independent review and blockers.
