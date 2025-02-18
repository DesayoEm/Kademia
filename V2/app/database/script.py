from V2.app.database.models import StaffDepartments, StaffRoles
from config import engine
from uuid import UUID
from datetime import datetime, date
from sqlalchemy.orm import Session
from sqlalchemy import text
from V2.app.database.models.profiles import System
from V2.app.database.models.data_enums import (
    AccessLevel, EmploymentStatus, StaffAvailability, Gender, UserType, StaffType
)

TRAKADEMIK_ID = UUID('00000000-0000-0000-0000-000000000000')

try:
    with Session(engine) as session:
        session.execute(text('ALTER TABLE staff_roles DISABLE TRIGGER ALL'))
        session.execute(text('ALTER TABLE staff_departments DISABLE TRIGGER ALL'))
        session.execute(text('ALTER TABLE staff DISABLE TRIGGER ALL'))
        session.execute(text('ALTER TABLE system DISABLE TRIGGER ALL'))

        system_role = StaffRoles(
            id=TRAKADEMIK_ID,
            title='System Administrator',
            description='System administrative role',
            created_at=datetime.now(),
            last_modified_at=datetime.now(),
            created_by=TRAKADEMIK_ID,
            last_modified_by=TRAKADEMIK_ID,
            is_archived=False
        )
        session.add(system_role)

        system_department = StaffDepartments(
            id=TRAKADEMIK_ID,
            name='System Department',
            description='System administrative department',
            created_at=datetime.now(),
            last_modified_at=datetime.now(),
            created_by=TRAKADEMIK_ID,
            last_modified_by=TRAKADEMIK_ID,
            is_archived=False
        )
        session.add(system_department)


        system_user = System(
            id=TRAKADEMIK_ID,
            password_hash='trakademik_system_hash',
            first_name='TraKademik',
            last_name='System',
            gender=Gender.SYSTEM,
            access_level=AccessLevel.SYSTEM,
            user_type=UserType.SYSTEM,
            staff_type=StaffType.SYSTEM,
            status=EmploymentStatus.ACTIVE,
            availability=StaffAvailability.AVAILABLE,
            image_url='path/to/system/avatar.png',
            email_address='system@trakademik.com',
            phone='00000000000',
            address='System Location',
            department_id=TRAKADEMIK_ID,
            role_id=TRAKADEMIK_ID,
            date_joined=datetime.now().date(),
            created_at=datetime.now(),
            last_modified_at=datetime.now(),
            created_by=TRAKADEMIK_ID,
            last_modified_by=TRAKADEMIK_ID,
            is_archived=False,
            deletion_eligible=False
        )
        session.add(system_user)

        # Commit everything
        session.commit()

        session.execute(text('ALTER TABLE staff_roles ENABLE TRIGGER ALL'))
        session.execute(text('ALTER TABLE staff_departments ENABLE TRIGGER ALL'))
        session.execute(text('ALTER TABLE staff ENABLE TRIGGER ALL'))
        session.execute(text('ALTER TABLE system ENABLE TRIGGER ALL'))

        print("System user, department, and role created successfully.")

except Exception as e:
    print(f"Error: {e}")
    session.rollback()
    #re-enable triggers even if there's an error
    with Session(engine) as session:
        session.execute(text('ALTER TABLE staff_roles ENABLE TRIGGER ALL'))
        session.execute(text('ALTER TABLE staff_departments ENABLE TRIGGER ALL'))
        session.execute(text('ALTER TABLE staff ENABLE TRIGGER ALL'))
        session.execute(text('ALTER TABLE system ENABLE TRIGGER ALL'))
finally:
    session.close()