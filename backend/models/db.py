from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
import click

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

def add_db_setup_commands(app: Flask):
    def init_db():
        from . import user, todo
        with app.app_context():
            db.create_all()

    @app.cli.command("init-db")
    def init_db_command():
        init_db()
        click.echo("Initialised the database.")
