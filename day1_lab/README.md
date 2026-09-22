# Day 1 Lab — Chatbot vs Rule-Based Workflow vs AI Agent (VS Code)

All code from the lab manual, ready to drop into VS Code.

## Setup (do this on your own machine, in VS Code)

1. Open this `day1_lab` folder in VS Code (**File > Open Folder**).
2. Open a terminal (`Ctrl+\``) and create a virtual environment:
   ```
   python -m venv .venv
   ```
   Then activate it:
   - Windows PowerShell: `.venv\Scripts\Activate.ps1`
   - Windows CMD: `.venv\Scripts\activate`
   - Linux/macOS: `source .venv/bin/activate`
   Or press `Ctrl+Shift+P` → **Python: Create Environment** → **Venv**.
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Set up your LLM (pick ONE):
   - **Option A — Ollama (local, no key):** install from https://ollama.com/download, then
     ```
     ollama pull qwen2.5:1.5b
     ```
   - **Option B — Groq (free key):** sign up at https://console.groq.com, create an API key.
   - **Option C — Hugging Face (free token):** sign up at https://huggingface.co, create a Read token.
5. Copy `.env.example` to `.env` and fill in the option you chose:
   ```
   cp .env.example .env      # Linux/macOS
   copy .env.example .env    # Windows
   ```
   Edit `.env` so only your chosen provider's lines are active. **Never commit `.env` — it's already in `.gitignore`.**

## Run, in this order

```
python check_setup.py   # confirms the connection works — must print "SETUP OK" before continuing
python tools.py          # sanity-checks the calculator and fee lookup (no LLM needed)
python chatbot.py        # System 1
python workflow.py       # System 2
python agent.py          # System 3
python challenge.py      # the unplanned-for question
```

After each run, fill in `observations.md` with what you actually saw (answers vary by model/provider — that's expected and part of the lab).

## Files

- `config.py` — provider setup + shared course data
- `check_setup.py` — connection test (run first)
- `chatbot.py` — System 1: plain LLM chatbot
- `workflow.py` — System 2: rule-based workflow (no LLM) — verified working, see `Output/`
- `tools.py` — tool functions + schemas for the agent — verified working, see `Output/`
- `agent.py` — System 3: LLM + tools + loop
- `challenge.py` — tests all systems on an unplanned-for question
- `observations.md` — fill this in after running everything
- `.env.example` — template; copy to `.env` and fill in locally (never commit `.env`)
