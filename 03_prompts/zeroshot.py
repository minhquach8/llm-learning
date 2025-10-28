import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
gemini_api_key = os.environ["GEMINI_API_KEY"]

client = OpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Zero shot prompting is when you don't need to give the model any context.
SYSTEM_PROMPT = """You are an expert in Python programming. You are here to help me explain and write code in Python. Anything besides Python topic, you should not answer and reply sorry."""
USER_PROMPT = """Hi. I want to learn Python."""

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