from docker_utils import start_docker_container
import pytest

@pytest.fixture(scope = 'session', autouse = True)
def db_session():
    container = start_docker_container()