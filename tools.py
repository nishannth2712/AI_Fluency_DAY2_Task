"""Day 2 tools for the Restaurant Assistant scenario.

The agent knows NOTHING about menu prices until it calls get_menu_price.
It must never do arithmetic in its head — it must call calculator.
"""

MENU = {
    "pizza": 250,
    "pasta": 200,
    "burger": 150,
    "drink": 50,
    "salad": 120,
    "dessert": 100,
}


def get_course_menu():
    """Not used by the agent directly — handy for printing the menu to humans."""
    return MENU


def get_menu_price(dish_name: str):
    """Return the price (Rs.) of a dish from the restaurant menu."""
    key = dish_name.strip().lower()
    if key not in MENU:
        return f"Error: '{dish_name}' is not on the menu."
    return MENU[key]


def calculator(expression: str):
    """Safely evaluate a basic arithmetic expression and return the numeric result."""
    allowed = set("0123456789+-*/(). ")
    if not set(expression) <= allowed:
        return "Error: expression contains disallowed characters."
    try:
        return eval(expression, {"__builtins__": {}}, {})
    except Exception as e:
        return f"Error: {e}"


# OpenAI-style tool schema, used by agent.py for function calling.
TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "get_menu_price",
            "description": "Get the price (in Rs.) of a dish from the restaurant menu.",
            "parameters": {
                "type": "object",
                "properties": {
                    "dish_name": {
                        "type": "string",
                        "description": "Name of the dish, e.g. 'Pizza' or 'Pasta'",
                    }
                },
                "required": ["dish_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Evaluate an arithmetic expression and return the numeric result.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "e.g. '(250*2+50)*0.85'",
                    }
                },
                "required": ["expression"],
            },
        },
    },
]
