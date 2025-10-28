import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
gemini_api_key = os.environ["GEMINI_API_KEY"]

client = OpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role": "user", "content": "Hi, who are you?"},
    ]
)

print(response.choices[0].message.content)