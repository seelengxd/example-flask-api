from flask import Flask

from .models.db import db, add_db_setup_commands
from .blueprints import auth
from flask_restful import Api
from .blueprints.todos import TodoList, Todo


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI="postgresql+psycopg2://postgres:postgres@localhost:5432/todos")

    db.init_app(app)
    add_db_setup_commands(app)

    app.register_blueprint(auth.bp)

    api = Api(app)
    api.add_resource(TodoList, '/todos')
    api.add_resource(Todo, '/todos/<id>')

    return app
