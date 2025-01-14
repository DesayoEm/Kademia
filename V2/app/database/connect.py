from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker


# db_url = "postgresql://postgres:password@localhost:5432/trakademik"
#
# engine= create_engine(db_url, echo=True)
#
# Session=sessionmaker(bind=engine)
# session = Session()
#
# with engine.connect() as connection:
#     result= connection.execute(text("select 'Hello'"))
#
#     print (result.all())
