# RC validation receipt

Recorded **6 October 2026** for **`0.1.0-rc.1`**. This receipt covers read-only
host previews and bounded synthetic scratch delegation/artifact behavior. It does not establish
first-release readiness. Record final-head checks and independent **GPT-6 Astra
High** review in the RC PR before publication/acceptance. This receipt records
the initial check head and tested plugin fingerprints.

## Candidate binding

The initial RC commit `5af676e7486291fbfac1fb81263c2aecec629476` passed seven
checks and **120 framework tests**, with independent Astra High **CLEAN** review.
That result predates this host-result documentation integration and does not
validate its future final commit.

Host probes recorded base `94560c43bd4a5a062177870188f60a7ebafb5028` while the
RC manifest was uncommitted. The retained before/after packet fingerprints
**54 plugin files**; both sets match the candidate plugin bytes. Those exact
fingerprints identify tested content. A bare base SHA does not bind the RC
manifest. Both user-settings file hashes also matched before and after.

The initial private host packet retains invocation argv, prompts,
complete events, stderr, replies, exit status, verifier and the initial rubric.
Its 363-entry SHA-256 manifest was reopened with every entry matching. Public
hashes identify the retained packet; raw files and machine paths stay private.

| Receipt file | SHA-256 |
|---|---|
| `evidence-sha256.json` | `e8abcee68ecb6e05420ed4e5c0dc0e074b9f77c4fe9894312531c85898b5b9dd` |
| `check-report.json` | `add1828da8647e537c38f19eaa893c151a52b3af6bd144a0b084c7269b9ac81d` |
| `routes-verification.json` | `97fe20715548cad573973469bc56e3c372a5858b784cb91b6147d33954a5bbe2` |
| `before.json` | `950c265294f63b12e04dfe33a4d677bda83a34653beb7726530037d61d0cb222` |
| `after.json` | `206e929b744f9a998e3b6253695ea6a2b46ad069d11df5253e40e34b629a8dad` |

The separate corrected synthetic packet has **24 entries**, all reopened with
matching hashes. It retains the earlier denied packet and report unchanged.

| Corrected synthetic receipt | SHA-256 |
|---|---|
| `evidence-sha256.json` | `0186b1166354c3f67dc367bddf77b2c7e3069d38453cad17c8b6b7a0ebafb422` |
| `check-report.json` | `e84c8d45ec3e041a17bbae6a7a26594105e0163cb454ee7f332f184e4dbb51a9` |
| `normalize_topics.py` artifact | `516460e3d573220c78e606f0f58be256158ee3b99daa3895942780703aab8809` |
| Independent `coordinator-synthetic-behavior.json` | `4be8be73cf6613d92cf44e78da869f4a03e224e1d7484bf11c8b793ce2acff3e` |

## Read-only route previews

| Host | Observed path and result |
|---|---|
| Claude Code 2.1.290 | Direct command through session-local native plugin load; actual event-stream model `claude-opus-5-5`; exit 0 |
| Codex 0.160.1 | Disposable manual project-skill symlink/direct-read fallback; inherited configured `gpt-6.1-sol`, no invocation override; actual served model unconfirmed; exit 0 |

Each host returned **16 cases, 15 routes and 87 exact numbered step strings**.
The fifteen routes cover all fourteen playbooks plus `interrogate`; one route
has two cases. Actual tool events show every selected file was read. These
counts measure route/file selection and copied steps, not execution, test
assertions, repeated trials or general domain coverage.

The original **eleven literal fixture requests** matched expected domains and
proof obligations. Actual proof descriptions were inspected against mobile
lanes; literal proof-token matches were recorded separately and are not a
byte-identical proof-description test. No mobile proof ran.

Five supplemental cases extend route coverage. The Android Gradle-only prompt
does not establish implementation language. Codex correctly recorded it as
unresolved; Claude named Kotlin without repository evidence. The initial rubric
incorrectly required Kotlin; its mismatch remains retained alongside the
corrected Android-toolchain expectation. Host output was neither changed nor
rerun. No all-sixteen-domain validation is claimed.

