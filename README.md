# Restaurant Assistant — Direct Prompting vs. Chain-of-Thought vs. ReAct

Scenario: a restaurant billing assistant that can look up menu prices and do
arithmetic, used to compare three approaches to reasoning/acting with an LLM.

## Setup

```bash
# from inside this folder (reuse your Day 1 .venv if you have it)
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# edit .env: set LLM_OPTION and the matching model/API key
```

Make sure whichever backend you chose is ready:
- **Ollama**: `ollama serve` running locally, model pulled (`ollama pull qwen2.5:1.5b`)
- **Groq**: `GROQ_API_KEY` set in `.env`
- **Hugging Face**: `HF_API_KEY` set in `.env`

## Files

| File | Purpose |
|---|---|
| `tools.py` | `get_menu_price`, `calculator`, and the tool schema |
| `agent.py` | The ReAct agent loop (Thought → Action → Observation) |
| `react_trace.py` | Runs the agent on the tool-requiring question, prints its trace |
| `cot_compare.py` | Runs 4 reasoning questions with and without Chain-of-Thought |
| `self_consistency.py` | Runs one CoT question 5× at temperature 0.8, takes majority vote |
| `PAPER_TRACE_WORKSHEET.md` | Fill this in by hand *before* running `react_trace.py` |
| `WORKED_ANSWERS.md` | Correct answers, to check the model's output against |
| `analysis.md` | The written analysis to submit (see Day 2 Task) |
| `screenshots/` | Put your terminal output screenshots here |

## Run order

```bash
# 1. Fill in PAPER_TRACE_WORKSHEET.md by hand first (no computer)

# 2. Run the ReAct agent and compare to your paper trace
python react_trace.py

# 3. Compare direct vs. Chain-of-Thought answers
python cot_compare.py

# 4. Run self-consistency (majority voting)
python self_consistency.py
```

Take a screenshot of each run's terminal output and save it in `screenshots/`.
Then fill in `analysis.md` with your actual results (the comparison table,
self-consistency numbers, and your conclusions) and push everything to GitHub.
