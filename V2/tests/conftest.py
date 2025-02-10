from .docker_utils import start_database_container
from .test_db import get_session
import pytest

@pytest.fixture(scope='session')
def docker_container():
    """start the Docker container"""
    container = start_database_container()
    yield container
    container.stop()
    container.remove()

@pytest.fixture(scope='session')
def db_session(docker_container):
    """database session that persists for the entire test session"""
    session = get_session()
    yield session
    session.close()

@pytest.fixture(autouse=True)
def cleanup_database(db_session):
    """clean up the database after each test"""
    yield
    db_session.rollback()
