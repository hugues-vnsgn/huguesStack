# Verification continuation

This receipt records a bounded snapshot on 5 October 2026, after WP3 and WP5
merged. Raw consumer identities, source, selectors, device IDs, captures,
credentials and reports remain in private evidence outside this repository.
The target remains end of day **9 October 2026, GMT+7**.

## Integrated framework

[PR #4](https://github.com/hugues-vnsgn/huguesStack/pull/4) merged as
`76f13b791cbefd984a028cad2841ce867165d012`;
[PR #5](https://github.com/hugues-vnsgn/huguesStack/pull/5) merged as
`89e7125490a659a77381a3c12336abc56bb58dda`. The integrated tree
`280f42f14603f9e0b89b3a049ca8a3e831d43d88` equals tested and reviewed
head `cdc44dc`. All **119 framework tests** passed. Package checks, offline
upstream validation, shell syntax, strict plugin/marketplace validation and
whitespace checks passed. Claude Code `--model fable --effort high`, resolved
model `claude-fable-5-1`, returned CLEAN after three LOW integration findings
were fixed (two initial findings and one downgrade-bypass finding) and the full
checks repeated. PR #2 remains draft and unmerged; no release
was published.

## Observed host invocation

The existing private recipe loaded through Claude's native Skill tool in a fresh
project/local session. A separate direct plugin-generator invocation read the
actual repository and template and authored a complete private candidate.
Both exited 0. The generator probe used head `3d88839`, whose plugin bytes
were identical to integrated main `89e7125`; the private project recipe was
fingerprinted separately. These are **observed-pass invocation** and **authored candidate**
results. The candidate was not written into the consumer or executed through
its generated sections. A full generated-recipe cycle remains unrun.

Two earlier project-recipe probes returned unknown-skill under different
isolation settings. Retain them as failed probes; the successful session does
not erase those attempts or establish their root cause. See
[host loading](host-loading.md#wp3-claude-invocation-observations) for settings
and the read-only boundary. Codex's direct-read fallback remains observed;
native plugin installation/invocation remains unrun.

## Bounded Jev judgment

One explicitly approved Android version-1 scenario ran with the installed
Jev 1.3.0 CLI against the exact previously tested artifact. It drove a
three-checkpoint placeholder navigation journey and returned **PASS**,
`ALL_CHECKPOINTS_PASSED`: **3/3 checkpoints**, six label claims, claim probabilities
**0.98 to 0.99**, model `jev-1.13.0`. Fresh captures guarded the unique target and
bound the run to the installed artifact.

The owner approved transmission of each checkpoint's complete visible text,
identifiers, positions and state to TypeSafe for that run. The existing key was
loaded into that process only; screenshots and logs stayed local. CLI capture
`--jev` only formats local output. It is not an external judgment; the scenario
run and returned report supply that evidence.

This verdict covers the six label claims. Header geometry, accessibility,
selected return state and enlarged-text observations retain their separate
local tests and captures. Jev did not judge them. iOS judgment for the agreed WP3 consumer remains blocked:
Jev's bundled MobileBuildMCP driver conflicts with that consumer's XcodeBuildMCP-only
execution rule. The existing permitted iOS captures remain valid local evidence.

## Independent native domains

A separate existing Swift app and test bundle compiled through the permitted
native workflow with signing disabled on retry. **Zero tests executed**; no app
install or launch occurred. App-host startup would create default account/feed
state and refresh; additional authority is pending.

A separate existing native Kotlin app assembled its demo APK offline. Its test
build is blocked by three uncached pinned libraries: `kotlin-test 2.3.0`,
`androidx.test:rules 1.7.0-rc01` and `hilt-android-testing 2.59`. **Zero unit or UI
tests executed**; no APK install or app startup occurred. Dependency-download
authority is pending. Neither build establishes the plan's independent
native-feature bar.

The historical shared KMP/CMP task passed 12 Android JVM and eight iOS logic
tests, plus the bounded journey on Android and two iOS simulators with normal
and enlarged text. Those observations remain scoped to shared navigation and
the header. Narrow/enlarged iOS bottom-tab clipping remains outside that scope.

## Remaining acceptance

Run an applied generated recipe through Launch, Doctor, Drive, Evidence and
Cleanup on each authorized target, preserving failed attempts and reopening
artifacts after teardown. Resolve each independent native-domain prerequisite
before running its tests and driven path. Preserve repository tool requirements
for iOS judgment. Record each new result against its actual artifact and revision.
The four-domain personal-workflow bar and release readiness remain unestablished.
