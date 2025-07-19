from sqlalchemy import create_engine, MetaData
from app import Base

def create_test_tables(engine):
    """Create all tables defined in Base.metadata"""
    try:
        metadata = MetaData()
        metadata.reflect(bind=engine)
        metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        print("Test tables created successfully")
    except Exception as e:
        print(f"Error creating test tables: {e}")
        raise

def drop_test_tables(engine):
    """Drop all tables in correct order based on dependencies"""
    try:
        metadata = MetaData()
        metadata.reflect(bind=engine)
        metadata.drop_all(bind=engine)
        print("Test tables dropped successfully")
    except Exception as e:
        print(f"Error dropping test tables: {e}")
        raise
