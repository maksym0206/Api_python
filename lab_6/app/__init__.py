from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flasgger import Swagger  
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass

migrate = Migrate()
db = SQLAlchemy(model_class=Base)

def create_app(config_name="../config"):

    app = Flask(__name__)
    app.config.from_pyfile(config_name)

    api = Api(app)
    swager = Swagger(app)

    from .routes import BookListResource, BookResource
    api.add_resource(BookListResource, "/books", endpoint="books")
    api.add_resource(BookResource, "/books/<int:book_id>", endpoint="book")

    db.init_app(app)
    migrate.init_app(app, db)

    from .routes import main
    app.register_blueprint(main)

    return app

