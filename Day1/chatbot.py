"""
1. PLAIN CHATBOT
----------------
This script represents the "plain chatbot" approach to the expense-tracker
scenario.

Key property being demonstrated:
    A plain chatbot mainly provides responses using an LLM ALONE.
    - It has NO access to files on disk (it cannot open data/expenses.csv).
    - It has NO tools (no calculator function, no file reader, no database).
    - It has NO loop -- it answers once, based only on whatever text the
      user pastes into the conversation, then stops.

To make it answer a question about "my expenses", the user must manually
copy-paste their expense data into the prompt. If they forget to paste
something, or paste it wrong, the chatbot simply cannot know it exists --
it has no way to go check for itself.

Run:
    python chatbot.py
"""

import os

# Optional: use the real Anthropic API if a key is available.
# If not, we fall back to a simple simulated "LLM-style" answer so the
# script still runs end-to-end for the screenshot / demo.
USE_REAL_API = bool(os.environ.get("ANTHROPIC_API_KEY"))

PASTED_DATA = """
date,category,amount
2026-08-02,Food,500
2026-08-07,Food,600
2026-08-12,Food,280
2026-08-20,Food,550
2026-08-23,Food,300
2026-08-29,Food,420
"""

USER_QUESTION = "How much did I spend on food in August, and am I overspending?"


def call_llm(prompt: str) -> str:
    if USE_REAL_API:
        import requests
        resp = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": os.environ["ANTHROPIC_API_KEY"],
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": "claude-sonnet-4-6",
                "max_tokens": 300,
                "messages": [{"role": "user", "content": prompt}],
            },
            timeout=30,
        )
        data = resp.json()
        return "".join(b.get("text", "") for b in data.get("content", []))

    # --- Simulated LLM response (fallback, no API key needed) ---
    # A plain chatbot can only reason over the text it was given -- it has
    # no way to verify totals, no way to check a real budget, and no way
    # to look beyond what was pasted in.
    return (
        "Based on the numbers you pasted, your food expenses in August "
        "were roughly: 500 + 600 + 280 + 550 + 300 + 420 = 2650.\n"
        "I can't say for certain whether that counts as 'overspending' "
        "because I don't know your budget, and I have no way to check "
        "your actual expense records myself -- I only know what you typed "
        "into this message. If you pasted an incomplete list, or there are "
        "more August food expenses in your records that you didn't include, "
        "my answer will be wrong and I have no way of knowing that."
    )


def main():
    print("=== PLAIN CHATBOT DEMO ===\n")
    print("User pastes their data directly into the chat:\n")
    print(PASTED_DATA)
    print(f"User question: {USER_QUESTION}\n")
    print("Chatbot response:\n")
    prompt = f"Here is my expense data:\n{PASTED_DATA}\n\nQuestion: {USER_QUESTION}"
    print(call_llm(prompt))
    print("\n--- LIMITATION ---")
    print(
        "This chatbot never touched data/expenses.csv. It has no tools and\n"
        "no memory of past months beyond what was pasted. It cannot verify\n"
        "anything, cannot fetch the July data to compare, and cannot take\n"
        "any follow-up action (e.g. flag the overspend, send an alert)."
    )


if __name__ == "__main__":
    main()
