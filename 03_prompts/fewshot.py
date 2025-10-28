import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
gemini_api_key = os.environ["GEMINI_API_KEY"]

client = OpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Few shot prompting is when you give the model some examples of what you want it to do.
SYSTEM_PROMPT = """
You are an expert in programming. You are here to help me explain and write code in any programming languages. Anything besides programming topic, you should not answer and reply sorry.

Examples:
Q: What is Python?
A: Python is a high-level, interpreted, object-oriented programming language. It's known for its readability, versatility, and large community.

Q: Who are you?
A: Sorry, I'm an expert in Python programming. I'm here to help you explain and write code in Python.
"""

USER_PROMPT = input("Your prompt: ")

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        { "role": "system", "content": SYSTEM_PROMPT },
        {"role": "user", "content": USER_PROMPT},
    ]
)

filename = "output.md"
with open(filename, "w", encoding="utf-8") as file:
    file.write(response.choices[0].message.content)
print(f"Output saved to {filename}")
print("=" * 50)
print(response.choices[0].message.content)