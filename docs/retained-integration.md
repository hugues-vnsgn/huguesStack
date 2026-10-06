# Retained tools and RC2 integration

`0.1.0-rc.2` combines the eight owner-approved retained tools with the existing
mobile mode. This is a separate unmerged proposal based on main
`94560c43bd4a5a062177870188f60a7ebafb5028`. PR #8's RC1 and draft PR #2's
deferred feature maps/CLI-first changes remain separate. No merge, tag or release
is established. Target remains 9 October 2026, end of day GMT+7.

## Reviewed package inputs

The following completed package checks and independent Astra High reviews were
observed before this integration. Each package's seven exact-head checks passed.
These verdicts cover those heads, not the later integration commit.

| Package | Reviewed head | Public draft and receipt |
|---|---|---|
| Foundation | `3af59a9c78e710ac51b0a886e4abf9d79c4b2af3` | [PR #9](https://github.com/hugues-vnsgn/huguesStack/pull/9); shared retained-source accounting |
| Research | `615edc7b40336acc60adfb82d3f41a34d8119919` | [PR #10](https://github.com/hugues-vnsgn/huguesStack/pull/10); [research receipt](upstream/retained-research-provenance.json), [contracts](retained-research.md) |
| Design | `f4026d5e4f15df7666a47876aa06d7cc18da266d` | [PR #11](https://github.com/hugues-vnsgn/huguesStack/pull/11); [design receipt](upstream/retained-design-provenance.json), [contracts](retained-design.md) |
| Verification | `f126656d2718084de8292cda0cb40b81333e4d6e` | [PR #12](https://github.com/hugues-vnsgn/huguesStack/pull/12); [verification receipt](upstream/retained-verification-provenance.json), [contracts](retained-verification.md) |

The reviewed verification tree is `dc9920b430d37d2d368492831f2345d45e639ec9`.
It passed 152 framework tests and all seven checks before integration. The
combined package contains 35 skills, 14 playbooks and one worker, across 79 plugin
files. The eight leaves and their 25 source-accounted files retain their reviewed
bytes. All 24 principles remain verbatim at the unchanged pstack 0.15.9 pin
`e43c7ee26e0038c6c1fa8380dd34ce86ff94cb2a`.

## Existing playbook handoffs

Read each linked tool in full from the package before using it. Their disabled
model invocation means a direct file read, not a Skill-tool call. Keep the
[host adapter](../plugin/skills/hugues-mode/references/host-notes.md), scoped
worker role and current consumer authority throughout.

| Existing route | Handoff |
|---|---|
| [investigation](../plugin/skills/hugues-mode/playbooks/investigation.md) | `how` for mechanics; `why` for rationale and regression history; read-only findings and confidence |
| [bug-fix](../plugin/skills/hugues-mode/playbooks/bug-fix.md) | `how`/`why`, design-only `architect` when a function boundary changes, fresh test-only worker and independently observed cheap `tdd` RED before the separate production worker, preserved RED and same-check GREEN afterward; original runtime path still required |
| [feature](../plugin/skills/hugues-mode/playbooks/feature.md) | `how`, design-only `architect` with arena's two distinct sketches and verified synthesis; `arena` for warranted competing implementations |
| [prototype](../plugin/skills/hugues-mode/playbooks/prototype.md) | Design tools for an actual structural decision or competing executable experiment, within throwaway scratch scope |
| [refactoring](../plugin/skills/hugues-mode/playbooks/refactoring.md) | `how`, characterization first, design-only `architect` across boundaries and `blast-radius` for wide/shared-API changes |
| [authoring-a-skill](../plugin/skills/hugues-mode/playbooks/authoring-a-skill.md) | New bounded recipe uses `create-verification-skill`; existing recipe hands off to coordinator-owned `maintain-verification-skill` before generic worker briefing; recurring classes hand off to `correct` |
| [opening-a-pr](../plugin/skills/hugues-mode/playbooks/opening-a-pr.md) and direct review | `blast-radius` for big/wide diffs, retaining falsifiable safety checks and unrun facts within actual check authority |
| [kmp-bridge-change](../plugin/skills/hugues-mode/playbooks/kmp-bridge-change.md) / [cmp-two-target-change](../plugin/skills/hugues-mode/playbooks/cmp-two-target-change.md) | Cheap bug RED before the production worker; design and wide-change tools retain both targets' proof obligations |

Maintenance covers the existing agreed journey, every named checkpoint and every
required target. Its source readers remain read-only; the coordinator owns one
live mobile session at a time and re-proves owned harness repairs. Clean and
blocked outcomes produce no PR; changed permits at most one bounded authorized
correction. A missing live pass is blocked. The generic authoring route ends at
this handoff. `correct` requires repeated real evidence per class and proves
chosen enforcement against a real past mistake. A scoped implementation worker
performs its assignment directly; these links do not authorize recursive workflow
delegation.

All fourteen routes plus `interrogate`, routing precedence and numbered checklist
counts remain intact. Optional owner writing/unslop and mobile specialty skills
retain explicit absence reporting. The 6 October approval defers only `swarm`,
`show-me-your-work` and `setup-huguesstack` to 0.2; existing feature-map, CLI-first,
Layer 2 and other deferred scope remains in the [plan](PLAN.md).

## Static checks and observed-proof boundary

The integration regressions use manifest-driven discovery, actual numbered-step
links, pre-worker RED ordering, maintenance handoff and deferred-scope accounting.
Mutations remove or move those inputs; real package checking rejects missing
shipped targets. This tests Markdown/package contracts, not LLM adherence or
native execution. Run the existing unittest, package, upstream, strict Claude
plugin/marketplace, shell syntax and whitespace checks. Record their exact
integration head/tree, raw-log hashes and independent final-head review in the
separate RC2 draft record before publication; no future SHA or verdict is assumed.

The [RC1 receipt](rc-validation.md) retains 54 fingerprints bound only to the
plugin bytes at `21a82942019292f7212ff1185e9ef187ac96e86d`. Its two-host
16-case/87-step previews and bounded scratch delegation are historical. RC2's
changed mode/playbooks, metadata and 79 plugin files have no fresh host probe.
Native loading, eight-workflow adherence and mobile execution remain unrun for
this integration. Native todo behavior, four-domain feature completeness,
Swift/Kotlin red-green paths, full mode/persistence and the clean generated-recipe
cycle remain incomplete. Historical failures, native results and target limits
remain in [support](support.md) and the [evidence index](evidence-index.md).
