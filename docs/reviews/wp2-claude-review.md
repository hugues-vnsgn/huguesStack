# WP2 Claude Code review audit

The owner authorized the implementation → Claude Code review → adjudicated
fixes → tests → re-review workflow through first-release readiness. PR #2 and
[PR #3](https://github.com/hugues-vnsgn/huguesStack/pull/3) remain unmerged pending
authorization. Release publishing and consumer selection, edits or execution
require separate authorization.

## Initial review

On 4 October 2026, Claude Code 2.1.286 with `claude-opus-5-5` reviewed head
`17ba517058e1f56b0ead6a53587cda375312bc45` against base
`7f58e929958cec14a9ee86db6a41b5a30feeee26`. The read-only public-code snapshot
exposed Read, Glob and Grep in plan permission mode. The invocation exited 0;
30 tool calls completed with no errors. No Bash, edits, consumer access or
permission bypass was used. The report returned `material-findings`.

The coordinator independently evaluated and accepted these six findings:

| Finding | Accepted issue | Corrective change |
|---|---|---|
| WP2-R1 | Domain routes could override explicit pause, resume, PR preparation or explanation intent | Put explicit intent before implementation lanes; add precedence cases |
| WP2-R2 | Claude and common worker handoffs lacked resolvable plugin paths | Require absolute mode and skills-directory paths for each host and wrapper |
| WP2-R3 | Workspace rules could be read as granting consumer or publication authority | Make rules constraints; require explicit owner/user authority for those actions |
| WP2-R4 | Four verbatim review references lacked ongoing byte checks | Check every verbatim receipt against destination bytes; add a mutation regression |
| WP2-R5 | Prototype production handoff always selected the native feature route | Select the matching native, KMP or CMP production route |
| WP2-R6 | Mode recovery gave a bare slash command for both hosts | Document the namespaced Claude and Codex invocation forms |

The corrective working tree passed all 71 stdlib tests: the original 54 plus
17 regression tests for the accepted findings. The package checker accepted
26 skills with the same explicit deferred benchmark link. A fresh Codex
0.160.0 manual preview exited 0: all eleven expected routes and domains matched,
all 61 numbered steps matched the current selected files byte-for-byte, and
thirteen read-only skill-file reads succeeded. All 48 plugin file fingerprints
matched that preview. No delegates, writes or consumer commands ran. The host
exposed no todo/plan tool, so only its displayed checklist fallback was observed.

The initial head required corrections. The final tested head, verification
results and exact-head Claude re-review verdict are recorded in
[PR #3](https://github.com/hugues-vnsgn/huguesStack/pull/3). Raw evidence and the
commit-bound audit are retained outside the public repository. This file records
the initial review and the corrective scope; it does not substitute for that
final review evidence.

## Review limits

Claude performed static code review and ran no tests, package checker or host
validator. It did not invoke plugin routing, run a native worker, test mode
persistence or operate a mobile app. The original six-case Codex preview and 54
passing tests are separately recorded in [WP2 validation](../wp2-validation.md).
The expanded eleven-case preview verifies planning behavior through the manual
Codex project-skill path. Native todo integration remains unverified.

Optional broader routing coverage and standalone agent-frontmatter linting are
deferred. Consumer feature maps and CLI-first enhancements remain deferred until
after first release.
