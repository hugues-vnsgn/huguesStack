# Mobile lanes

source: huguesStack first-release requirements; conceptual reference to osxsystem/hstack at `99cc6129aea3f702ee6cd3b448e4f67700b4353c`, `packs/mobile/skills/mobile-proof/SKILL.md`, `packs/mobile/references/platforms.md`, `packs/mobile/references/evidence.md` and `packs/mobile/references/kmp-compose-pilot.md`. No consumer code or managed-worker runtime is imported.

Read this file before a mobile build, bug fix, feature, refactor, prototype or proof. The selected lane binds the target and observations, not just a command name.

## Authority and discovery

Establish the consumer repo, revision, worktree, permitted files and execution authority from the owner's instruction. A generic mode request or a plan naming an app grants no consumer edit, copy, build, install or runtime authority. Keep consumer apps and copied fixtures outside the plugin; preserve tracked fixture baselines. If authority is missing, perform the authorized read-only investigation and report the required scope.

Read the consumer's AGENTS.md and build configuration before selecting argv. Identify Xcode project/workspace, schemes, test plans and destinations; Gradle wrapper, modules, flavors, targets and source sets; native entry points; and existing verification scripts. Use repository-supported commands and explicit target/device identities rather than cached versions or guessed tasks. For the plan's selected consumers, verify the actual `NetNewsWire-iOS` scheme and `demoDebug` variant before use.

Keep SDK/JDK selection process-local when authorized. Missing tools, licenses, signing, credentials or system changes are blockers to name, not implied repair authority. Serialize simulator and emulator runs when local resource contention would mix evidence. Allocate, boot, install or stop a runtime only within the owner's scope; retained artifacts must survive cleanup.

## Required lanes

| Domain | Build and tests | Behavior proof | Relevant installed owner skills |
| --- | --- | --- | --- |
| Swift/iOS | Repository-selected Xcode build and relevant XCTest slice on the explicit simulator destination. Preserve xcodebuild logs and xcresult. | Drive the changed user path on that iOS simulator and retain screenshots/verdict. For a bug, preserve the failing path before the fix. | `ios-tdd-practitioner`, `swiftui-expert-skill`, `uikit-expert` |
| Kotlin/Android | Wrapper-selected unit tests, relevant instrumentation tests for affected platform behavior, and selected APK variant. Use `demoDebug` for nowinandroid; preserve Gradle/JUnit reports and APK identity. | Install that APK and drive the changed path on the explicit Android emulator. For a bug, preserve the failing path before the fix. | Repository's Kotlin/Android guidance and test skills |
| KMP shared logic | Execute common tests on each Android and iOS target, plus affected platform tests and native builds. Preserve each target's result and exported API identity. | Exercise at least one Android native caller and one iOS native caller of the changed shared contract. Check affected export, threading, cancellation, lifecycle and error behavior. | `kmp-boundaries`, `kmp-ios-integration`, `kmp-test-seams`, `tdd-kmp`; `kmp-ktor` for networking |
| CMP shared UI | Build/test affected targets and native hosts; retain separate Android and iOS results. | Drive the changed shared UI on an Android emulator and an iOS simulator. Preserve screenshots and one explicit semantics or text-scaling observation, accounting for both runtimes and affected interop. | `compose-multiplatform-ui` plus relevant native and KMP skills |

Load an installed owner skill only at its relevant decision point. These skills are external prerequisites, not shipped files; if one is absent, disclose the gap and use the consumer's documented guidance within authority. A missing leaf is never a successful invocation.

For changes spanning domains, select every affected lane. A linked framework is build proof; it does not prove a native caller ran. JVM tests do not establish iOS behavior. A simulator screenshot does not establish physical-device performance.

## Evidence and outcomes

Store each authorized run outside the repository in a task-specific evidence folder, for example `~/huguesstack-evidence/<date>-<task>/`. Preserve raw logs, xcresult bundles, JUnit XML, UI reports and screenshots next to evidence.md. Record:

- Plugin SHA, host name/version, consumer repo and SHA, and any dirty consumer diff that changes the tested artifact.
- Domain, scheme/variant, target and explicit simulator UDID or emulator serial/API identity.
- Every command as an argv array, its exit code, run outcome and artifact paths. Include failed attempts and retries.
- Tested app/APK/framework identity where applicable, using an artifact hash and the path that ties build, install and observation together.
- The original failing observation for a bug, final observation, independent review type, and every missing prerequisite or excluded target.

Inspect reports as well as exit codes. An exit code of zero with zero relevant assertions is incomplete. A skipped assertion is skipped, never passed; a retried or flaky assertion is flaky, never a clean pass; a wrong-target result is invalid for the requested target. Keep artifact provenance separate when several result files exist. A later pass does not erase a failed attempt.

Report run outcomes (pass, fail, flaky, skipped, incomplete) separately from support states (authored, static-tested, observed-pass, observed-fail, blocked, deferred). A completed playbook with a blocker still lacks that observed proof. The personal-workflow bar permits disclosed gaps; it never permits invented passes.

## Missing capabilities

Use the available jev-ios-bridge mobile skills for judged screen proof after confirming their prerequisites and scoped execution authority. If the bridge or its required tools are unavailable, use authorized XCTest UI tests and simulator/device tooling for iOS, or instrumentation/UI tooling and adb screenshots for Android. Label this fallback **no judged verdict**, record what it actually observed and list the missing bridge proof. Screenshots alone do not show that the interaction passed.

If the runtime, host, device or execution authority is absent, mark the check blocked with that prerequisite. Keep the required check in the todo list. Finish the available checks and report the gap; do not replace runtime or native-caller evidence with compilation.

Consumer-app feature maps and the new CLI-first token-saving strategy remain deferred until after the first release. Continue the existing required build/test commands and native/UI checks; these playbooks add neither deferred feature to release acceptance.
