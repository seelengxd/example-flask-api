from flask import g
from flask_restful import Resource, reqparse
from .auth import login_required

from typing import List
from sqlalchemy import select
from ..models.todo import Todo as ModelTodo
from ..models.db import db


form_parser = reqparse.RequestParser()
form_parser.add_argument("title", required=True, help="'title' missing")
form_parser.add_argument("description")
form_parser.add_argument("done", type=bool)


class TodoList(Resource):
    @login_required
    def get(self):
        todos: List[ModelTodo] = db.session.scalars(select(ModelTodo))
        return {"data": [todo.as_dict() for todo in todos]}

    @login_required
    def post(self):
        args = form_parser.parse_args()
        new_todo = ModelTodo(**args)
        new_todo.user = g.user
        db.session.add(new_todo)
        db.session.commit()
        return new_todo.as_dict()


class Todo(Resource):
    @login_required
    def put(self, id):
        todo = db.get_or_404(ModelTodo, id)
        data = form_parser.parse_args()
        todo.query.update(data)
        db.session.commit()

    @login_required
    def delete(self, id):
        todo = db.get_or_404(ModelTodo, id)
        db.session.delete(todo)
        db.session.commit()
