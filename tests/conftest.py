import sys
from pathlib import Path
from flask_login import FlaskLoginClient
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent.resolve()))
from TQapp.TQ import TQ
from TQapp.TQ import User
from TQapp.config import TestConfig



@pytest.fixture()
def app():
    app = TQ
    app.config.from_object(TestConfig)
    

    # other setup can go here

    yield app

    # clean up / reset resources here



@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def authenticated_client(app):
    app.test_client_class = FlaskLoginClient
    user = User()
    user.id = 1
    return app.test_client(user=user)

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()