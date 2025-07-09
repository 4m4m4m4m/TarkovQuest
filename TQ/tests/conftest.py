import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.resolve()))
from TQ import TQ

@pytest.fixture()
def app():
    app = TQ
    app.config.update({
        "TESTING": True,
    })
    

    # other setup can go here

    yield app

    # clean up / reset resources here

@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()