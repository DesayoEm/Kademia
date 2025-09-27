from datetime import datetime
from uuid import UUID
from sqlalchemy.orm import Session
from app.core.auth.services.password_service import PasswordService
from app.core.identity.models.staff import System
from app.core.rbac.models import Role
from app.core.shared.models.enums import (
    EmploymentStatus, StaffAvailability, StaffType, Gender, UserType, UserRoleName,
)
from app.infra.settings import config
from app.infra.db.db_config import engine

KADEMIA_ID = UUID(config.KADEMIA_ID)
KADEMIA_PASSWORD = UUID(config.KADEMIA_PASSWORD)

now = datetime.now()
session = Session(engine)

def create_role():
    try:
        super_user_role = Role(
            id=KADEMIA_ID,
            name=UserRoleName.SYSTEM,
            description='Super User',
            rank=10,
            created_at=now,
            last_modified_at=now,
            is_archived=False,
        )
        session.add(super_user_role)
        session.commit()
        print("System role created successfully.\n ========================")

    except Exception as e:
        print(f"Error: {e} \n xxxxxxxxxxxxxxxxxxxxxxxxx")
        session.rollback()


def create_user():
    try:
        system_user = System(
            id=KADEMIA_ID,
            password_hash=PasswordService.hash_password(F"{KADEMIA_PASSWORD}"),
            first_name='Kademia',
            last_name='System',
            gender=Gender.SYSTEM,
            current_role_id=KADEMIA_ID,
            user_type=UserType.SYSTEM,
            staff_type=StaffType.SYSTEM,
            status=EmploymentStatus.ACTIVE,
            availability=StaffAvailability.AVAILABLE,
            email_address='system@kademia.com',
            phone='00000000110',
            address='System',
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
        print("Super user created successfully.\n ========================")

    except Exception as e:
        print(f"Error: {e} \n xxxxxxxxxxxxxxxxxxxxxxxxx")
        session.rollback()



