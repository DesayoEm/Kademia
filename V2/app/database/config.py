from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from pathlib import Path
from dotenv import load_dotenv
import os

app_dir = Path(__file__).resolve().parent.parent
env_path = app_dir / '.env'

load_dotenv(dotenv_path=env_path)
database_url = os.getenv("DATABASE_URL")
engine= create_engine(database_url, echo=True)

SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)




