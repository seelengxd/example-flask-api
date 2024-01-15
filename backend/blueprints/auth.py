from flask import Blueprint, request, session, g, abort
from werkzeug.security import check_password_hash, generate_password_hash

from sqlalchemy import select
from ..models.user import User
from ..models.db import db
import psycopg2

import functools


bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=("POST",))
def register():
    username = request.json["username"]
    password = request.json["password"]

    try:
        new_user = User(username=username,
                        hashed_password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
    except psycopg2.errors.UniqueViolation:
        return {"errors": [
            {"msg": f"Username {username} is taken."}
        ]}

    return "OK"


@bp.route("/login", methods=("POST",))
def login():
    username = request.json["username"]
    password = request.json["password"]

    user = db.session.scalar(select(User).where(
        User.username == username))

    if not user:
        return {"errors": [
            {"msg": f"Username does not exist."}
        ]}
    if not check_password_hash(user.hashed_password, password):
        return {"errors": [
            {"msg": "Wrong password."}
        ]}

    session.clear()
    session["user_id"] = user.id
    return "OK"


@bp.route("/logout", methods=("POST",))
def logout():
    session.clear()
    return "OK"


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = db.session.scalar(select(User).where(
            User.id == user_id))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            abort(401)
        return view(*args, **kwargs)
    return wrapped_view


@bp.route("/me")
@login_required
def get_user_info():
    return g.user.as_dict()
