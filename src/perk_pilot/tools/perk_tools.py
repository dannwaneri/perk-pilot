"""Tools the agent uses to log perks and track build plans against them."""
from __future__ import annotations

from strands import tool

from perk_pilot import store


@tool
def log_perk(
    name: str,
    kind: str,
    expiry_date: str,
    amount: str = "",
    redemption_code: str = "",
    obligation: str = "",
    source: str = "",
) -> dict:
    """Record a perk extracted from an email or program notice.

    Args:
        name: Short human name for the perk, e.g. "AWS Community Builders credit".
        kind: One of "credit", "swag", "voucher", "requirement".
        expiry_date: ISO date (YYYY-MM-DD) the perk lapses or is due. Use your
            best estimate from relative dates like "90 days from this email".
        amount: Dollar value or quantity if applicable, e.g. "$500".
        redemption_code: Any code needed to claim it. Never invent one.
        obligation: What the user must still do, if this is a requirement
            rather than a reward, e.g. "publish 2 posts in 365 days".
        source: Where this perk was found, e.g. the email subject line.

    Returns:
        The stored perk record, including its id and days_left.
    """
    perk = store.add_perk(
        {
            "name": name,
            "kind": kind,
            "expiry_date": expiry_date,
            "amount": amount,
            "redemption_code": redemption_code,
            "obligation": obligation,
            "source": source,
        }
    )
    return perk


@tool
def list_open_perks() -> list[dict]:
    """List all logged perks with days remaining until expiry, soonest first."""
    perks = store.list_perks()
    return sorted(perks, key=lambda p: (p.get("days_left") is None, p.get("days_left", 9999)))


@tool
def propose_plan(
    perk_id: str,
    project_title: str,
    milestones: list[str],
    estimated_cost: str = "",
) -> dict:
    """Save a proposed build plan tied to a specific perk, awaiting user approval.

    Args:
        perk_id: The id of the perk this plan spends (from list_open_perks).
        project_title: One-line description of what will be built.
        milestones: Ordered list of small, concrete milestones with rough
            timing, e.g. ["Day 1: deploy Lambda skeleton", "Day 3: wire DynamoDB"].
        estimated_cost: Rough cost estimate so it can be checked against the
            perk's remaining value.

    Returns:
        The stored plan record, status "proposed" until the user approves it.
    """
    return store.add_plan(
        {
            "perk_id": perk_id,
            "project_title": project_title,
            "milestones": milestones,
            "estimated_cost": estimated_cost,
        }
    )


@tool
def list_plans() -> list[dict]:
    """List all build plans and their current status/progress notes."""
    return store.list_plans()


@tool
def update_plan(plan_id: str, status: str, note: str = "") -> dict | str:
    """Update a plan's status as the user makes progress or a decision.

    Args:
        plan_id: The plan id (from list_plans).
        status: One of "approved", "in_progress", "behind_pace", "shipped", "abandoned".
        note: Optional short note, e.g. "deployed Lambda skeleton" or
            "user chose to descope to just the API".
    """
    updated = store.update_plan_status(plan_id, status, note)
    if updated is None:
        return f"No plan found with id {plan_id}"
    return updated
