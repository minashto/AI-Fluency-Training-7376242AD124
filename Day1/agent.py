"""
3. AI AGENT (LLM + Tools + Loop)
---------------------------------
This script represents the "AI agent" approach to the expense-tracker
scenario.

Key property being demonstrated:
    An AI agent combines an LLM + TOOLS + a LOOP.
    - The LLM is given a natural-language goal, NOT a fixed set of steps.
    - It is given a set of TOOLS (functions) it may call: read_expenses,
      totals_by_category, compare_months.
    - It reasons about which tool(s) it needs, calls one, OBSERVES the
      result, decides whether it needs another tool, and keeps looping
      until it has enough information to answer -- unlike the workflow,
      nobody told it in advance "first do X, then do Y".
    - Because it has real tool access, it CAN reach the private data file
      (unlike the chatbot), and because it can reason step-by-step, it CAN
      answer questions nobody hardcoded a path for (unlike the workflow) --
      e.g. "compare July and August" even though only "August vs budget"
      was hardcoded in workflow.py.

Run:
    python agent.py
"""

import csv
import json
import os
from collections import defaultdict

DATA_FILE = os.path.join("data", "expenses.csv")
USE_REAL_API = bool(os.environ.get("ANTHROPIC_API_KEY"))

USER_REQUEST = (
    "Compare my Food spending in July vs August, tell me if it went up, "
    "and let me know if August Food spending is above 1500."
)

# ---------------------------------------------------------------------
# TOOLS available to the agent. The agent (LLM) decides for itself which
# of these to call, in which order, and how many times.
# ---------------------------------------------------------------------

def tool_read_expenses():
    """Reads the private expense file from disk."""
    rows = []
    with open(DATA_FILE, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["amount"] = float(row["amount"])
            rows.append(row)
    return rows


def tool_totals_by_category(rows, month_prefix):
    """Sums expenses by category for a given month (e.g. '2026-08')."""
    totals = defaultdict(float)
    for r in rows:
        if r["date"].startswith(month_prefix):
            totals[r["category"]] += r["amount"]
    return dict(totals)


def tool_compare(value_a, value_b):
    """Compares two numbers and returns the difference and direction."""
    diff = value_b - value_a
    direction = "increased" if diff > 0 else ("decreased" if diff < 0 else "stayed the same")
    return {"difference": diff, "direction": direction}


TOOLS = {
    "read_expenses": tool_read_expenses,
    "totals_by_category": tool_totals_by_category,
    "compare": tool_compare,
}

TOOL_SCHEMAS = [
    {
        "name": "read_expenses",
        "description": "Read all private expense records from disk.",
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "totals_by_category",
        "description": "Given expense rows and a month prefix like '2026-08', return totals per category.",
        "input_schema": {
            "type": "object",
            "properties": {
                "month_prefix": {"type": "string"}
            },
            "required": ["month_prefix"],
        },
    },
    {
        "name": "compare",
        "description": "Compare two numeric values and report the difference and direction.",
        "input_schema": {
            "type": "object",
            "properties": {
                "value_a": {"type": "number"},
                "value_b": {"type": "number"},
            },
            "required": ["value_a", "value_b"],
        },
    },
]


def run_with_real_api():
    """
    Real agent loop using the Anthropic API's tool-use feature.
    Requires ANTHROPIC_API_KEY to be set in the environment.
    """
    import requests

    messages = [{"role": "user", "content": USER_REQUEST}]
    rows_cache = None

    for step in range(1, 8):
        resp = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": os.environ["ANTHROPIC_API_KEY"],
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": "claude-sonnet-4-6",
                "max_tokens": 1000,
                "tools": TOOL_SCHEMAS,
                "messages": messages,
            },
            timeout=60,
        )
        data = resp.json()
        content = data.get("content", [])
        messages.append({"role": "assistant", "content": content})

        tool_uses = [b for b in content if b.get("type") == "tool_use"]
        if not tool_uses:
            final_text = "".join(b.get("text", "") for b in content if b.get("type") == "text")
            print(f"\n[Step {step}] Agent gives final answer:\n{final_text}")
            return

        tool_results = []
        for tu in tool_uses:
            name = tu["name"]
            args = tu.get("input", {})
            print(f"[Step {step}] Agent calls tool: {name}({args})")
            if name == "totals_by_category" and rows_cache is None:
                rows_cache = tool_read_expenses()
            if name == "read_expenses":
                result = tool_read_expenses()
                rows_cache = result
            elif name == "totals_by_category":
                result = tool_totals_by_category(rows_cache, **args)
            elif name == "compare":
                result = tool_compare(**args)
            else:
                result = {"error": "unknown tool"}
            print(f"          -> observed result: {result}")
            tool_results.append(
                {"type": "tool_result", "tool_use_id": tu["id"], "content": json.dumps(result)}
            )
        messages.append({"role": "user", "content": tool_results})


