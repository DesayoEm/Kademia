from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from V2.app.database.models.common_imports import Base

load_dotenv()
database_url = os.getenv("DATABASE_URL")
engine= create_engine(database_url, echo=True)

