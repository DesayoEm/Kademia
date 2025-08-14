from datetime import datetime
from uuid import UUID
from sqlalchemy.orm import Session
from app.core.auth.services.password_service import PasswordService
from app.core.identity.models.staff import System
from app.core.shared.models.enums import (
    EmploymentStatus, StaffAvailability, StaffType, Gender, UserType, UserRole,
)
from app.infra.db.db_config import engine


KADEMIA_ID = UUID('00000000-0000-0000-0000-000000000000')

now = datetime.now()
session = Session(engine)

try:
    system_user = System(
        id=KADEMIA_ID,
        password_hash=PasswordService.hash_password('kademia'),
        first_name='Kademia',
        last_name='System',
        gender=Gender.SYSTEM,
        current_role=UserRole.SYSTEM,
        user_type=UserType.SYSTEM,
        staff_type=StaffType.SYSTEM,
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

    print("✅ System user created successfully.")

except Exception as e:
    print(f"❌ Error: {e}")
    session.rollback()
