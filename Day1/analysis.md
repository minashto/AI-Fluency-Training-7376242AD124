# Comparing a Plain Chatbot, a Rule-Based Workflow, and an AI Agent on a Personal Expense-Tracking Scenario

## 1. The Scenario

The private-data scenario I chose is a **personal expense tracker**. I keep a
private record of my daily spending (`data/expenses.csv`), with each entry
containing a date, a category (Food, Transport, Entertainment, Bills,
Shopping), an amount, and a short description. This is private data in the
sense that it lives only on my own machine and is not something a public LLM
would ever have seen during training or could look up on the web.

The task I use to compare all three approaches is: *"Compare my Food
spending in July vs August, tell me if it went up, and let me know if August
Food spending is above 1500."* This question was deliberately chosen because
it requires (a) reading real private data, (b) doing more than one step, and
(c) making a small decision (over/under a threshold) based on the result of
a calculation — which makes the differences between the three approaches
very visible.

## 2. Explanation of Each Approach

### 2.1 Plain Chatbot (`chatbot.py`)

A plain chatbot mainly provides responses using an **LLM alone**. In this
implementation, the chatbot has no connection whatsoever to
`data/expenses.csv` — it cannot open it, list it, or even know it exists.
The only way it can "see" any of my expense data is if I manually copy and
paste it into the conversation, which is exactly what the script does: it
pastes six lines of August food expenses directly into the prompt before
asking the question.

From start to finish, the chatbot's process is: receive a prompt containing
whatever text the user typed → generate a response based purely on that
text and the model's general language ability → return the answer → stop.
There are no tools, no rules, and no loop. It cannot go back and fetch more
data if it needs it, and it cannot verify anything against a source of
truth.

The limitation shows up immediately on this scenario: the chatbot can only
add up the six numbers I happened to paste in. It has no way to retrieve the
July figures to make the requested comparison unless I paste those too, and
it has no way to independently confirm that 1500 is actually my budget for
that category — it can only take my word for it. If I paste incomplete or
slightly wrong data, the chatbot has no mechanism to notice or correct that,
because it never touches the real file.

### 2.2 Rule-Based Workflow (`workflow.py`)

A rule-based workflow follows **predefined steps and conditions, with no
LLM involved**. This script reads `data/expenses.csv` and `data/budget.json`
directly off disk using ordinary file-handling code, so — unlike the
chatbot — it genuinely can access my private data. But everything it does
with that data was decided by me, the programmer, in advance: it always
filters for the hardcoded month `"2026-08"`, always groups by category using
the same fixed loop, and always compares each category's total against the
same hardcoded `budget.json` file using the same fixed `if spent > limit`
condition.

Its start-to-finish process is a fixed pipeline: load file → filter by a
hardcoded month string → sum by category → compare each sum to a hardcoded
budget number → print a report in a fixed format. There is no reasoning
step anywhere — every branch the code can take was written out by hand
beforehand.

The limitation is obvious on this exact scenario: the task asks for a
July-vs-August *comparison*, but `workflow.py` was never written with a
"compare two months" function — it only knows how to check one hardcoded
month against a budget file. To answer the actual question asked, I would
have to go back into the code and write an entirely new function. The
workflow is reliable and repeatable for the one job it was built for, but it
cannot adapt itself to a slightly different request the way the other two
approaches can.

### 2.3 AI Agent (`agent.py`)

An AI agent combines an **LLM + Tools + a Loop**. Instead of being handed a
fixed sequence of steps, the agent is given the plain-English request and a
small set of tools it is free to use as it sees fit: `read_expenses()`,
`totals_by_category(month_prefix)`, and `compare(value_a, value_b)`. The
LLM decides for itself which tool to call, when to call it, and what to do
with the result.

Its start-to-finish process, visible in the console output, is: reason
("I need the raw data first") → call `read_expenses` → observe the result
(22 rows) → reason again ("I need July's Food total") → call
`totals_by_category('2026-07')` → observe the result (1720) → reason again
("now August") → call `totals_by_category('2026-08')` → observe the result
(2650) → reason again ("I should compare these") → call `compare(1720,
2650)` → observe the result (increased by 930) → check the 1500 threshold →
decide it now has enough information → produce a final natural-language
answer and stop. This is the LLM + Tools + Loop pattern: reason, act,
observe, repeat, until done.

The main limitation on this scenario is less about capability and more
about control and cost: because the agent is reasoning for itself at every
step rather than following a fixed script, its exact tool-calling sequence
can vary slightly between runs, it is slower and more computationally
expensive than the workflow for a job this simple, and if the available
tools were poorly described the agent could misuse them or take an
inefficient path to the answer. For a one-off, well-defined report, that
flexibility is more overhead than benefit — but the moment the question
changes (as it does here, from workflow.py's hardcoded single-month check
to a genuine two-month comparison), the agent handles the new request
without anyone rewriting its code, which neither of the other two
approaches can do.

## 3. Comparison Table

