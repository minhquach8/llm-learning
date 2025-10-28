import json
import os

from dotenv import load_dotenv
from mem0 import Memory
from openai import OpenAI

load_dotenv()

OPEN_API_KEY = os.getenv("OPENAI_API_KEY")

NEO_CONNECTION_URI = os.getenv("NEO_CONNECTION_URI")
NEO_USERNAME = os.getenv("NEO_USERNAME")
NEO_PASSWORD = os.getenv("NEO_PASSWORD")

client = OpenAI(api_key=OPEN_API_KEY)

config = {
    "version": "v1.1",
    "embedder": {
        "provider": "openai",
        "config": { "api_key": OPEN_API_KEY, "model": "text-embedding-3-small"}
    },
    "llm": {
        "provider": "openai",
        "config": { "api_key": OPEN_API_KEY, "model": "gpt-4.1" }
    },
    "graph_store":{
        "provider": "neo4j",
        "config": {
            "url": NEO_CONNECTION_URI,
            "username": NEO_USERNAME,
            "password": NEO_PASSWORD
        }  
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "host": "localhost",
            "port": 6333
        }
    }
}

mem_client = Memory.from_config(config)

while True:
    user_query = input("> Input: ")

    search_memory = mem_client.search(query=user_query, user_id="ashuxie")

    memories = [
        f"ID: {mem.get("id")}\nMemory: {mem.get("memory")}" for mem in search_memory.get("results")
    ]
    
    print("> Memories: ", memories)

    SYSTEM_PROMPT = f"""
        Here is the context about the user:
        {json.dumps(memories)}
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_query}
        ]
    )

    ai_response = response.choices[0].message.content

    print("> AI Output: ", ai_response)

    mem_client.add(
        user_id="ashuxie",
        messages=[
            {"role": "user", "content": user_query},
            {"role":"assistant", "content": ai_response}
        ]
    )

    print("Memory has been saved!")