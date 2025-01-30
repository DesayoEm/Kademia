from config import engine
from .models.common_imports import Base


def create_tables():
    print('create_tables')
    Base.metadata.create_all(engine)