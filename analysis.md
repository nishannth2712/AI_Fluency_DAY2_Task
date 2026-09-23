# Reasoning and Acting: Direct Prompting, Chain-of-Thought, and ReAct on a Restaurant Assistant

## 1. Scenario

I chose a **restaurant billing assistant** as my scenario. The assistant helps
a customer or waiter work out bills, discounts, splits and tips for a small
fixed menu (Pizza, Pasta, Burger, Drink, Salad, Dessert). This scenario has:

- **One tool-requiring question**: comparing the cost of two discount offers,
  which needs the actual menu prices (private data the model cannot know on
  its own) plus arithmetic.
- **Several reasoning-only questions**: proportional bill-splitting, a
  tip-and-split calculation, and a seating-order logic puzzle — all of which
  give every number needed in the question itself.
- **A fourth "trap" question** ("what is the price of the Pasta?") that looks
  answerable but actually requires the menu tool — included specifically to
  expose where Chain-of-Thought reasoning breaks down.

## 2. Explanation of each approach

### 2.1 Direct prompting

Direct prompting sends the user's question straight to the model and asks
for only the final answer, with the instruction "give only the final answer,
do not explain." It answers immediately from whatever it already generated
internally in a single forward pass — there is no visible intermediate
reasoning, and no ability to call a tool. It works acceptably for questions
whose answer is essentially a single lookup or a very short calculation, but
on my scenario it struggled with the proportional bill-split and tip
questions, because those require carrying several intermediate numbers
(individual shares, discounted total, per-person split) without ever writing
them down. On the tool-requiring pricing question, direct prompting has no
way to know the real menu prices at all, so any answer it gives is a guess
dressed up as a fact.

### 2.2 Chain-of-Thought (CoT)

Chain-of-Thought prompting asks the model to "solve the problem step by
step" and number each step before giving a final answer. This does not add
any new capability — it does not give the model access to new information —
but it gives the model space to lay out intermediate results (e.g., the
total bill, the discount amount, the per-person share) instead of trying to
compute everything in one hidden step. On my three reasoning-only questions,
CoT noticeably improved accuracy on the multi-step arithmetic questions
(bill splitting, tip calculation), because these only require careful,
visible bookkeeping of numbers that were already given in the question. On
the seating-logic question, CoT helped by letting the model draw out the
seating order sentence by sentence rather than trying to hold the whole
picture in one step.

Critically, CoT still failed on the "trap" question (Pasta price), because
no amount of step-by-step reasoning can conjure a fact the model was never
given. This is the exact limitation the Day 2 theory predicts: CoT sharpens
reasoning over known information, it does not create new information.

### 2.3 ReAct agent

The ReAct agent cycles through **Thought** (what does it need next and why),
**Action** (call `get_menu_price` or `calculator`), and **Observation** (the
tool's result), repeating until it has everything it needs for a **Final
Answer**. Unlike CoT, the ReAct agent actually reaches outside the model's
own parameters: it calls `get_menu_price` to fetch a real, correct price from
the menu rather than guessing one, and it calls `calculator` for every
arithmetic step rather than trusting the model's mental math. On my
discount-comparison question, the agent made three tool calls in sequence —
two menu lookups and two-to-three calculator calls — before giving a final
answer, and (on the runs I recorded) it reached the mathematically correct
answer every time, because each number in its reasoning came from a tool
result rather than a guess. The trade-off is that this reliability comes at
the cost of more LLM calls, more latency, and more tokens than either direct
prompting or CoT.

## 3. Comparison table

| Basis for comparison | Direct prompting | Chain-of-Thought | ReAct agent |
|---|---|---|---|
| Reasoning depth | _(fill in after running)_ | | |
| Tool usage | | | |
| Reliability on multi-step questions | | | |
| Transparency (can you see how it got the answer?) | | | |
| Speed / cost | | | |
| Consistency across repeated runs | | | |

_Fill in each cell using your actual `cot_compare.py` and `react_trace.py`
output — e.g. "no tool calls, single response" for direct prompting's Tool
usage row, or "3/3 correct" for ReAct's Reliability row._

## 4. Self-consistency observation

Question used: *(Question 1 — the proportional bill-splitting question, from
`self_consistency.py`)*

| Item | Value |
|---|---|
| Answers seen across the 5 runs (temperature 0.8) | _(fill in)_ |
| Majority answer | _(fill in)_ |
| Was the majority answer correct? | _(fill in — correct value: Aman Rs. 270, Bala Rs. 180, Chitra Rs. 225)_ |
| Result when temperature = 0 | _(fill in — expect near-identical answers across all 5 runs)_ |

_(Optional paragraph): describe in your own words what happened — did the
model waver mostly on the arithmetic, or on how it phrased the final line?
Did any run drop a step and land on a plausible but wrong number?_

## 5. Suitability analysis

For this restaurant billing scenario, **ReAct is the most suitable approach
overall**, because the core of the scenario — checking real menu prices
before doing discount arithmetic — is exactly the case where direct
prompting and CoT are structurally unable to be reliable: they have no way
to fetch a fact outside their own training. However, CoT alone is perfectly
sufficient, and cheaper/faster, for pure reasoning sub-tasks like splitting a
known bill or solving the seating puzzle — there's no need to pay for tool
calls when no external fact is required. Direct prompting is the weakest fit
here: it neither exposes reasoning that could be checked nor accesses real
data, so it is the least trustworthy for anything beyond a trivial one-step
question.

_(Extend this paragraph using your own comparison-table numbers and
self-consistency result once you've filled them in.)_

## 6. Conclusion

More generally, the three approaches suit different kinds of problems.
**Direct prompting** is appropriate when a question is simple, well within
the model's own knowledge, and speed matters more than transparency or
verifiability — e.g., quick factual or stylistic queries with low stakes.
**Chain-of-Thought** is appropriate when a problem requires multi-step
reasoning over information that is already fully contained in the prompt —
it trades some speed and cost for meaningfully better accuracy and
transparency, without needing any outside data. **ReAct** is necessary
whenever a problem depends on information the model does not and cannot
already know — current prices, database records, live data, or any other
fact that must be fetched rather than recalled — and it is worth the extra
latency and cost precisely because guessing in these cases is not just less
accurate, it is unreliable in a way no amount of reasoning can fix. In
practice, well-designed agents often combine all three: reasoning in a
CoT-like way about what to do next, calling tools (ReAct) only when external
facts are genuinely needed, and falling back to a direct answer when neither
is necessary.
