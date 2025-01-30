from config import engine
from uuid import UUID
from datetime import datetime
from sqlalchemy.orm import Session
from models.profiles import System

TRAKADEMIK_ID = UUID('00000000-0000-0000-0000-000000000000')

try:
    with Session(engine) as session:

        system_user = System(
            id=TRAKADEMIK_ID,
            image_url = "path-to-img",
            password_hash="trakademik_system",
            access_level="System",
            first_name="TraKademik",
            last_name="System",
            gender="S",
            is_verified=True,
            email_address="system@trakademik.com",
            phone="00000000000",
            department_id = TRAKADEMIK_ID,
            role_id = TRAKADEMIK_ID,
            address="System",
            staff_type="System",
            date_joined=datetime.now().date()
        )
        session.add(system_user)
        session.commit()
        print("System user created successfully.")
except Exception as e:
    print(f"Error: {e}")