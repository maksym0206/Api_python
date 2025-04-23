from flask import Flask
from .routes import main

def create_app(config_name="config"):
    app = Flask(__name__)
    app.config.from_pyfile(config_name)

    app.register_blueprint(main)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5050, host='0.0.0.0')