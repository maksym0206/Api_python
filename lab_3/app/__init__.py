from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass

migrate = Migrate()
db = SQLAlchemy(model_class=Base)

def create_app(config_name="../config"):

    app = Flask(__name__)
    app.config.from_pyfile(config_name)

    db.init_app(app)
    migrate.init_app(app, db)

    from .routes import main
    app.register_blueprint(main)

    return app

