import sys
from pathlib import Path
from flask_login import FlaskLoginClient, UserMixin
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent.resolve()))
from TQapp.TQ import User
from TQapp import TQ

@pytest.fixture()
def app():
    app = TQ
    app.config.update({
        "TESTING": True,
        "WTF_CSRF_ENABLED": False
    })
    

    # other setup can go here

    yield app

    # clean up / reset resources here



@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def authenticated_client(app):
    app.test_client_class = FlaskLoginClient
    user = User("1","testuser")
    return app.test_client(user=user)

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()