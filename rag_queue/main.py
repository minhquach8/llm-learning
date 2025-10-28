import uvicorn
from dotenv import load_dotenv

from .server import app

load_dotenv()

def main():
    uvicorn.run(app, port=8000, host='0.0.0.0')


main()
