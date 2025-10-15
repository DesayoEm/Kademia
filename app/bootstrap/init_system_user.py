from datetime import datetime
from uuid import UUID
from sqlalchemy.orm import Session
from app.core.auth.services.password_service import PasswordService
from app.core.identity.models.staff import System
from app.core.shared.models.enums import UserRoleName
from app.core.rbac.models import Role

from app.core.shared.models.enums import (
    StaffStatus, StaffAvailability, StaffType, Gender, UserType
)

from app.settings import config
from app.infra.db.db_config import engine

KADEMIA_ID = UUID(config.KADEMIA_ID)

now = datetime.now()
session = Session(engine)


def init_system_user_and_role():
    now = datetime.utcnow()
    try:
        with Session(engine) as session:
            # Step 1: Create the system role with NULL creator temporarily
            system_role = Role(
                id=KADEMIA_ID,
                name=UserRoleName.SYSTEM,
                description="Super Super User",
                created_by=None,  # temporarily break the circle
                last_modified_by=None,
                created_at=now,
                last_modified_at=now,
                is_archived=False,
            )
            session.add(system_role)
            session.flush()


            system_user = System(
                id=KADEMIA_ID,
                password_hash=PasswordService.hash_password(f"{config.KADEMIA_PASSWORD}"),
                first_name="Kademia",
                last_name="System",
                gender=Gender.SYSTEM,
                current_role_id=system_role.id,  # now valid
                user_type=UserType.SYSTEM,
                staff_type=StaffType.SYSTEM,
                status=StaffStatus.ACTIVE,
                availability=StaffAvailability.AVAILABLE,
                email_address="system@kademia.com",
                phone="00000000110",
                address="System",
                date_joined=now.date(),
                created_by=KADEMIA_ID,
                last_modified_by=KADEMIA_ID,
                created_at=now,
                last_modified_at=now,
                is_archived=False,
                deletion_eligible=False,
            )
            session.add(system_user)
            session.flush()

            system_role.created_by = system_user.id
            system_role.last_modified_by = system_user.id

            session.commit()
            print("System role and user created successfully.")

    except Exception as e:
        session.rollback()
        print(f"Error: {e}")

if __name__ == '__main__':
    init_system_user_and_role()