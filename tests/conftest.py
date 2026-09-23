import os

import pytest


# Tell the application to use a separate database during testing.
os.environ['DATABASE_URL'] = 'sqlite:///test_todo.db'


from app import app
from models import db


@pytest.fixture(scope='session')
def test_app():
    app.config['TESTING'] = True

    with app.app_context():
        # Make sure no old SQLAlchemy session is holding
        # objects from a previous database state.
        db.session.remove()

        db.drop_all()
        db.create_all()

        yield app

        # Remove the session before destroying the tables.
        db.session.remove()

        db.drop_all()
        db.engine.dispose()


@pytest.fixture
def client(test_app):

    # Start each test with a completely clean database
    # and a completely clean SQLAlchemy session.
    with test_app.app_context():

        db.session.remove()

        db.drop_all()
        db.create_all()

    with test_app.test_client() as client:
        yield client

    # Clean the session before resetting the database
    # for the next test.
    with test_app.app_context():

        db.session.remove()

        db.drop_all()
        db.engine.dispose()