from datetime import datetime
from uuid import UUID, uuid4
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.core.auth.services.password_service import PasswordService
from app.core.identity.models.staff import System, AdminStaff
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

def seed_super_user():
    try:
        with Session(engine) as session:
            #role
            stmt = select(Role).where(Role.name == UserRoleName.SUPERUSER)
            super_user_obj = session.execute(stmt).scalar_one()
            role_id = super_user_obj.id


            super_user = AdminStaff(
                id=uuid4(),
                password_hash=PasswordService.hash_password(F"{config.USER_PASSWORD}"),
                first_name='Admin',
                last_name='Staff',
                gender=Gender.SYSTEM,
                current_role_id=role_id,
                user_type=UserType.STAFF,
                staff_type=StaffType.ADMIN,
                status=StaffStatus.ACTIVE,
                availability=StaffAvailability.AVAILABLE,
                email_address='admin@kademia.com',
                phone='00000000111',
                address='System',
                date_joined=now.date(),
                created_at=now,
                last_modified_at=now,
                created_by=KADEMIA_ID,
                last_modified_by=KADEMIA_ID,
                is_archived=False,
                deletion_eligible=False
            )
            session.add(super_user)
            session.commit()
            print("Super user created successfully.\n ========================")

    except Exception as e:
        print(f"Error: {e} \n xxxxxxxxxxxxxxxxxxxxxxxxx")
        session.rollback()

print(KADEMIA_ID)