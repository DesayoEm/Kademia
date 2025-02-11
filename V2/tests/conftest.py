from ..tests.utils.docker_utils import start_database_container
from ..tests.utils.db_utils import migrate_to_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest
import os

@pytest.fixture(scope='session')
def docker_container():
    """start the Docker container"""
    container = start_database_container()
    yield container
    # container.stop()
    # container.remove()

@pytest.fixture(scope='session', autouse = True)
def db_session(docker_container):
    container = start_database_container()
    engine = create_engine(os.getenv('TEST_DB_URL'))
    SessionLocal = sessionmaker(autoflush=True, autocommit = False, bind=engine)
    session = SessionLocal()
    with engine.begin() as connection:
        migrate_to_db('migrations', 'alembic.ini', connection)
    yield session
    container.stop()
    container.remove()
    engine.dispose()


@pytest.fixture(autouse=True)
def cleanup_database(db_session):
    """clean up the database after each test"""
    yield
    db_session.rollback()
