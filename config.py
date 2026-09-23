"""
Day 2 config — Restaurant Assistant project.

Reuses whichever LLM option you set up on Day 1 (Ollama, Groq, or Hugging Face).
Set LLM_OPTION in your .env file, or just edit the default below.
"""
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

OPTION = os.getenv("LLM_OPTION", "groq")  # "ollama", "groq", or "huggingface"

if OPTION == "ollama":
    client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
    MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:1.5b")

elif OPTION == "groq":
    client = OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=os.getenv("GROQ_API_KEY"),
    )
    # Hardcode a primary production model ID
    MODEL = os.getenv("GROQ_MODEL") or "openai/gpt-oss-120b"

elif OPTION == "huggingface":
    client = OpenAI(
        base_url="https://router.huggingface.co/v1",  # Updated from api-inference
        api_key=os.getenv("HF_API_KEY"),
    )
    MODEL = os.getenv("HF_MODEL", "meta-llama/Llama-3.2-3B-Instruct")
else:
    raise ValueError(f"Unknown LLM_OPTION: {OPTION}")


def banner(title: str):
    print("=" * 72)
    print(title.center(72))
    print("=" * 72)
