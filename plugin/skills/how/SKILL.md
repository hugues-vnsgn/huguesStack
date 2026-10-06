---
name: how
description: "Explain subsystem architecture, runtime flow, and code ownership."
disable-model-invocation: true
source: pstack/skills/how/SKILL.md
source-revision: e43c7ee26e0038c6c1fa8380dd34ce86ff94cb2a
source-lines: "1-58"
---

# How

Explain how code works at the level a senior engineer needs to start working in the subsystem. Use [why](../why/SKILL.md) for historical motivation; read that Markdown directly when needed.

## Steps

1. **Assess complexity.** State an interpretation when scope is ambiguous and continue source discovery. Classify a single module, small utility or narrow function question as simple; use step 2b. Classify a subsystem spanning files or services, a cross-cutting feature or an architectural overview as complex; use step 2a. When uncertain, choose simple. Record the consumer, mobile domain when relevant, exact source target and current authority before handing off.
2. **Explore or explain.** Follow the selected branch below. Complete it when the assigned findings or explanation have returned, including files read and unresolved gaps.
3. **Synthesize complex findings.** Once every explorer returns, spawn one fresh explainer using [explainer prompt](references/explainer-prompt.md), with the original question and every explorer's findings. Require it to reconcile overlap, check contradictions against source and disclose unresolved gaps. Skip this step for simple questions.
4. **Present.** Return the explainer's output with light edits for clarity or conversation context. Preserve its substantive explanation. Include the source paths and remaining gaps; label source-derived flow separately from observed runtime behavior.

## Step 2a. Explore complex questions

Choose 2 to 4 distinct exploration angles. Launch all fresh explorers concurrently through the available native subagent tool, using [explorer prompt](references/explorer-prompt.md) with the question and assigned angle filled in. Each owns its slice, returns exact source locations and lists files read. Continue to step 3 after all have returned.

## Step 2b. Direct explain simple questions

Spawn one fresh explainer with [explainer prompt](references/explainer-prompt.md), the question and the single-pass instruction to explore and explain. Omit the Explorer Findings section. Spawn zero explorers and continue directly to step 4 when the explanation returns.

## Host and authority

Before spawning, read [host notes](../hugues-mode/references/host-notes.md) and use its actual Claude Code Agent or Codex native subagent adapter. Supply the resolved absolute [mode](../hugues-mode/SKILL.md) path, absolute plugin skills directory, consumer, source target, question, role template, domain, proof surface and current authority. Require workers to perform their assignment directly. Default every research role to `inherit-parent` by omitting model overrides. Apply an explicit owner-selected model only when the actual tool accepts it; disclose rejection instead of guessing a replacement slug.

Declare every research assignment read-only. Use only fields exposed by the current host schema; a prompt's read-only scope remains binding when the tool has no corresponding field. Preserve access to available read-only tools. Missing native subagents or a current delegation prohibition blocks the delegated workflow: report the gap and return bounded source findings without claiming explorer or explainer runs.

Read consumer source and existing artifacts within current authority. Source review does not execute the app or prove a runtime observation. Run authorized read-only source queries within the current research request. Running tests, apps, builds or devices requires explicit current human authority for that consumer. Consumer edits, external messages, installs and publication are outside this research assignment.

## Output format

Use the explainer template's applicable sections: Overview, Key Concepts, How It Works, Where Things Live and Gotchas. Include a diagram when it clarifies a multi-component flow; omit sections that add no information.
