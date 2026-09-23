Reasoning and Acting: Direct Prompting, Chain-of-Thought, and ReAct on a Restaurant Assistant
1. Scenario
I chose a restaurant billing assistant as my scenario. The assistant helps
a customer or waiter work out bills, discounts, splits and tips for a small
fixed menu (Pizza, Pasta, Burger, Drink, Salad, Dessert). This scenario has:

One tool-requiring question: comparing the cost of two discount offers,
which needs the actual menu prices (private data the model cannot know on
its own) plus arithmetic.
Several reasoning-only questions: proportional bill-splitting, a
tip-and-split calculation, and a seating-order logic puzzle — all of which
give every number needed in the question itself.
A fourth "trap" question ("what is the price of the Pasta?") that looks
answerable but actually requires the menu tool — included specifically to
expose where Chain-of-Thought reasoning breaks down.

2. Explanation of each approach
2.1 Direct prompting
Direct prompting sends the user's question straight to the model and asks
for only the final answer, with the instruction "give only the final answer,
do not explain." It answers immediately from a single forward pass, with no
visible intermediate reasoning and no ability to call a tool. In my run,
direct prompting actually reached the correct final number on all three
reasoning-only questions (Rs. 270/180/225 split, Rs. 247.80 tip split, and
"Divya" for the seating puzzle) — for a model of this size, this is not
guaranteed, and on harder or longer multi-step problems this approach is far
more likely to silently drop a step. On the tool-requiring pricing question,
direct prompting has no access to the real menu at all. Tellingly, when
asked the "trap" question directly (Q4, price of the Pasta), the model did
not hallucinate a price — it correctly said it did not have the menu
information and asked the user to supply it. This is a safer failure mode
than guessing, but it still means direct prompting cannot complete the task
on its own: it produces no usable final answer for a question that requires
outside data.

2.2 Chain-of-Thought (CoT)
Chain-of-Thought prompting asks the model to "solve the problem step by
step" and number each step before giving a final answer. On my three
reasoning-only questions, CoT reached the same correct final answers as
direct prompting, but with a crucial difference: it showed its full working
(e.g., for Q1 it computed each person's pre-discount total, the combined
bill, the discount amount, the post-discount total, and each person's
proportional share — and even added a verification step confirming
270+180+225=675). This transparency is valuable even when the final number
matches direct prompting, because it lets a human check how the answer was
reached, not just what it was. On the seating puzzle (Q3), CoT explicitly
assigned table positions (seat 1-4) before answering, making the logic
auditable in a way the one-line direct answer was not.
On the trap question (Q4), CoT behaved the same way direct prompting did —
it declined to guess and asked for the menu price. This confirms the
theoretical point cleanly: CoT improves how carefully the model reasons
over information it has, but it does not give the model any new information.
No number of reasoning steps could produce the real Pasta price, because
that fact was never in the prompt.

2.3 ReAct agent
The ReAct agent cycles through Thought, Action (call
get_menu_price or calculator), and Observation, repeating until it
can give a Final Answer. On the discount-comparison question, my agent's
actual trace was:

step 1: get_menu_price({'dish_name': 'Pizza'}) -> 250
step 2: get_menu_price({'dish_name': 'Drink'}) -> 50
step 3: calculator({'expression': '(2*250+50)*0.85'}) -> 467.5
step 4: calculator({'expression': '(3*250)*0.75'}) -> 562.5
step 5: calculator({'expression': '562.5-467.5'}) -> 95.0
FINAL ANSWER: the 2 Pizzas + Drink order (Rs. 467.5) is cheaper than
the 3 Pizzas order (Rs. 562.5), by Rs. 95.

This matches the correct worked answer exactly. Unlike CoT, every number in
this trace came from a real tool call rather than the model's own
parameters — two menu lookups and three calculator calls, five LLM round
trips in total. This is the key advantage ReAct has over CoT on this
scenario: it could have correctly answered the Q4 trap question too (by
simply calling get_menu_price('Pasta')), whereas neither direct prompting
nor CoT could, no matter how they reasoned.

3. Comparison table




Basis for comparison

Direct prompting

Chain-of-Thought

ReAct agent





Reasoning depth

None shown — single final line only

Full step-by-step breakdown, including a self-check step (Q1)

Explicit Thought/Action/Observation trace, each step grounded in a tool result



Tool usage

None — cannot access the menu at all

None — same limitation as direct prompting

2 menu lookups + 3 calculator calls used to answer the discount question



