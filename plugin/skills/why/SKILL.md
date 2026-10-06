---
name: why
description: "Investigate historical rationale with cited evidence and calibrated confidence."
disable-model-invocation: true
source: pstack/skills/why/SKILL.md
source-revision: e43c7ee26e0038c6c1fa8380dd34ce86ff94cb2a
source-lines: "1-158"
---

# Why

Investigate the forces that shaped code. Use [how](../how/SKILL.md) for runtime mechanics; read its Markdown directly when needed. Treat the user's hypothesis as a candidate to test. Read [epistemics](references/epistemics.md) in full before investigation and require the synthesizer to follow it.

## Steps

1. **Understand target and question.** Identify the code, pattern, feature or decision and the rationale, tradeoff, edge case, constraint or history being asked about. For a vague target, state the best interpretation from the conversation and continue discovery. Record the consumer, relevant mobile domain, exact source target and current authority.
2. **Establish a code anchor.** Read the relevant files and record paths, line ranges, symbols, recent commits, PR numbers extracted from commit messages and linked ticket IDs. Use the safe history templates below when local git history is available. Verify `gh` availability and authorized read access before fetching substantive PR bodies, comments and reviews. Record missing history, CLI or access as gaps. Complete the seed context before spawning investigators.
3. **Discover and investigate in parallel.** Build a coverage map for all seven categories below from tools actually available to this host. Inspect their current schemas and access; tool discovery alone does not establish searchable data. Launch fresh investigators concurrently for available sources using the roster and source contracts below. Collect their exact queries, findings, null results, inaccessible records and cross-source leads. Include written reasons for every skipped category.
4. **Synthesize.** Once all investigators return, spawn one fresh synthesizer with [synthesizer prompt](references/synthesizer-prompt.md), every report including null results, skipped categories and reasons, the code anchor, original question and complete [epistemics framework](references/epistemics.md). Give it the same authorized read tools needed to spot-check citations. Complete when claims are calibrated, citations checked and contradictions and gaps retained.
5. **Present.** Lightly edit for clarity or conversation context; preserve the confidence language. Return the output sections below and one Sources Consulted entry for every category, including unavailable, empty or skipped sources with reasons. When the question precedes a code change, append Preserve / Change / Avoid / Risk constraints derived from the lineage; these constraints authorize no implementation.

## Code anchor templates

Substitute verified values, quote paths and search text safely, and read history without changing the checkout:

```bash
# Last-touch commits for target lines
git blame -L <start>,<end> -- <file>
# File history and patches through renames
git log --follow -p -- <file>
# Recent commits; merge subjects may contain (#1234)
git log --oneline -20 -- <file>
# Extract PR numbers and linked tickets from the message
git log -1 --format=%B <commit>
# Only if gh is available and authorized for this repository
gh pr view <number> --json title,body,author,createdAt,mergedAt,labels,closingIssuesReferences,comments,reviews
```

Pass this seed context to every investigator. Read [code archaeology](references/sources/code-archaeology.md) for pickaxe, co-change, comments, tests and older origins. Read test source as evidence; execute tests only under explicit current consumer authority.

## Coverage map and investigator roster

Default to the full parallel investigation. Discover through the host's available-tools map or actual tool-discovery interface; inspect exposed metadata and schemas. Use MCP resources only when that server actually exposes them. Classify by primary evidence, record ambiguous classifications, and retain all seven rows even when unavailable:

| Category | Evidence to seek | Category reference |
|---|---|---|
| Source control history | Implementation-time rationale in commits, PRs, comments and tests | [code archaeology](references/sources/code-archaeology.md) |
| Issue / ticket tracker | Product and business forcing functions | [ticket example](references/sources/linear.md) |
| Long-form documents | Design rationale, specs, ADRs and meeting notes | [document example](references/sources/notion.md) |
| Real-time team chat | Deliberation that never reached a document | [chat example](references/sources/slack.md) |
| Infrastructure observability | Runtime constraints, incidents, logs, monitors and traces | [observability example](references/sources/datadog.md) |
| Error / exception tracking | Exceptions and trajectories motivating defensive code | [error example](references/sources/sentry.md) |
| Product analytics warehouse | Product data, experiments and numeric thresholds | [warehouse example](references/sources/databricks.md) |

Always assign a source-control investigator when repository history or an authorized source-control read tool is available. Verify local git and history; verify `gh` separately. If neither history nor a source-control read tool is accessible, report source control unavailable rather than fabricating the guaranteed source. Each investigator owns one actual tool or MCP; the source-control assignment may include local git, in-repo evidence and verified `gh` as its archaeology reference describes. Keep investigators separate when multiple tools or MCPs cover a category, and consolidate their reports into that category's final coverage entry.

Each investigator gets [investigator prompt](references/investigator-prompt.md), its single category reference, the code anchor and original question. Read [source playbook index](references/source-playbook.md) to adapt example queries to actual schemas. If target code is defensive (null guards, retry, timeout, rate limits, flags, egress or OOM guards), also append [incident/postmortem angle](references/sources/incident-postmortem.md). Investigators search their own source and return cross-source links as leads for the matching investigator or a fresh follow-up pass.

Skip only for unavailable access or a provably irrelevant category; write the reason in Sources Consulted. A missing tool, inaccessible data, retention gap and a searched empty result are distinct outcomes. A single-commit trivial target may be answered inline only after checking the coverage map and confirming every available category search would be redundant because the PR already contains the complete answer. State that justification explicitly. Thin evidence alone does not justify the shortcut.

## Host and authority

Read [host notes](../hugues-mode/references/host-notes.md) before delegation and use the actual Claude Code Agent or Codex native subagent adapter. Supply the resolved absolute [mode](../hugues-mode/SKILL.md) path, absolute plugin skills directory, consumer, target, role template, domain, proof surface, allowed source and current authority. Require direct assigned work. Default research roles to `inherit-parent`, omitting model overrides. Use an explicit owner-selected model only if accepted by the actual schema; disclose rejection instead of guessing a replacement.

Declare investigator and synthesizer assignments read-only while preserving authorized MCP read access. Use the current native schema rather than assuming Task, Ask or a `readonly` field. If a host mode removes needed MCPs, choose a supported native configuration that retains those read tools and bind it to no writes in the prompt. Report missing subagents or prohibited delegation and return bounded findings without claiming the full delegated workflow ran.

Read code, history and existing artifacts within current authority. Tool examples are templates for available services, not required integrations or proof of access. Consumer edits, messaging, installs and publication are outside scope. Run available read-only source queries, including schema inspection and SQL retrieval, within the current research request and authorized source access. Inspect actual tool effects. Tests, apps, builds, devices, service writes/setup or new private-data transmission outside that research scope require explicit current human authority. Apply that boundary to tools that launch new AI analyses. Prepare queries and report gaps only when actual authority or capability excludes them. Spot-verification follows the same limits. Source review does not execute the app or establish observed runtime behavior.

## Output and epistemics

Use [synthesizer output](references/synthesizer-prompt.md): The Question, The Code in Question, What We Found, What We Can Reasonably Infer, Competing Hypotheses, What We Don't Know, Sources Consulted and Confidence Summary. Drop inapplicable inference or hypothesis sections while retaining evidence/confidence separation and concrete gaps. Keep Direct, Supported, Inferred, Speculative and Unknown distinct. Cite actual sources; code behavior alone establishes no author intent. Preserve conflicting evidence and avoid recency bias by tracing earlier decisions. Never turn an unavailable source or empty search into an invented rationale.
