from datetime import datetime
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import text
from V2.app.core.shared.models import System, StaffDepartment, StaffRole
from V2.app.core.shared.models import (
    AccessLevel, EmploymentStatus, StaffAvailability, Gender, UserType, StaffType
)
from V2.app.infra.db.db_config import engine


KADEMIA_ID = UUID('00000000-0000-0000-0000-000000000000')

now = datetime.now()
session = Session(engine)

try:
    session.execute(text('ALTER TABLE staff_roles DISABLE TRIGGER ALL'))
    session.execute(text('ALTER TABLE staff_departments DISABLE TRIGGER ALL'))
    session.execute(text('ALTER TABLE staff DISABLE TRIGGER ALL'))
    session.execute(text('ALTER TABLE system DISABLE TRIGGER ALL'))

    system_role = StaffRole(
        id=KADEMIA_ID,
        name='System Administrator',
        description='System administrative role',
        created_at=now,
        last_modified_at=now,
        created_by=KADEMIA_ID,
        last_modified_by=KADEMIA_ID,
        is_archived=False
    )
    session.add(system_role)

    system_department = StaffDepartment(
        id=KADEMIA_ID,
        name='System Department',
        description='System administrative department',
        created_at=now,
        last_modified_at=now,
        created_by=KADEMIA_ID,
        last_modified_by=KADEMIA_ID,
        is_archived=False,
        manager_id=None
    )
    session.add(system_department)
    session.flush()


    system_user = System(
        id=KADEMIA_ID,
        password_hash='Kademia_system_hash',
        first_name='Kademia',
        last_name='System',
        gender=Gender.SYSTEM,
        access_level=AccessLevel.SYSTEM,
        department_id=system_department.id,
        role_id=system_role.id,
        user_type=UserType.SYSTEM,
        staff_type=StaffType.System,
        status=EmploymentStatus.ACTIVE,
        availability=StaffAvailability.AVAILABLE,
        email_address='system@kademia.com',
        phone='00000000000',
        address='System Location',
        date_joined=now.date(),
        created_at=now,
        last_modified_at=now,
        created_by=KADEMIA_ID,
        last_modified_by=KADEMIA_ID,
        is_archived=False,
        deletion_eligible=False
    )
    session.add(system_user)

    session.commit()

    print("✅ System user, department, and role created successfully.")

except Exception as e:
    print(f"❌ Error: {e}")
    session.rollback()

finally:
    session.execute(text('ALTER TABLE staff_roles ENABLE TRIGGER ALL'))
    session.execute(text('ALTER TABLE staff_departments ENABLE TRIGGER ALL'))
    session.execute(text('ALTER TABLE staff ENABLE TRIGGER ALL'))
    session.execute(text('ALTER TABLE system ENABLE TRIGGER ALL'))
    session.close()