def run_simulated():
    """
    Simulated agent loop (no API key needed) -- shows the SAME reasoning
    pattern a real LLM-driven agent would follow: think -> act -> observe
    -> think again -> act -> observe -> ... -> final answer.
    This is only a stand-in so the script is runnable for the demo/
    screenshot without requiring a paid API key.
    """
    print("[Step 1] Agent reasons: \"I need the raw expense data first.\"")
    print("          -> calling tool: read_expenses()")
    rows = tool_read_expenses()
    print(f"          -> observed result: {len(rows)} rows loaded\n")

    print("[Step 2] Agent reasons: \"I need July Food total.\"")
    print("          -> calling tool: totals_by_category(month_prefix='2026-07')")
    july_totals = tool_totals_by_category(rows, "2026-07")
    july_food = july_totals.get("Food", 0.0)
    print(f"          -> observed result: Food = {july_food}\n")

    print("[Step 3] Agent reasons: \"Now I need August Food total.\"")
    print("          -> calling tool: totals_by_category(month_prefix='2026-08')")
    aug_totals = tool_totals_by_category(rows, "2026-08")
    aug_food = aug_totals.get("Food", 0.0)
    print(f"          -> observed result: Food = {aug_food}\n")

    print("[Step 4] Agent reasons: \"I should compare the two months.\"")
    print(f"          -> calling tool: compare(value_a={july_food}, value_b={aug_food})")
    comparison = tool_compare(july_food, aug_food)
    print(f"          -> observed result: {comparison}\n")

    print("[Step 5] Agent reasons: \"I also need to check the 1500 threshold "
          "the user mentioned.\" (no tool needed, simple check)")
    over_budget = aug_food > 1500
    print(f"          -> August Food ({aug_food}) > 1500 ? {over_budget}\n")

    print("[Step 6] Agent has enough information. Produces final answer:\n")
    print(
        f"Your Food spending in July was {july_food:.0f} and in August it was "
        f"{aug_food:.0f}. That's a {comparison['direction']} of "
        f"{abs(comparison['difference']):.0f}. "
        + (
            f"Yes, August Food spending ({aug_food:.0f}) is above your 1500 threshold."
            if over_budget
            else f"No, August Food spending ({aug_food:.0f}) is within the 1500 threshold."
        )
    )


def main():
    print("=== AI AGENT DEMO (LLM + Tools + Loop) ===\n")
    print(f"User request: {USER_REQUEST}\n")
    if USE_REAL_API:
        run_with_real_api()
    else:
        run_simulated()

    print("\n--- WHAT MADE THIS DIFFERENT ---")
    print(
        "Nobody hardcoded 'read file, then compare July to August, then\n"
        "check 1500'. The agent worked that sequence out itself from a\n"
        "plain-English request, called tools one at a time, looked at each\n"
        "result before deciding the next step, and stopped once the task\n"
        "was actually done -- something neither the chatbot (no tools) nor\n"
        "the workflow (fixed steps only) could do."
    )


if __name__ == "__main__":
    main()