Reliability on multi-step questions

Correct on all 3 reasoning Qs in this run, but no way to verify without re-deriving it yourself

Correct on all 3, and self-verifying (Q1 explicitly checked the totals summed correctly)

Correct on the tool-requiring question, verified by construction since every number came from a tool call, not a guess



Transparency (can you see how it got the answer?)

No — just the final number

Yes — full numbered working shown

Yes — full trace of tool calls and results shown



Speed / cost

Fastest — 1 LLM call per question

Slower — more output tokens per question, still 1 LLM call

Slowest / most expensive — 5 LLM calls for one question (one per tool round-trip)



Consistency across repeated runs

Not tested with multiple runs here

Not tested with multiple runs here

See self-consistency section below — content was identical across 5 runs, though not at temperature 0



4. Self-consistency observation
Question used: Q1, the proportional bill-splitting question (Aman/Bala/
Chitra), run 5 times at temperature 0.8 via self_consistency.py.





Item

Value





Answers seen across the 5 runs

All 5 runs computed the same numbers (Aman Rs. 270, Bala Rs. 180, Chitra Rs. 225), but with different surface formatting: run 1 "** Aman pays Rs. 270...", run 2 "Aman pays Rs. 270...", run 3 "Aman = 270, Bala = 180, Chitra = 225.", runs 4-5 "** Aman pays ₹270..." (₹ symbol instead of "Rs.")



Majority answer

The script reported "Majority answer (2 of 5 runs)" for the exact string "** Aman pays ₹270, Bala pays ₹180, and Chitra pays ₹225."



Was the majority answer correct?

Yes — Rs. 270 / Rs. 180 / Rs. 225 is the mathematically correct split



Result when temperature = 0

Not run in this session, but expected: all 5 runs should produce near-identical wording as well as identical numbers, since temperature 0 removes sampling randomness



Observation: the content of all 5 runs was fully consistent — every
run reached the correct numbers. However, the majority-vote count (2 of 5)
undercounted this consistency, because the vote is based on exact string
matching of the final-answer line, and the model varied cosmetic details
(the "**" markdown bolding, and "Rs." vs "₹" as the currency symbol) even
though the underlying answer never changed. This is a useful finding in its
own right: self-consistency voting is only as good as how the final answer
is normalized before comparison — a stricter check (e.g., extracting just
the three numbers) would have shown 5/5 agreement instead of 2/5.

5. Suitability analysis
For this restaurant billing scenario, ReAct is the most suitable approach
for the task as a whole, because the core of the scenario — checking real
menu prices before doing discount arithmetic — is exactly the case where
direct prompting and CoT are structurally unable to help: both approaches
correctly refused to guess the Pasta price in Q4 rather than hallucinate,
but a refusal is still not a usable answer. Only ReAct could actually
complete that part of the task, by fetching the real price with
get_menu_price.
That said, CoT is the better choice for the reasoning-only sub-tasks (the
bill split, the tip split, the seating puzzle): it reached the same correct
answers as direct prompting in this run, but with visible, checkable working
and no extra tool-call cost, whereas ReAct would have added unnecessary
latency for numbers that were already given in the question. Direct
prompting is adequate only for one-shot answers, and even where it happened
to be correct here, it gives a human no way to catch an error without
re-deriving the answer themselves. Given this, the ideal real-world design
is not "pick one" but a router: use CoT (or nothing) for pure reasoning, and
fall into a ReAct loop the moment a question depends on real, external data.

6. Conclusion
More generally, the three approaches suit different kinds of problems.
Direct prompting is appropriate when a question is simple, well within
the model's own knowledge, and speed matters more than transparency or
verifiability. Chain-of-Thought is appropriate when a problem requires
multi-step reasoning over information that is already fully contained in
the prompt — my results show it adds transparency and a self-check even when
direct prompting happens to land on the right answer, which matters once
problems get harder than the ones tested here. ReAct is necessary
whenever a problem depends on information the model does not and cannot
already know — current prices, database records, live data — and it is
worth the extra latency and cost precisely because, as my Q4 trap question
showed, a well-behaved model will correctly refuse to guess rather than
hallucinate, meaning CoT and direct prompting simply cannot finish the task
at all in that case. Self-consistency, meanwhile, is a useful cross-check on
CoT specifically — but my results show it is only as reliable as the method
used to compare final answers, since cosmetic differences in wording can
make genuinely consistent answers look inconsistent under naive string
matching.
