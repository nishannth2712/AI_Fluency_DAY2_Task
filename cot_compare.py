"""Part C: the same reasoning-only questions asked WITHOUT and WITH Chain-of-Thought.

These four questions need no tools — the numbers are all given in the question,
EXCEPT question 4, which is deliberately included to show that CoT alone
still cannot fetch a fact it doesn't have (that's what ReAct is for).
"""
from config import client, MODEL, banner

QUESTIONS = [
    # 1. Multi-step arithmetic: proportional bill splitting
    "Three friends dine together. Aman orders a Pizza (Rs. 250) and a Drink (Rs. 50), "
    "Bala orders a Pasta (Rs. 200), and Chitra orders a Burger (Rs. 150) and a "
    "Dessert (Rs. 100). They get a flat 10% discount on the total bill, split "
    "proportionally to what each person ordered. How much does each person pay?",
    # 2. Multi-step arithmetic: tip + even split
    "A group's restaurant bill comes to Rs. 840 after tax. They want to leave an "
    "18% tip and then split the total evenly among 4 people. How much does each "
    "person pay?",
    # 3. Ordering / logic
    "Four friends are seated at a round table for dinner. Meera sits opposite Arjun. "
    "Kabir sits to the immediate right of Meera. Divya sits to the immediate left of "
    "Meera. Who sits to the immediate right of Arjun?",
    # 4. Requires private/tool data — CoT will hallucinate this one on purpose
    "What is the price of the Pasta on the restaurant menu, and how much would two "
    "servings of it cost?",
]

DIRECT_PROMPT = "You are a helpful assistant. Give only the final answer. Do not explain."

COT_PROMPT = (
    "You are a helpful assistant. Solve the problem step by step. "
    "Number each step and show the calculation in that step. "
    "After the steps, write the last line exactly as: Final Answer: <answer>"
)


def ask(system_prompt, question):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question},
        ],
        temperature=0,
    )
    return response.choices[0].message.content.strip()


if __name__ == "__main__":
    banner("CHAIN-OF-THOUGHT COMPARISON — RESTAURANT ASSISTANT")
    for number, question in enumerate(QUESTIONS, start=1):
        print("=" * 72)
        print(f"QUESTION {number}: {question}\n")
        print("--- WITHOUT CoT ---")
        print(ask(DIRECT_PROMPT, question), "\n")
        print("--- WITH CoT ---")
        print(ask(COT_PROMPT, question), "\n")
