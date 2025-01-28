from sqlalchemy.orm import Session
from .config import Session

def get_db() -> Session:
    db = Session()
    try:
        yield db
    finally:
        Session.remove()
