from fastapi import FastAPI

def create_app():

    app = FastAPI()
    from .books.books_routes import main
    app.include_router(main, prefix="/books", tags=["main"])
    from .auth.auth_routes import auth_router
    app.include_router(auth_router, prefix="/user")

    return app

app = create_app()