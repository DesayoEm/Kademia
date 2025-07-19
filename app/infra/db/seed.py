from datetime import datetime
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.core.auth.services.password_service import PasswordService
from app.core.identity.models.staff import System
from app.core.staff_management.models import StaffRole
from app.core.shared.models.enums import (
    EmploymentStatus, StaffAvailability, StaffType, AccessLevel, Gender, UserType,
)
from app.infra.db.db_config import engine


KADEMIA_ID = UUID('00000000-0000-0000-0000-000000000000')
MORIA_ID = UUID('00000000-0000-0000-0000-000000000001')

now = datetime.now()
session = Session(engine)

try:
    session.execute(text('ALTER TABLE staff_roles DISABLE TRIGGER ALL'))
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

    system_user = System(
        id=KADEMIA_ID,
        password_hash= PasswordService.hash_password('kademia'),
        first_name='Kademia',
        last_name='System',
        gender=Gender.SYSTEM,
        access_level=AccessLevel.SYSTEM,
        role_id=system_role.id,
        user_type=UserType.SYSTEM,
        staff_type=StaffType.System,
        status=EmploymentStatus.ACTIVE,
        availability=StaffAvailability.AVAILABLE,
        email_address='system@kademia.com',
        phone='00000000110',
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

    print("✅ System user, and role created successfully.")

except Exception as e:
    print(f"❌ Error: {e}")
    session.rollback()

finally:
    session.execute(text('ALTER TABLE staff_roles ENABLE TRIGGER ALL'))
    session.execute(text('ALTER TABLE staff ENABLE TRIGGER ALL'))
    session.execute(text('ALTER TABLE system ENABLE TRIGGER ALL'))
    session.close()