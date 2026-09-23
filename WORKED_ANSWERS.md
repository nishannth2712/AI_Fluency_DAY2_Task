# Worked Answers (for you to check the model's output against)

Menu: Pizza = Rs. 250, Pasta = Rs. 200, Burger = Rs. 150, Drink = Rs. 50,
Salad = Rs. 120, Dessert = Rs. 100.

## ReAct question (react_trace.py)
"Which is cheaper: 2 Pizzas and a Drink with a 15% delivery discount, or
3 Pizzas with a 25% bulk discount? By how much?"

- Option 1: (250×2 + 50) × 0.85 = 550 × 0.85 = **Rs. 467.50**
- Option 2: (250×3) × 0.75 = 750 × 0.75 = **Rs. 562.50**
- **Answer: Option 1 is cheaper, by Rs. 95.00**

## CoT Question 1 — proportional bill split
Aman = 300, Bala = 200, Chitra = 250 → total = 750
After 10% discount: 750 × 0.9 = 675
- Aman: 300/750 × 675 = **Rs. 270**
- Bala: 200/750 × 675 = **Rs. 180**
- Chitra: 250/750 × 675 = **Rs. 225**
(Check: 270+180+225 = 675 ✓)

## CoT Question 2 — tip + even split
840 × 1.18 = 991.2
991.2 / 4 = **Rs. 247.80 per person**

## CoT Question 3 — logic / seating
Clockwise order: Meera, Kabir, Arjun, Divya (Meera opposite Arjun;
Kabir immediately right of Meera; Divya immediately left of Meera).
**Divya sits to the immediate right of Arjun.**

## CoT Question 4 — the "trap" question (needs the menu tool)
"What is the price of the Pasta on the restaurant menu, and how much
would two servings of it cost?"
- Correct: Pasta = Rs. 200, so 2 servings = **Rs. 400**
- A direct-prompt or CoT-only model has never seen the menu, so it
  will guess a plausible-sounding price and get this wrong (or get it
  right by luck) — that's the point of this question. Only the ReAct
  agent can get this reliably correct, because it calls get_menu_price.
