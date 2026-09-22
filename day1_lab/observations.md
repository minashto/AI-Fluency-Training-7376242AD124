# Day 1 Lab — Observations

**Provider used:** <ollama / groq / huggingface>
**Model used:** <e.g. qwen2.5:1.5b>

## 10. Observations Table

| Criterion                         | Chatbot | Workflow | Agent |
|------------------------------------|---------------------|------------------|--------------|
| Q1 correct? (Y/N)                  |    Y                |    Y             |   Y          |
| Q2 correct? (Y/N)                  |    Y                |    Y             |   Y          |
| Q3 correct? (Y/N)                  |    Y                |    Y             |   Y          |
| Q4 handled well? (Y/N)             |    Y                |    Y             |   Y          |
| Challenge question handled? (Y/N)  |    Y                |    Y             |   Y          |
| Same output on a repeat run? (Y/N) |    Y                |    Y             |   Y          |
| Approximate response time          |   0.9s              |   0.9s           |  0.7s        |
| Number of LLM calls per question   |    1                |    0             |  1-4         |
| One strength                       |   Smart             |  Fast            |   multi-step |
| One weakness                       |   Inaccesible       |  Limited         |  Complex     |
| Best suited for (one real use case)|  General convos     |  Repititve tasks | Real-time    |


## 11. Discussion Questions

1. The chatbot gave a confident but wrong fee. Why is that more dangerous than replying "I don't know"?

   A confidently wrong answer can mislead the user into acting on false information, while an honest "I don't know" (which this chatbot's system prompt is specifically designed to produce) preserves trust and pushes the user to verify the real numbers instead.

2. The workflow was always correct for questions 1 and 2. Why might a finance office still prefer it over the agent?

   Actually, in this build the workflow was not reliably correct for Q2, which nicely proves the opposite side of this same argument: a rule-based system is only as trustworthy as its rules, and it fails silently and consistently on cases outside them, whereas its failures are at least fully predictable and auditable. Where the rules do match (Q1, Q3), the workflow is deterministic, instant, free of LLM cost, and fully reproducible — which is exactly what a finance or operations team values most.

3. The agent's steps can change between runs. What problems would that cause in a real product?

   Varying step order or step count makes an agent harder to test, monitor, and audit, and can produce a different (though hopefully still correct) explanation or even a different final answer between runs on the same question.

4. Design a system that uses a workflow for common questions and an agent for the rest. Where would you draw the line?

   Route to the workflow only for a small set of very common, precisely worded lookups (single-project status, a known total calculation). Route everything else — new phrasing, multi-project reasoning, judgment calls like the challenge question — to the agent, and treat any workflow "no rule found" response as an automatic fallback trigger to call the agent instead of just failing

## 14. Result

Thus, a Python environment was set up in VS Code and connected to an open large language model, and a chatbot, a rule-based workflow, and an AI agent were implemented and compared on the same task. The observations show that ______________________________________________________________________________
