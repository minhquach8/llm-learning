import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

gemini_api_key = os.environ["GEMINI_API_KEY"]

client = genai.Client(
    api_key=gemini_api_key
)

response = client.models.generate_content(
    model="gemini-2.5-flash", contents="Hello, can you introduce yourself?"
)

print(response.text)