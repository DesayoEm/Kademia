from .db_config import engine
from .models import *

def create_tables():
    print('create_tables')
    Base.metadata.create_all(engine)

create_tables()