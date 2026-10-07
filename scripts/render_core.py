"""Render tiny host entrypoints; workflow bodies stay immutable in plugin/core."""
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def skill_loader(name, row, root=ROOT):
    source = (root / 'plugin/core' / row['source']).read_text()
    flag = '\ndisable-model-invocation: true' if re.search(
        r'^disable-model-invocation: true$', source, re.M) else ''
    leaf = row['source'].split('/')[2]
    return f'''---
name: {name}
description: "Pinned pstack 0.15.9 {leaf} workflow with explicit Claude Code, Codex and mobile adapters."
source: {row['source']}{flag}
---

# {name}

Before work, read in full and in this order:

1. [Host adapter](../../adapters/host.md).
2. [Mobile adapter](../../adapters/mobile.md).
3. [Project PR policy](../../policies/astra-pr-review.md).
4. [Pinned {leaf} core](../../core/{row['source']}).

Execute that core contract, applying only the named adapter translations and
explicit project policy. Read its phase-required references in full. Do not
substitute this loader for the workflow. Report blocked gates and actual proof.
'''


def playbook_loader(name, row):
    return f'''# {name}

Read [host adapter](../../../adapters/host.md),
[mobile adapter](../../../adapters/mobile.md),
[project PR policy](../../../policies/astra-pr-review.md), then the
[pinned {name} playbook](../../../core/{row['source']}) in full.
Copy its ordered todos verbatim before execution. Keep skips with their reasons.
The pinned source owns the steps; the adapters translate host mechanics and add
applicable mobile proof. Missing capability blocks the gate, not its existence.
'''


WORKER = '''---
name: hugues-agent
description: Fresh native wrapper for the pinned pstack worker; read the full mode and adapters before scoped work.
source: pstack/agents/poteto-agent.md
---

# Native worker

Read [host adapter](../adapters/host.md), [mobile adapter](../adapters/mobile.md),
[project PR policy](../policies/astra-pr-review.md),
[pinned worker](../core/pstack/agents/poteto-agent.md), and
[hugues-mode](../skills/hugues-mode/SKILL.md) in full before work.
Use the coordinator-supplied absolute mode, skills, core and adapter paths.
Read each applicable principle leaf in full. A fresh scoped worker performs its
assigned round directly without recursive delegation of the same assignment.
Preserve base/head, writable scope, consumer authority and success predicate.
Return actual diff, checks with exit codes, evidence and unresolved gaps; the
coordinator independently verifies. Background execution is a host capability,
not a promise; disclose when the native host lacks it.
'''


def outputs(root=ROOT):
    binding = json.loads((root / 'plugin/core-bindings.json').read_text())
    result = {}
    for name, row in binding['skills'].items():
        result[row['entrypoint']] = ((root / 'plugin/core' / row['source']).read_text()
                                    if row['kind'] == 'verbatim' else skill_loader(name, row, root))
    for name, row in binding['playbooks'].items():
        result[row['entrypoint']] = playbook_loader(name, row)
    result['plugin/agents/hugues-agent.md'] = WORKER
    return result


if __name__ == '__main__':
    for destination, content in outputs().items():
        path = ROOT / destination
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
