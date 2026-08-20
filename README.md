# Perk Pilot

An agent that turns unused developer perks — cloud credits, program swag,
certification vouchers, content requirements — into shipped work before
they expire.

Built with the [Strands Agents SDK](https://strandsagents.com/) for the
**Agents for Humans Hackathon** (Everyday Agents track).

## The problem

Developer programs (AWS Community Builders, hackathon prize credits,
certification vouchers, startup credit programs) hand out real, valuable,
time-boxed perks. The information about them rarely arrives cleanly — it's
usually buried inside a noisy weekly digest email alongside a dozen
unrelated announcements. The perk gets acknowledged, then forgotten, then
it expires unused. This isn't a lack of awareness problem — every
"tracker" tool assumes you already know what you have. It's an
**activation** problem: nothing turns "I have this benefit" into "I
actually built something with it" before the deadline.

## What it does

1. **Extract** — feed it a forwarded program email or digest; the agent
   pulls out every distinct perk (credit, swag, voucher, content
   requirement) with its expiry date, value, and any code — ignoring the
   surrounding newsletter noise.
2. **Prioritize** — across everything logged, it reasons about which perk
   is most urgent and worth acting on.
3. **Propose** — it drafts ONE scoped, time-boxed build plan with small
   milestones that plausibly fit inside the remaining time and budget.
   This is a proposal, not a decision — the agent always asks for
   approval before treating a plan as active.
4. **Track quietly** — as you check in on progress, it only speaks up when
   you're falling behind pace relative to the expiry date. On track means
   silence.

## Architecture

See [docs/architecture.md](docs/architecture.md) for the full diagram.

```
Email/notice text
        |
        v
  Strands Agent  <----->  log_perk / list_open_perks / propose_plan /
  (Bedrock model)         list_plans / update_plan   (tools)
        |                          |
        v                          v
  Reasoning: urgency,        Local JSON store (data/store.json)
  scoping, escalation        -> swap for DynamoDB in production
        |
        v
  Proposed build plan -> user approval -> milestone tracking
```

## Setup

Requires Python 3.11+ and an AWS account with Bedrock model access enabled
(Claude models, `us-west-2` by default — see [Strands quickstart](https://strandsagents.com/docs/user-guide/quickstart/python/)).

```bash
python -m venv .venv
.venv/Scripts/activate   # or source .venv/bin/activate on macOS/Linux
pip install -e .
aws configure             # if you haven't already set up AWS credentials
```

## Run the demo

```bash
python demo.py
```

This feeds three sample perk notices (`data/sample_emails/`, synthetic —
modeled on real AWS Community Builders emails but with placeholder codes)
through the agent, then asks it to propose a build plan for the most
urgent one.

## Status

Early hackathon build. The local JSON store is a stand-in for DynamoDB;
perk extraction currently takes pasted/forwarded email text rather than a
live inbox connection.

## License

MIT — see [LICENSE](LICENSE).
