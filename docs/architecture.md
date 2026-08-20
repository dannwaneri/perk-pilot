# Architecture

```mermaid
flowchart TD
    U[User: forwards a perk email / asks<br/>'what should I build next?'] --> A

    subgraph Agent["Strands Agent (Bedrock model)"]
        direction TB
        R1[Extract perks from noisy email text]
        R2[Weigh open perks by urgency + value]
        R3[Propose ONE scoped build + milestones]
        R4[Track progress, escalate only if behind pace]
        R1 --> R2 --> R3 --> R4
    end

    A --> Agent
    Agent --> T1[log_perk]
    Agent --> T2[list_open_perks]
    Agent --> T3[propose_plan]
    Agent --> T4[list_plans / update_plan]

    T1 & T2 & T3 & T4 --> S[(Perk + plan store<br/>local JSON now,<br/>DynamoDB in production)]

    Agent --> O[Output: extracted perk records,<br/>proposed build plan,<br/>progress nudges]
    O --> U

    subgraph AWS["AWS services (production path)"]
        Bedrock[Amazon Bedrock — model]
        Dynamo[DynamoDB — perk/plan store]
        Lambda[Lambda / AgentCore Runtime — agent host]
        EventBridge[EventBridge — scheduled check-ins]
    end

    Agent -.->|swap in| AWS
```

## Components

| Layer | Now (hackathon demo) | Production path |
|---|---|---|
| Interface | CLI (`demo.py`) feeding sample emails | Web/chat form or email-forward address |
| Agent core | Strands `Agent` with a system prompt encoding the extract → prioritize → propose → track loop | Same, deployed via AgentCore Runtime |
| Model | Amazon Bedrock (Claude) | Same |
| Tools | `log_perk`, `list_open_perks`, `propose_plan`, `list_plans`, `update_plan` | Same tools, same signatures |
| Store | Local JSON file (`data/store.json`) | DynamoDB table, same read/write shape |
| Scheduling | Manual re-invocation | EventBridge-triggered check-ins |

## Why this loop is agentic, not a lookup

The reasoning steps that matter — deciding which perk is urgent enough to
act on, scoping a build that plausibly fits the remaining time/budget, and
deciding whether progress is "on pace" or needs to surface to the user —
are judgment calls, not deterministic lookups. A cloud credit dashboard
can tell you a balance and a date; it can't tell you what to build with it
or whether you're falling behind.
