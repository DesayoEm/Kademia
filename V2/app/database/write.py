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

        student = Students(
            id=TRAKADEMIK_ID,
            image_url = "path-to-img",
            student_id = 'STU1',
            password_hash="teststudent",
            access_level="User",
            first_name="Test",
            last_name="Student",
            gender="F",
            date_of_birth = date.today(),
            class_id = TEST_DEPT,
            department_id = TEST_DEPT,
            parent_id = TEST_DEPT,
            is_active = True,
            admission_date = date.today(),
            last_login=datetime.now().date()
        )

        session.add(student)
        session.commit()
        print("System user created successfully.")
except Exception as e:
    print(f"Error: {e}")