from .db_config import engine
from V2.app.core.shared.database.models import *

def create_tables():
    print('create_tables')
    Base.metadata.create_all(engine)

create_tables()