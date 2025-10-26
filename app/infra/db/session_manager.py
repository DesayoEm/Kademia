from typing import Generator
from .db_config import SessionFactory

def get_db() -> Generator:
    db = SessionFactory()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
