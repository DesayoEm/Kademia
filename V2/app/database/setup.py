from app.database.config import engine
from app.database.models.common_imports import Base

def create_tables():
    print('create_tables')
    Base.metadata.create_all(engine)