| Basis for comparison        | Plain chatbot                                                                 | Rule-based workflow                                                                 | AI agent                                                                                   |
|------------------------------|-------------------------------------------------------------------------------|---------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------|
| **Flexibility**              | Very low — can only respond to what is pasted in; cannot handle new questions without the user manually supplying new data | Very low — only answers the exact question it was coded for (single month vs hardcoded budget); a new question needs new code | High — can handle a new phrasing or a new combination of the same tools without any code changes |
| **Decision-making**          | Surface-level; guesses/estimates based on text, cannot verify anything        | None; every branch is a fixed `if/else` written in advance                            | Genuine step-by-step reasoning; decides which tool to call next based on the result of the last one |
| **Tool usage**                | None                                                                           | Uses plain code (file I/O), but not "tools" in the reasoning sense — nothing is chosen dynamically | Uses defined tools (`read_expenses`, `totals_by_category`, `compare`) and chooses which to call and in what order |
| **Private-data access**       | None — cannot open `expenses.csv`; relies entirely on the user pasting data manually | Full — reads `expenses.csv` and `budget.json` directly from disk                      | Full — reads the same private file via its tools, on its own initiative                       |
| **Multi-step task handling**  | Cannot chain steps; one prompt in, one answer out                             | Can perform multiple fixed steps, but only the exact sequence that was pre-programmed  | Naturally handles multi-step tasks (read → compute A → compute B → compare → check threshold → answer) |
| **Automation**                 | Low — a human must manually gather and paste the relevant data every time    | High for the one task it was built for, but any new task requires manual re-coding    | High and generalizable — the same agent can be pointed at new but related questions without modification |
| **Reliability**                | Low — answer quality depends entirely on what was pasted and can't be checked | Very high — deterministic, same input always gives the same output, easy to test       | Good but not perfectly deterministic — correct in this run, but reasoning-driven tool calls can vary slightly between runs |

## 4. Suitability Analysis

For this specific scenario — a personal expense tracker where I want to ask
varied, sometimes multi-step questions about my own private spending data —
the **AI agent is the most suitable approach**.

The comparison table makes the reasoning clear. Private-data access rules
out the plain chatbot immediately: it simply cannot reach `expenses.csv` on
its own, and requiring me to manually copy-paste my spending every time I
have a question defeats the purpose of having a tracker at all. That leaves
the rule-based workflow and the agent, both of which can genuinely read the
file. The deciding factors are flexibility and multi-step task handling:
the question I actually wanted answered ("compare July and August, then
check a threshold") was not something `workflow.py` could do without being
rewritten, while `agent.py` handled it correctly on the first attempt simply
because it was given tools and allowed to reason about how to combine them.
Automation reinforces this — a workflow only stays "automated" for the
exact question it was built for, whereas the agent generalizes to related
questions I have not thought of yet, which matters for a tracker I intend
to keep using and asking new things of over time.

The one place the workflow wins outright is reliability and cost: for the
single, narrow task of "check this month against my fixed budget," the
workflow is deterministic, cheap, and trivially testable, while the agent
is doing more computation than strictly necessary to reach the same
conclusion. In a production version of this expense tracker, the realistic
answer is a hybrid: use a rule-based workflow for the fixed, repeated report
(e.g. a monthly budget check that runs automatically), and reserve the agent
for the free-form, exploratory questions a user might ask on demand. But
if I have to pick one single approach for a general-purpose personal
expense assistant, the agent is the right choice because it is the only one
of the three that combines real private-data access with the ability to
answer questions I didn't specifically pre-program it to answer.

## 5. Conclusion — When to Use Each Approach in General

Stepping back from this one scenario, the three approaches suit genuinely
different classes of problem, and the right choice depends on how
predictable the task is and whether private data or real-world actions are
involved.

A **plain chatbot** is the right choice when the task is purely
conversational or knowledge-based, and does not require touching any
private or external data — answering general questions, explaining a
concept, drafting or rewording text, or brainstorming, where everything
the model needs is either general knowledge or supplied directly in the
conversation. As soon as the task requires looking something up in a private
file, taking an action in the outside world, or being repeated identically
many times, a plain chatbot stops being sufficient because it has no way to
reach outside the conversation.

A **rule-based workflow** is the right choice when the task is well-defined,
repetitive, and unlikely to change — situations where every possible input
and the exact response to it can be enumerated in advance, such as
validating a form, generating a fixed monthly report, routing a support
ticket based on a keyword, or enforcing a simple approve/reject rule.
Workflows are cheap, fast, fully deterministic, and easy to test and audit,
which makes them the better engineering choice whenever flexibility isn't
actually needed — using an LLM-driven agent for a task this narrow is
usually unnecessary overhead.

An **AI agent** is the right choice when the task is open-ended,
multi-step, or unpredictable in advance, and especially when it requires
combining private data access with reasoning about what to do next based on
intermediate results — for example, answering varied natural-language
questions about personal records, planning a sequence of actions across
multiple tools or systems, or handling requests that don't fit into a fixed
set of pre-written branches. The trade-off is that agents are more
computationally expensive, slower, and less strictly predictable than a
workflow, so they are best reserved for problems where that flexibility is
actually needed rather than applied by default to every task.
