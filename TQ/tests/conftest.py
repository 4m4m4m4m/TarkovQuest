import pytest
import TQ as tq

@pytest.fixture
def TQ():
    tq.config.update({
        "TESTING": True,
    })
    yield tq

@pytest.fixture
def client(TQ):
    return TQ.test_client()

@pytest.fixture
def runner(TQ):
    return TQ.test_cli_runner()