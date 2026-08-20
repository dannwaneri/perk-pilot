"""Local JSON-backed store for perks and build plans.

Swap this for a DynamoDB-backed implementation with the same function
signatures when deploying (see docs/architecture.md).
"""
from __future__ import annotations

import json
from datetime import date, datetime
from pathlib import Path
from typing import Any

STORE_PATH = Path(__file__).resolve().parents[2] / "data" / "store.json"


def _load() -> dict[str, Any]:
    if not STORE_PATH.exists():
        return {"perks": [], "plans": []}
    return json.loads(STORE_PATH.read_text(encoding="utf-8"))


def _save(data: dict[str, Any]) -> None:
    STORE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STORE_PATH.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")


def add_perk(perk: dict[str, Any]) -> dict[str, Any]:
    data = _load()
    perk = dict(perk)
    perk["id"] = f"perk_{len(data['perks']) + 1}"
    perk["logged_at"] = datetime.now().isoformat(timespec="seconds")
    data["perks"].append(perk)
    _save(data)
    return perk


def list_perks() -> list[dict[str, Any]]:
    perks = _load()["perks"]
    today = date.today()
    for perk in perks:
        expiry = perk.get("expiry_date")
        if expiry:
            try:
                days_left = (date.fromisoformat(expiry) - today).days
                perk["days_left"] = days_left
            except ValueError:
                perk["days_left"] = None
    return perks


def add_plan(plan: dict[str, Any]) -> dict[str, Any]:
    data = _load()
    plan = dict(plan)
    plan["id"] = f"plan_{len(data['plans']) + 1}"
    plan["created_at"] = datetime.now().isoformat(timespec="seconds")
    plan.setdefault("status", "proposed")
    data["plans"].append(plan)
    _save(data)
    return plan


def list_plans() -> list[dict[str, Any]]:
    return _load()["plans"]


def update_plan_status(plan_id: str, status: str, note: str = "") -> dict[str, Any] | None:
    data = _load()
    for plan in data["plans"]:
        if plan["id"] == plan_id:
            plan["status"] = status
            if note:
                plan.setdefault("progress_notes", []).append(
                    {"at": datetime.now().isoformat(timespec="seconds"), "note": note}
                )
            _save(data)
            return plan
    return None
