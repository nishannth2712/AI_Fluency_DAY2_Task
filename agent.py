"""Day 2 ReAct agent — Restaurant Assistant scenario.

Cycles Thought -> Action -> Observation by letting the model call tools
(get_menu_price, calculator) until it has enough information to answer.
"""
import json
from config import client, MODEL
from tools import get_menu_price, calculator, TOOLS_SCHEMA

AVAILABLE_FUNCTIONS = {
    "get_menu_price": get_menu_price,
    "calculator": calculator,
}

SYSTEM_PROMPT = (
    "You are a restaurant billing assistant. "
    "You must use the get_menu_price tool to find any dish price — never guess a price. "
    "You must use the calculator tool for any arithmetic — never compute in your head. "
    "Think step by step, call one tool at a time, and give a final answer only once "
    "you have all the numbers you need."
)


def agent(question: str, max_steps: int = 8, verbose: bool = True):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question},
    ]

    for step in range(1, max_steps + 1):
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS_SCHEMA,
            temperature=0,
        )
        msg = response.choices[0].message

        # No tool call means the model believes it can answer now.
        if not msg.tool_calls:
            return msg.content

        messages.append(msg)
        for call in msg.tool_calls:
            fn_name = call.function.name
            args = json.loads(call.function.arguments)
            fn = AVAILABLE_FUNCTIONS.get(fn_name)
            result = fn(**args) if fn else f"Error: unknown tool {fn_name}"

            if verbose:
                print(f"step {step}: {fn_name}({args}) -> {result}")

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": call.id,
                    "name": fn_name,
                    "content": str(result),
                }
            )

    return "Stopped: maximum steps reached."
