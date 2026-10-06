# pstack upstream delta

Source: https://github.com/cursor/plugins

From: 0.15.5 `2eb7ed4613cfc8f098dfe464a23680ea44d84c5e`
To: 0.15.9 `e43c7ee26e0038c6c1fa8380dd34ce86ff94cb2a`

3 added / 18 changed / 0 removed.

Dispositions are decisions about scope; they do not establish implementation or observed support.
Pending rows require review before re-pinning. Read adapted playbook diffs; never overwrite the fork.

| Path | Change | Previous blob / mode | Current blob / mode | Disposition | Reason |
|---|---|---|---|---|---|
| pstack/.cursor-plugin/plugin.json | changed | 6ebc34b96f65088d695e3c3038eb412d750c8bdb / 100644 | 0ab7fa1b6a2bbcbb1a25e797e74be5ee63370bed / 100644 | port with adaptation | Adapt packaging and documentation for Claude Code and Codex; retain development and support limits. |
| pstack/README.md | changed | b7cdef8aeb15da88a8f9cdd82904d884552395b7 / 100644 | cf64d3602995ddf54f06fb8bf27e3520850d21f2 / 100644 | port with adaptation | Adapt packaging and documentation for Claude Code and Codex; retain development and support limits. |
| pstack/agents/poteto-agent.md | changed | 91d53b85918f842c703758e66352b956ee80feb7 / 100644 | f9d79a75560520cbb2f939c587ce00fa7e33037a / 100644 | port with adaptation | Use the fresh-per-task worker with revision-bound authority and host-native handoff. |
| pstack/docs/guide/08-principles.md | changed | be1102d678a9748b396f829e29fb3dfdd60ba205 / 100644 | 283a5e66b99917c12ca88f8c3e3e70ad69342062 / 100644 | ignore with reason | Deferred beyond the Layer 1 release by the revised public plan; responsibility remains accounted for. |
| pstack/docs/guide/README.md | changed | b8b1b079456d6f2b2c536937d21180ba5c21f733 / 100644 | 564eee1d5b43729d57caca4fddcef45d3dffdef5 / 100644 | ignore with reason | Deferred beyond the Layer 1 release by the revised public plan; responsibility remains accounted for. |
| pstack/skills/architect/SKILL.md | changed | afa6eead878d2a7b8d22b8eb99e6cf0c6ee0ad69 / 100644 | 2bd58a7d46f1899f107f3c502f6ddcfbd6717f99 / 100644 | port with adaptation | Retain pstack design workflow with native same-host runners, mobile contracts and explicit authority; see retained-design-provenance.json. |
| pstack/skills/architect/references/design-red-flags.md | changed | 32cb24083f308fd67ab4c431b44e1d7d3563435a / 100644 | f8503c9595b289c607ff5088f82b21197edf94ec / 100644 | port verbatim | Retain byte-verbatim design reference from pstack 0.15.9. |
| pstack/skills/benchmark-checklist/SKILL.md | added | — | c02adb78929d0c1218fba554a31c423d65deb24d / 100644 | ignore with reason | Deferred beyond the Layer 1 release by the revised public plan; responsibility remains accounted for. |
| pstack/skills/correct/SKILL.md | added | — | c09f486e32935a154dd98daa13aa8187856600fe / 100644 | port with adaptation | Adapt pstack 0.15.9 correct for mobile, direct host reading and current authority; retained contracts and deviations are recorded in retained-verification-provenance.json. |
| pstack/skills/poteto-mode/SKILL.md | changed | f8ddcae379007d61aefcae39b18bd836a488ee21 / 100644 | 90bfebeecd3b8344eee39d08803a3e2a0f09e3c9 / 100644 | port with adaptation | Read upstream routing changes and adapt fresh-worker, benchmark and reply contracts to the mobile mode. |
| pstack/skills/poteto-mode/playbooks/autopilot-full.md | changed | e92be88a8dfcb0a1f2745e0da7af42d31f1d6606 / 100644 | d5a68c339e25ac016ffad9c51d858f0f6c37937a / 100644 | ignore with reason | Only the ten selected upstream playbooks ship in Layer 1; performance and managed/automatic workflows remain deferred. |
| pstack/skills/poteto-mode/playbooks/autopilot-stack.md | changed | 810a70fff72ae49a9387b5ea41dcb13f890c83c0 / 100644 | 750a7547235ae8eb340285684b9be7c36dff323a / 100644 | ignore with reason | Only the ten selected upstream playbooks ship in Layer 1; performance and managed/automatic workflows remain deferred. |
| pstack/skills/poteto-mode/playbooks/hillclimb.md | changed | 582555e826675068ceaea08e6134a44ba0ea4511 / 100644 | c6441b92d30a71489d88eae5bfa8dc457da55cb1 / 100644 | ignore with reason | Only the ten selected upstream playbooks ship in Layer 1; performance and managed/automatic workflows remain deferred. |
| pstack/skills/poteto-mode/playbooks/multi-phase-plan.md | changed | fe006110f6005dcdb746d891e7901a1734a75538 / 100644 | f8ed78a6533cc5d738d3a3ec106bf2577d3f98ca / 100644 | ignore with reason | Only the ten selected upstream playbooks ship in Layer 1; performance and managed/automatic workflows remain deferred. |
| pstack/skills/poteto-mode/playbooks/opening-a-pr.md | changed | 626f376bd64e2e7b04c2575cb8b8f4ba70a6078d / 100644 | 4e25989729174580e48ce36e265f298231c6de7f / 100644 | port with adaptation | Read the upstream playbook diff and preserve user adaptations, mobile proof and separately authorized publication. |
| pstack/skills/poteto-mode/playbooks/perf-issue.md | changed | 688d483d4d4a6c58efa515558c822e11f621540f / 100644 | 405c7a4362bedbd4194a5ef234553adf0dff78c9 / 100644 | ignore with reason | Only the ten selected upstream playbooks ship in Layer 1; performance and managed/automatic workflows remain deferred. |
| pstack/skills/poteto-mode/scripts/check-plan.mjs | changed | 6c07f4e903d10332702a2ac4602ada9273e71609 / 100755 | d242f28eb801e781ccc2f2ba93b700b263a77816 / 100755 | ignore with reason | Layer 2 helper tooling is deferred; check-plan is reconsidered only if multi-phase-plan ships. No upstream script is executed. |
| pstack/skills/principle-explain-the-number/SKILL.md | added | — | 9c22351d1fbe1ffcf277e61aef9fdb7816306fa7 / 100644 | port verbatim | Keep the principle byte-for-byte with upstream MIT attribution; provenance lives in source receipts. |
| pstack/skills/swarm/SKILL.md | changed | a63e09eda94558aa8c7ae6d0653951838a3abd3f / 100644 | db22b8787966abc61216052d9f3142018404cab8 / 100644 | ignore with reason | Owner approval on 6 October 2026 defers this family to 0.2; preserve private owner originals and ship no files in this retained-eight package. |
| pstack/skills/technical-writing/SKILL.md | changed | 1cd44cf2595a5caeda1f702aacd4f8a25aa8166a / 100644 | 5eef4fc494a059eb740cb621dadb4a7a81af23e4 / 100644 | ignore with reason | Deferred beyond the Layer 1 release by the revised public plan; responsibility remains accounted for. |
| pstack/skills/typescript-best-practices/references/patterns.md | changed | f44d22ffe9130c5340d55a2fa57028c6959479cb / 100644 | c21d876b71b9c7afa897f2f6d982ead07db8f104 / 100644 | ignore with reason | This service/TypeScript responsibility is outside the selected mobile release scope; no duplicate or automatic integration is shipped. |
