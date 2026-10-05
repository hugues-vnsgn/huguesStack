# Authoring a skill

source: Adapted from pstack 0.15.9 at `e43c7ee26e0038c6c1fa8380dd34ce86ff94cb2a`, `pstack/skills/poteto-mode/playbooks/authoring-a-skill.md`; MIT notice in PSTACK-LICENSE.

Own the instructions and their completion criteria.

## Steps

1. Read the owner's available `writing-for-agents` skill, including its skill mechanics when editing SKILL.md. Establish the skill's trigger, branch behavior and observable finish criteria. If the skill is absent, record the gap and use explicit ordered steps with checkable bounds.
2. Brief a fresh implementation subagent with the owned paths and expected behavior. Keep reference behind pointers that name the trigger; retain only prose that changes a decision. A worker owns the authored diff directly and does not recursively delegate; each new revision round gets a fresh worker.
3. Validate skill name and description frontmatter, existing referenced files and cross-skill links with the repository's package checks. Named external skills must be marked as prerequisites with a missing-capability path rather than linked as if shipped.
4. Exercise structural behavior with representative prompts and regression cases. Keep subjective prose judgment separate from a behavioral pass; retain this step with a skip reason when no structural behavior changed.
5. Inspect the actual diff, apply the owner's available `unslop` skill after the structural pass, and obtain an independent fresh review. Resolve findings, rerun affected checks and run [opening a PR](opening-a-pr.md).

**Reply:** trigger and behavior, design decisions, validation evidence and missing capabilities.
