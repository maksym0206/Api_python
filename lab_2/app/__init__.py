from fastapi import FastAPI
from .routes import main

def create_app():

    app = FastAPI()
    app.include_router(main, prefix="/books", tags=["main"])

    return app

app = create_app()