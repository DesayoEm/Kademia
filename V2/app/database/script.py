from uuid import uuid4
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import text
from V2.app.database.models import StaffDepartments, StaffRoles, Staff
from V2.app.database.models.profiles import System
from V2.app.database.models.data_enums import (
    AccessLevel, EmploymentStatus, StaffAvailability, Gender, UserType, StaffType
)
from config import engine
from uuid import UUID

TRAKADEMIK_ID = UUID('00000000-0000-0000-0000-000000000000')

now = datetime.now()
try:

    with Session(engine) as session:
        session.execute(text('ALTER TABLE staff_roles DISABLE TRIGGER ALL'))
        session.execute(text('ALTER TABLE staff_departments DISABLE TRIGGER ALL'))
        session.execute(text('ALTER TABLE staff DISABLE TRIGGER ALL'))
        session.execute(text('ALTER TABLE system DISABLE TRIGGER ALL'))


        system_user = System(
            id=TRAKADEMIK_ID,
            password_hash='trakademik_system_hash',
            first_name='TraKademik',
            last_name='System',
            gender=Gender.SYSTEM,
            access_level=AccessLevel.SYSTEM,
            department_id=None,
            role_id=None,
            image_url="path_to_img",
            user_type=UserType.SYSTEM,
            staff_type=StaffType.SYSTEM,
            status=EmploymentStatus.ACTIVE,
            availability=StaffAvailability.AVAILABLE,
            email_address='system@trakademik.com',
            phone='00000000000',
            address='System Location',
            date_joined=now.date(),
            created_at=now,
            last_modified_at=now,
            created_by=TRAKADEMIK_ID,
            last_modified_by=TRAKADEMIK_ID,
            is_archived=False,
            deletion_eligible=False
        )

        session.add(system_user)
        session.flush()


        system_role = StaffRoles(
            id=TRAKADEMIK_ID,
            name='System Administrator',
            description='System administrative role',
            created_at=now,
            last_modified_at=now,
            created_by=TRAKADEMIK_ID,
            last_modified_by=TRAKADEMIK_ID,
            is_archived=False
        )

        session.add(system_role)
        session.flush()

        system_department = StaffDepartments(
            id=TRAKADEMIK_ID,
            name='System Department',
            description='System administrative department',
            created_at=now,
            last_modified_at=now,
            created_by=TRAKADEMIK_ID,
            last_modified_by=TRAKADEMIK_ID,
            is_archived=False
        )

        session.add(system_department)
        session.flush()


        system_user.department_id = system_department.id
        system_user.role_id = system_role.id


        session.commit()


        session.execute(text('ALTER TABLE staff_roles ENABLE TRIGGER ALL'))
        session.execute(text('ALTER TABLE staff_departments ENABLE TRIGGER ALL'))
        session.execute(text('ALTER TABLE staff ENABLE TRIGGER ALL'))
        session.execute(text('ALTER TABLE system ENABLE TRIGGER ALL'))

        print("✅ System user, department, and role created successfully and updated.")

except Exception as e:
    print(f"❌ Error: {e}")
    session.rollback()

finally:
    session.close()