Neither session exposed a native todo tool. Both displayed the copied
checklists; native todo integration remains unrun. Claude used
`--no-session-persistence` and Codex `--ephemeral`; durable resume and
multi-turn/compaction persistence remain unrun.

Initial sandbox attempts failed before route proof: Claude
`authentication_failed`, Codex runtime `Operation not permitted`. The same
scoped CLI probes completed under authorized escalation for existing host
authentication/runtime. Failed attempts remain in the packet. No installation,
global settings change, model override or permission bypass occurred.

## Initial synthetic setup failure

A separate Claude session registered `hugues-stack:hugues-agent` and launched
one fresh native worker plus one fresh native Explore reviewer. Parented tool
events show the worker read the actual mode and three principles, and the
reviewer read the mode and Prove It Works. This is **PASS for bounded delegated
loading/reads**. Init listed `Task`; emitted native calls used `Agent`. The
reviewer used observed Read/Glob tools; no complete reviewer-tool schema claim
is made. This session preserved normal hook policy.

The worker attempted one Write to the exact scratch target. Claude's
noninteractive permission system denied it despite an explicit one-path
`allowedTools` setting. The owner had authorized these host checks; the probe
lacked an effective matching Write grant and had no approval surface. This
was a probe setup/runtime permission limit, **not withheld owner authority or
a platform automatic approval review rejection**.
There was no retry or privilege broadening. Coordinator and reviewer Reads
confirmed the target absent; zero behavioral assertions ran.

The reviewer also assessed the unwritten proposal. That static assessment
accepted no implementation artifact. Its `all(...)` validation followed by
another traversal consumed generator input, a separate static defect; no
written artifact or executed red-green result existed in this attempt.

## Fresh bounded scratch delegation PASS

A fresh check used only exact-file Edit grants covering requested and resolved
scratch aliases. Claude's [permission rules](https://code.claude.com/docs/en/permissions#read-and-edit)
apply Edit rules to built-in writes and use `//` for absolute paths; the initial
Write-path rule was ineffective. Correcting the authorized probe's setup was
not a permission bypass. No broad Edit/Write grant, hook disabling, global
configuration change or scope expansion occurred.

Claude Code **2.1.290**, actual **`claude-opus-5-5`**, exited 0 with no denial.
The fresh registered `hugues-stack:hugues-agent` read the mode and principles,
then wrote the single scratch function once. A fresh native Explore reviewer
read the mode, principles and actual target and found no behavior defects.
Parented events retain both agents' actual reads and completed calls. The
coordinator also read the target. Init listed Task while emitted calls used
Agent; requested manual permission mode emitted default. This is same-host
fresh process independence, with no model-diversity or cross-host claim.

On the same hashed artifact, the outer worker's **22 assertions PASS** and the
coordinator's independently authored **14 literal checks PASS** cover trimming,
empty removal, sorting, case-sensitive uniqueness, immutable inputs, non-string
errors and one-pass iterable/generator handling. These are separate overlapping
assertion sets, not 36 unique tests and not additions to the 120 framework tests.
An initial coordinator AST preflight omitted the harmless `type` builtin;
source inspection corrected its whitelist without changing the artifact or
observing a behavior assertion failure. No commands or tests ran inside the
native session; Explore supplied static review only.

All 54 plugin fingerprints and both user-settings hashes remained unchanged.
Normal installed plugin/hook policy remained active, with strict empty MCP;
only observed public-plugin/scratch reads and the exact write are claimed.
No full mode execution, delegated mobile task, native todo integration,
red-green proof, generated-recipe cycle or persistence pass follows from this
bounded check. Historical mobile facts and their limits remain in the
[evidence index](evidence-index.md) and [support matrix](support.md).
