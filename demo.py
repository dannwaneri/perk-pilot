"""End-to-end demo: feed sample perk emails to the agent, then ask it to
propose a build plan for the most urgent one.

Run:
    .venv/Scripts/python demo.py
"""
from pathlib import Path

from perk_pilot.agent import build_agent

SAMPLE_DIR = Path(__file__).parent / "data" / "sample_emails"


def main() -> None:
    agent = build_agent()

    print("=== Step 1: ingest perk emails ===\n")
    for email_path in sorted(SAMPLE_DIR.glob("*.txt")):
        print(f"--- {email_path.name} ---")
        agent(
            f"Here is an email. Extract any perks it contains using log_perk.\n\n"
            f"{email_path.read_text(encoding='utf-8')}"
        )
        print()

    print("\n=== Step 2: what should I do next? ===\n")
    agent(
        "Review my open perks and propose a build plan for the most "
        "urgent one that's worth acting on."
    )


if __name__ == "__main__":
    main()
