"""
2. RULE-BASED WORKFLOW
-----------------------
This script represents the "rule-based workflow" approach to the
expense-tracker scenario.

Key property being demonstrated:
    A rule-based workflow follows PREDEFINED steps and conditions, with
    NO LLM involved at all.
    - It CAN access private data directly (it reads data/expenses.csv and
      data/budget.json straight off disk).
    - It follows a fixed sequence of steps written in advance by the
      programmer: read file -> group by category -> sum -> compare to a
      hardcoded budget -> print a fixed-format report.
    - It cannot handle a question it wasn't specifically coded for. Ask it
      anything outside its hardcoded logic (e.g. "compare July and August
      restaurant spending only") and it simply has no path to do that.

Run:
    python workflow.py
"""

import csv
import json
import os
from collections import defaultdict

DATA_FILE = os.path.join("data", "expenses.csv")
BUDGET_FILE = os.path.join("data", "budget.json")


def load_expenses(path):
    rows = []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["amount"] = float(row["amount"])
            rows.append(row)
    return rows


def load_budget(path):
    with open(path) as f:
        return json.load(f)


def totals_by_category_for_month(rows, month_prefix):
    totals = defaultdict(float)
    for r in rows:
        if r["date"].startswith(month_prefix):
            totals[r["category"]] += r["amount"]
    return totals


def main():
    print("=== RULE-BASED WORKFLOW DEMO ===\n")

    # Step 1 (fixed): read the file
    expenses = load_expenses(DATA_FILE)
    budget = load_budget(BUDGET_FILE)
    print(f"Step 1: Loaded {len(expenses)} rows from {DATA_FILE}")

    # Step 2 (fixed): this workflow is hardcoded to only ever check "2026-08"
    TARGET_MONTH = "2026-08"
    print(f"Step 2: Filtering rows for hardcoded target month {TARGET_MONTH}")
    totals = totals_by_category_for_month(expenses, TARGET_MONTH)

    # Step 3 (fixed): compare each category total to the hardcoded budget
    print("Step 3: Comparing totals against data/budget.json\n")
    print(f"{'Category':<15}{'Spent':<10}{'Budget':<10}{'Status'}")
    print("-" * 50)
    for category, limit in budget.items():
        spent = totals.get(category, 0.0)
        status = "OVER BUDGET" if spent > limit else "OK"
        print(f"{category:<15}{spent:<10.0f}{limit:<10}{status}")

    # Step 4 (fixed): a single hardcoded conditional message
    food_spent = totals.get("Food", 0.0)
    food_budget = budget.get("Food", 0)
    print("\nStep 4: Fixed conditional rule for 'Food' category")
    if food_spent > food_budget:
        print(
            f"-> RULE TRIGGERED: Food spending ({food_spent:.0f}) exceeds "
            f"budget ({food_budget}). Printing fixed warning message."
        )
    else:
        print(
            f"-> Food spending ({food_spent:.0f}) is within budget "
            f"({food_budget}). Printing fixed OK message."
        )

    print("\n--- LIMITATION ---")
    print(
        "This workflow can ONLY ever check the hardcoded month (2026-08)\n"
        "against the hardcoded budget file. If the user asks a different\n"
        "question -- e.g. 'compare this month to last month' or 'which\n"
        "single day did I spend the most on food' -- there is no code path\n"
        "for it. Someone would have to open this script and add a brand\n"
        "new function for every new type of question."
    )


if __name__ == "__main__":
    main()
