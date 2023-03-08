from flask import Flask
from db.models.history import History
from db.db import db
import config

def create_app():
    app = Flask(__name__)
    app.config.from_prefixed_env()
    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    create_app()