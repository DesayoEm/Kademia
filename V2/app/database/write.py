from config import engine
from uuid import UUID
from datetime import datetime, date
from sqlalchemy.orm import Session
from models.profiles import System, Parents, Students
from models.organization import Classes, Departments

TRAKADEMIK_ID = UUID('00000000-0000-0000-0000-000000000000')
TEST_DEPT = UUID('00000000-0000-0000-0000-000000000001')
try:
    with Session(engine) as session:
        user = session.query(Students).filter_by(student_id = 'STU/00/01/0000').first()
        session.delete(user)
        session.commit()
#
#         session.add(student)
#         session.commit()
#         print("System user created successfully.")
except Exception as e:
    print(f"Error: {e}")

