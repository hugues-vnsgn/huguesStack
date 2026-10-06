---
name: create-verification-skill
description: "Create a project-local skill that builds, drives and records proof of one agreed mobile user journey."
disable-model-invocation: true
source: pstack/skills/create-verification-skill/SKILL.md
---

# Create a verification skill

source: Adapted from pstack 0.15.5 at `2eb7ed4613cfc8f098dfe464a23680ea44d84c5e`, `pstack/skills/create-verification-skill/SKILL.md`; input receipt and differences are recorded in this package's WP3 source receipts.

For an audit or repair of an existing bounded recipe, read [maintain-verification-skill](../maintain-verification-skill/SKILL.md) in full and hand off to its steps, preserving the existing journey and clean/changed/blocked outcomes. Use this generator for a new agreed recipe.

Write the next agent's executable verification recipe in the consumer repository. Keep consumer code, selectors, scripts and private evidence outside this plugin.

## Steps

1. Establish the consumer, agreed journey, expected behavior, writable paths and execution authority. Read its repository instructions, existing project skills and build configuration. Preserve existing tracked and untracked work; document the tested baseline and any carried diff. Read [mobile lanes](../hugues-mode/references/mobile-lanes.md) and select every affected domain. Finish with the exact scope, targets and permitted commands, or a named scope conflict.
2. Discover how to build, launch, health-check, drive and stop this app using its own documented tools. Inspect available host capabilities without installing, connecting credentials or changing system settings. Read [jev Drive](../hugues-mode/references/jev-drive.md) for mobile screens. Record each target's selected scheme/variant, tests, device, app identity and readiness signal. A configured MCP server is not proof that its tools are callable. Missing permitted tools block that check; choose another tool only when repository instructions and current authority allow it.
3. Choose the [project skill location](#project-skill-location), preserving existing files. Write `verify-<app>/SKILL.md` using the [project template](references/project-skill-template.md). Replace every template prompt with observed repo facts or a precise blocker. Include one bounded journey with its expected checkpoints, real selectors and per-target checks. Do not generate a feature map: that work remains deferred. Keep an unavailable build or runtime visibly blocked; report code repair through [build doctor](../hugues-mode/playbooks/build-doctor.md) within its own authority.
4. Validate frontmatter, local pointers and actual command/tool availability. In a fresh host session, confirm that the chosen project directory discovers the skill, or record direct Markdown reading as the fallback and native discovery as unrun. Creating a path alone proves no loader behavior. Run the generated Launch, Doctor, Drive and Evidence sections on each authorized target against the same recorded artifact. Inspect outputs rather than trusting a delegate summary; keep failed attempts and missing checks in the evidence.
5. Perform only the generated authorized cleanup. Independently reopen the durable evidence after teardown and confirm that logs, reports and screenshots still exist. Report authored or blocked sections separately from executed proof. Call the generated recipe observed only for the targets and journey actually driven; compilation, planning previews and an unexecuted recipe are not native proof.

## Project skill location

Honor the consumer repository's existing canonical skill layout first. Use the current host's repository loader directory: `.claude/skills/verify-<app>/SKILL.md` for Claude Code and `.agents/skills/verify-<app>/SKILL.md` for Codex. Resolve it from the consumer worktree root, not the plugin root or home directory. Read existing project conventions before choosing a slug; if several verification skills fit and intent is ambiguous, ask which to update.

For both hosts, keep one reviewed canonical body. If the repository supports a canonical directory and host symlinks, preserve that convention and create a symlink only within the assigned writable scope. Verify the link resolves inside the consumer worktree and confirm loader behavior in each host before claiming discovery. When that behavior is unavailable, record direct reading as the fallback and native discovery as unrun; do not silently replace the repository layout. If the repository instead requires regular-file copies, or has no supported shared layout, create copies only within scope, record the canonical path, compare body hashes and retain synchronization instructions in the generated skill. Preserve existing differences; report a conflict rather than overwriting them. Do not edit global host configuration or install the plugin to generate a local skill.

**Reply:** skill paths, exact tested revision and carried diff, journey/targets, loader result, proof outcomes, durable evidence path and missing capabilities. Keep consumer details local; publish only separately authorized sanitized summaries.
