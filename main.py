import uvicorn
from dotenv import load_dotenv
import os

load_dotenv()

host = os.getenv("HOST", "0.0.0.0")
port = int(os.getenv("PORT", "8002"))

if __name__ == "__main__":
    uvicorn.run("src.app:app", host=host, port=port, reload=True)