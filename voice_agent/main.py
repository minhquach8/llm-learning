import asyncio

import speech_recognition as sr
from dotenv import load_dotenv
from openai import AsyncOpenAI, OpenAI
from openai.helpers import LocalAudioPlayer

load_dotenv()

client = OpenAI()
async_client = AsyncOpenAI()


async def tts(speech: str):
    async with async_client.audio.speech.with_streaming_response.create(
        model='gpt-4o-mini-tts',
        voice='coral',
        instructions='Always speak as if you try to lure the user into a conversation',
        input=speech,
        response_format='pcm',
    ) as response:
        await LocalAudioPlayer().play(response)


def main():
    r = sr.Recognizer()  # Speech to Text

    with sr.Microphone() as source:  # Mic Access
        r.adjust_for_ambient_noise(source)
        r.pause_threshol = 2

        SYSTEM_PROMPT = f"""
            You're an expert voice agent. You are given the transcript of what user has said using voice.
            You need to output as if you are a voice agent and whatever you  speak will be converted back to audio using AI and played back to user.
        """
        messages = [
            {'role': 'system', 'content': SYSTEM_PROMPT},
        ]

        while True:
            print('Listening...')
            audio = r.listen(source)

            print('Processing...(STT)')
            stt = r.recognize_google(audio)

            print('You said: ', stt)

            messages.append({'role': 'user', 'content': stt})

            response = client.chat.completions.create(
                model='gpt-4.1-mini',
                messages=messages
            )

            print('> Output: ', response.choices[0].message.content)
            asyncio.run(tts(response.choices[0].message.content))


main()
