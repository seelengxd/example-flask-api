from flask import Flask

from .models.db import db, add_db_setup_commands


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SQLALCHEMY_DATABASE_URI="postgresql+psycopg2://postgres:postgres@localhost:5432/todos")

    db.init_app(app)
    add_db_setup_commands(app)
    return app
