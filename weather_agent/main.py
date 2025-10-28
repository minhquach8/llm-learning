import requests
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()


def get_weather(city: str):
    url = f'https://wttr.in/{city.lower()}?format=%C+%t'
    response = requests.get(url)

    if response.status_code == 200:
        return f'The weather in {city} is {response.text}'
    return f'Error: {response.status_code}'


def main():
    user_query = input('> Input: ')
    response = client.chat.completions.create(
        model='gpt-4o', messages=[{'role': 'user', 'content': user_query}]
    )

    print(f'> Output: {response.choices[0].message.content}')


print(get_weather('Paris'))
