from fastapi import Body, FastAPI
from ollama import Client

app = FastAPI()
client = Client(
    host="http://localhost:11434"
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/chat")
def chat(
    message: str = Body(..., description="The Message") 
):
    response = client.chat(model="gemma3:1b", messages=[
        { "role": "user", "content": message}
    ])
    
    return { "resposne": response.message.content}