# WP2 validation

WP2 supplies the routing skill, fourteen playbooks, a worker definition,
`interrogate` guidance and the 24 pstack principles. The product is Markdown
consumed by the host. There is no routing runtime or execution harness.

## Static contracts

Run `./scripts/check-plugin.sh` and `python3 -m unittest discover -s tests -v`.
For `0.1.0-dev.2` on 4 October 2026, all 54 stdlib tests passed: 27 existing
package regressions and 27 WP2 tests. The package checker passed for 26 skills
and reported one explicit `DEFERRED` upstream benchmark-helper pointer, with
its source bytes and provenance verified. Shell syntax, whitespace and strict
Claude plugin and marketplace metadata validators also passed. Metadata
acceptance does not establish Claude model behavior. WP2 tests check:

- The exact fourteen-playbook set, valid route links and nonempty numbered steps.
- Literal acceptance cases with expected routes, plus the four mobile lane cases.
- All 24 principle bytes against pinned upstream SHA-256 values, provenance
  entries and complete inline index coverage.
- Adapted source mappings and the worker's bounded delegation contract.
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
contains six literal cases independent of the router's implementation:

| Request | Expected route | Domain |
|---|---|---|
| Article list jumps when the unread badge updates | bug-fix | Swift/iOS |
| Add mark older as read to the topic screen | feature | Kotlin/Android |
| Discount boundary is wrong in shared code | kmp-bridge-change | KMP shared logic |
| Review a diff from the other host | interrogate | Review; derive domains from the diff |
| Refactor duplicated Swift article formatting | refactoring | Swift/iOS |
| Prototype a shared Compose reading panel | prototype | CMP shared UI |

In a fresh host session, invoke `hugues-mode` with each case in **route preview**
mode. Require the host to read the selected file, copy its numbered steps into
its todo list, name the domain and required proof, then stop. If no todo tool is
available, require the displayed checklist fallback and disclose that limitation.
Review the actual reply against the literal expected values. Record a mismatch as observed-fail;
a static fixture passing is not a substitute. No consumer repository is needed
for this planning-only check.

The coordinator observed a fresh Codex 0.160.0 manual project-skill preview on
4 October 2026, exit 0. All six expected routes and domains matched. All 38
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

Claude routing is unrun; no external Claude invocation is authorized for this
work package. A future real task is needed to establish fresh delegate execution
and multi-turn mode persistence, both unrun here. Native build, test and UI
outcomes remain WP3 and WP4 work requiring authorization to operate on the
consumer repository.

## Limits and deferred work

Authored proof lanes cover Swift/iOS, Kotlin/Android, KMP and CMP. No mobile app
has been run or changed by WP2. Native Codex installation and invocation remain
unverified. Same-host review supplies process independence; cross-host review
must actually use the other host before claiming model independence.

Consumer feature maps and the CLI-first verification addition stay deferred
until after the first release. Current native, target-test and UI requirements
still apply. The full upstream inventory, weekly sync, model setup and remaining
leaf skills belong to later work packages.
