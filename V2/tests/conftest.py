import pytest
import os
from sqlalchemy import create_engine,inspect
from sqlalchemy.orm import sessionmaker
from ..tests.utils.db_utils import create_test_tables, drop_test_tables
from .test_db import TEST_DB_URL

@pytest.fixture(scope='session')
def test_engine():
    """Create test database engine"""
    engine = create_engine(os.getenv('TEST_DB_URL'))
    return engine


@pytest.fixture(scope='session', autouse=True)
def db_session(test_engine):
    """Create a test database session with fresh tables"""
    SessionLocal = sessionmaker(autoflush=True, autocommit=False, bind=test_engine)
    session = SessionLocal()
    create_test_tables(test_engine)
    yield session

    drop_test_tables(test_engine)
    session.close()
    test_engine.dispose()


@pytest.fixture(autouse=True)
def cleanup_database(db_session):
    """clean up the db after each test"""
    yield
    db_session.rollback()


@pytest.fixture(scope='function')
def db_inspector(db_session):
    """Get database inspector"""
    return inspect(db_session.bind)