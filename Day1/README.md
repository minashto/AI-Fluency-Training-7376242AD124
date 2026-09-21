# Personal Expense Tracker — Chatbot vs Workflow vs Agent

This repo demonstrates the same private-data task (a personal expense
tracker) solved three ways: a plain chatbot, a rule-based workflow, and an
AI agent (LLM + Tools + Loop).

## Files

- `data/expenses.csv` — sample private expense data
- `data/budget.json` — hardcoded budget limits (used only by workflow.py)
- `chatbot.py` — plain chatbot approach
- `workflow.py` — rule-based workflow approach
- `agent.py` — AI agent approach (tool-using, loop-based)
- `analysis.md` — full written analysis (explanation, comparison table, suitability analysis, conclusion)
- `Output/` — console output from each script (replace with real screenshots before submitting)

## Running

No external dependencies are required to run the scripts in their default
(simulated) mode:

```bash
python3 chatbot.py
python3 workflow.py
python3 agent.py
```

### Optional: run with a real Claude API call

`chatbot.py` and `agent.py` will use the real Anthropic API instead of the
built-in simulation if you set an API key first:

```bash
export ANTHROPIC_API_KEY="your-key-here"
python3 chatbot.py
python3 agent.py
```

(`pip install requests` if it isn't already installed.)

## Before you submit

1. Run all three scripts yourself, take actual screenshots of the terminal
   output, and drop them into `Output/` (replacing or alongside the `.txt`
   files already there).
2. Skim `analysis.md` and adjust anything you'd like to phrase in your own
   words — it should read as your own reasoning.
3. `git init`, commit everything, push to a new GitHub repo, and submit the
   repo link.
