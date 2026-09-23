"""Part B: print the agent's real ReAct trace for the restaurant scenario,
so it can be compared against a paper trace worked out by hand.
"""
from agent import agent

QUESTION = (
    "Which is cheaper: 2 Pizzas and a Drink with a 15% delivery discount, "
    "or 3 Pizzas with a 25% bulk discount? By how much?"
)

if __name__ == "__main__":
    print("QUESTION:", QUESTION, "\n")
    print("--- the agent's actions and observations ---")
    answer = agent(QUESTION, max_steps=8)
    print("\nFINAL ANSWER:", answer)
