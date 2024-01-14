from flask import Blueprint, request
from ..models.user import User
from ..models.todo import Todo
from ..models.db import db

bp = Blueprint("todos", __name__, url_prefix="/todos")
