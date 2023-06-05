# manage.py


import os
# import unittest
# import coverage
from flask.cli import AppGroup

from project import app, db
from project.models.user import User


manager_cli = AppGroup('manager')


@manager_cli.command('create_db')
def create_db():
    """Creates the db tables."""
    db.create_all()


@manager_cli.command('drop_db')
def drop_db():
    """Drops the db tables."""
    db.drop_all()


@manager_cli.command('create_master')
def create_admin():
    """Creates a master user."""
    db.session.add(
        User(
            email=os.environ['MASTER_MAIL'],
            password=os.environ['MASTER_PASSWORD'],
            admin=True,
            master=True)
    )
    db.session.commit()


app.cli.add_command(manager_cli)