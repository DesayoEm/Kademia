from sqlalchemy.orm import Session
from typing import Generator
from .db_config import SessionFactory

def get_db() -> Generator:
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()
