from sqlalchemy import create_engine
from app.settings import config
from sqlalchemy.orm import sessionmaker


database_url = config.DATABASE_URL
engine = create_engine(database_url, echo=True)

SessionFactory = sessionmaker(autocommit=False, autoflush=True, bind=engine)
