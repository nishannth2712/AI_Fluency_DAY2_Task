# Paper ReAct Trace — Restaurant Assistant

Do this by hand, before running `react_trace.py`. You may use only two tools:
`get_menu_price(dish_name)` and `calculator(expression)`. Write an observation
only when you "call" a tool — no arithmetic in your head.

**Question:** Which is cheaper: 2 Pizzas and a Drink with a 15% delivery
discount, or 3 Pizzas with a 25% bulk discount? By how much?

| Step | Type | Content | Why this step |
|---|---|---|---|
| 1 | Thought | | |
| 2 | Action | | |
| 3 | Observation | | |
| 4 | Thought | | |
| 5 | Action | | |
| 6 | Observation | | |
| 7 | Thought | | |
| 8 | Action | | |
| 9 | Observation | | |
| 10 | Final Answer | | |

Questions to answer below your trace:
- How many tool calls did you need?
- How many LLM calls would that be in real life?
- Could any two actions have been done in parallel?

## Comparison: paper trace vs. agent trace

| Item | Your paper trace | The agent |
|---|---|---|
| Number of price lookups | | |
| Number of calculator calls | | |
| Total steps | | |
| Any tools called in parallel? (Y/N) | | |
| Final answer | | |
| Correct? (Y/N) | | |
