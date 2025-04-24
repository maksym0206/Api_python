from app import app
import uvicorn
from config import Config

if __name__ == "__main__":
    uvicorn.run(app, host=Config.HOST, port=Config.PORT, reload=True)