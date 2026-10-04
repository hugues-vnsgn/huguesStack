# WP2 validation

WP2 supplies the routing skill, fourteen playbooks, a worker definition,
`interrogate` guidance and the 24 pstack principles. The product is Markdown
consumed by the host. There is no routing runtime or execution harness.

## Static contracts

Run `./scripts/check-plugin.sh` and `python3 -m unittest discover -s tests -v`.
At head `17ba517058e1f56b0ead6a53587cda375312bc45`, for `0.1.0-dev.2` on
4 October 2026, all 54 stdlib tests passed: 27 existing
package regressions and 27 WP2 tests. The package checker passed for 26 skills
and reported one explicit `DEFERRED` upstream benchmark-helper pointer, with
its source bytes and provenance verified. Shell syntax, whitespace and strict
Claude plugin and marketplace metadata validators also passed. Metadata
acceptance does not establish Claude model behavior.

After the six accepted Claude findings were corrected, all 71 tests passed on
the working tree: 27 existing package regressions and 44 WP2 tests, including
17 new regressions. The package checker passed for 26 skills with the same
explicit deferred link. The final tested commit is recorded in
[PR #3](https://github.com/hugues-vnsgn/huguesStack/pull/3). WP2 tests check:

- The exact fourteen-playbook set, valid route links and nonempty numbered steps.
- Literal acceptance cases with expected routes, plus the four mobile lane cases.
- All 24 principle bytes against pinned upstream SHA-256 values, provenance
  entries and complete inline index coverage.
- Adapted source mappings and the worker's bounded delegation contract.
- Intent precedence before implementation lanes, absolute mode and skills paths
  for each host and wrapper, direct reads for disabled skills, human consumer
  authority, prototype production routing and host-specific recovery commands.
- All 28 verbatim destination hashes, including independent hash expectations
  and mutation coverage for the four review references.
- Proof rules for skipped, flaky and wrong-target results, target coverage and
  consumer authority.

Mutation tests begin with a valid package and remove or alter one contract at a
time. Their diagnostics establish that the static checker detects those changes.
These tests check authored instructions. They cannot establish that a model
selects a route, follows a todo list or obeys the authority boundary. Separately,
all 41 upstream source receipts were independently verified against the pin;
28 imported files, including the 24 principles, remain byte-for-byte copies.

## Routing acceptance

The fixture [wp2-routing-prompts.json](../tests/fixtures/wp2-routing-prompts.json)
initially contained six literal cases independent of the router's implementation:

| Request | Expected route | Domain |
|---|---|---|
| Article list jumps when the unread badge updates | bug-fix | Swift/iOS |
| Add mark older as read to the topic screen | feature | Kotlin/Android |
| Discount boundary is wrong in shared code | kmp-bridge-change | KMP shared logic |
| Review a diff from the other host | interrogate | Review; derive domains from the diff |
| Refactor duplicated Swift article formatting | refactoring | Swift/iOS |
| Prototype a shared Compose reading panel | prototype | CMP shared UI |

Five additional literal cases cover the review findings:

| Request | Expected route | Domain |
|---|---|---|
| Pause the KMP discount fix before compaction | pause-safely | KMP shared logic |
| Resume the iOS badge bug fix from a handoff | session-pickup | Swift/iOS |
| Explain the iOS list jump; change nothing | investigation | Swift/iOS |
| Open a PR for a shared Compose panel change | opening-a-pr | CMP shared UI |
| Verify the existing KMP fix and native callers; no code changes | mobile-proof | KMP shared logic |

In a fresh host session, invoke `hugues-mode` with each case in **route preview**
mode. Require the host to read the selected file, copy its numbered steps into
its todo list, name the domain and required proof, then stop. If no todo tool is
available, require the displayed checklist fallback and disclose that limitation.
Review the actual reply against the literal expected values. Record a mismatch as observed-fail;
a static fixture passing is not a substitute. No consumer repository is needed
for this planning-only check.

At head `17ba517`, the coordinator observed a fresh Codex 0.160.0 manual
project-skill preview on 4 October 2026, exit 0. All six expected routes and domains matched. All 38
numbered playbook steps matched the selected files byte-for-byte: 6 bug-fix,
8 feature, 5 KMP, 5 interrogate, 8 refactoring and 6 prototype steps. The session
made eight read-only `cat` commands for skill files and ran no delegates or
consumer commands. Codex exposed no native todo/plan tool, so it returned the
displayed JSON checklist fallback.
This is **observed-pass for manual route preview and checklist fallback**;
native todo integration was unrun. The coordinator checked the final JSON
against the fixture and selected playbooks, and inspected the tool events.
Plugin bytes matched the recorded smoke-run hashes. Raw replies, argv, host
version and plugin fingerprints are retained outside the public repository.

After the six review fixes, a fresh Codex 0.160.0 manual project-skill preview
on 4 October 2026 exited 0. All eleven expected routes and domains matched,
including the five new precedence cases. Review domain remained unresolved
without a supplied diff. All 61 numbered steps matched the current selected
files byte-for-byte: the original 38, plus 4 pause, 5 resume, 4 investigation,
5 PR-preparation and 5 mobile-proof steps. All thirteen read-only skill-file
reads succeeded. The coordinator checked the literal routes, selected-file
steps, domain and proof requirements, and tool events; all 48 plugin file
fingerprints matched the preview. No delegates, writes or consumer commands
ran. This is **observed-pass for eleven-case manual route preview and displayed
checklist fallback**. The host exposed no native todo/plan tool; that integration
remains unrun. The final tested head is recorded in
[PR #3](https://github.com/hugues-vnsgn/huguesStack/pull/3).

The owner subsequently authorized Claude Code review. The static review of
head `17ba517` found six issues in routing precedence, handoff paths, authority,
verbatim reference coverage, prototype handoff and recovery commands. The
[review audit](reviews/wp2-claude-review.md) records the findings and follow-up.
The expanded precedence fixtures have the manual preview evidence above.
Claude routing remains unrun; code review alone does not
verify routing or worker execution. A future real task is needed to establish fresh delegate execution
and multi-turn mode persistence, both unrun here. Native build, test and UI
outcomes remain WP3 and WP4 work requiring authorization to operate on the
consumer repository.

## Limits and deferred work

Authored proof lanes cover Swift/iOS, Kotlin/Android, KMP and CMP. No mobile app
has been run or changed by WP2. Native Codex installation and invocation remain
unverified. The completed Claude Code review supplies a separate model
assessment of the public code; it supplies no observed plugin routing, native
worker execution or mobile proof.

Consumer feature maps and the CLI-first verification addition stay deferred
until after the first release. Current native, target-test and UI requirements
still apply. The full upstream inventory, weekly sync, model setup and remaining
leaf skills belong to later work packages.
