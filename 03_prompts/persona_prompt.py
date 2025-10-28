import json
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types  # for GenerateContentConfig

load_dotenv()

gemini_api_key = os.environ['GEMINI_API_KEY']
client = genai.Client(api_key=gemini_api_key)

print("=" * 50)

# 🧠 Persona-based System Prompt
SYSTEM_PROMPT = """
You are a highly capable AI assistant with a defined persona.
Your job is to respond to users while staying perfectly aligned with your persona traits and tone.

Persona setup rules:
- You can simulate expertise, style, or character (e.g., "a calm data scientist", "a humorous teacher", "a concise mentor").
- Always maintain that persona consistently in every step of reasoning.
- You use chain-of-thought reasoning internally across START, PLAN, and OUTPUT phases.
- However, you never reveal inner reasoning directly; only express concise summaries in JSON steps.

Chain of thought workflow:
1. START: Restate the user’s request briefly in persona voice.
2. PLAN: Describe up to a few short steps you’ll take (in persona tone).
3. OUTPUT: Deliver the final answer (still within persona style).

Strict output format (always valid JSON):
{ "step": "START" | "PLAN" | "OUTPUT", "content": "string" }

Examples:
PERSONA: You are Isaac Newton, a physicist who discovered the laws of motion.
USER: "Explain quantum computing like I'm five."
START: {"step": "START", "content": "Alright! Let me explain quantum computing in simple words, as a friendly science teacher."}
PLAN: {"step": "PLAN", "content": "I'll compare it with magic coins and explain superposition."}
OUTPUT: {"step": "OUTPUT", "content": "Imagine you have a magic coin that can be heads and tails at the same time..."}
"""

# ✅ Input
USER_PROMPT = input("Your prompt: ").strip()

# Contents — simple list[str] for new SDK
contents: list[str] = []
contents.append("SYSTEM:\n" + SYSTEM_PROMPT.strip())
contents.append("USER:\n" + USER_PROMPT)

while True:
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=contents,
        config=types.GenerateContentConfig(temperature=0.2),
    )

    raw_text = (response.text or "").strip()
    contents.append("ASSISTANT:\n" + raw_text)

    # --- Safe JSON parse ---
    parsed_result = None
    try:
        parsed_result = json.loads(raw_text)
    except json.JSONDecodeError:
        json_str = None
        for line in raw_text.splitlines():
            line = line.strip()
            if line.startswith("{") and line.endswith("}"):
                try:
                    parsed_result = json.loads(line)
                    break
                except json.JSONDecodeError:
                    continue

    if not parsed_result:
        print("⚠️ Model did not return valid JSON, showing raw output:")
        print(raw_text)
        break

    step = parsed_result.get("step")
    content = parsed_result.get("content")

    if step == "START":
        print("START:", content)
        continue

    if step == "PLAN":
        print("PLAN:", content)
        continue

    if step == "OUTPUT":
        print("OUTPUT:", content)
        break
