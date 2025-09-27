from app.bootstrap.python_scripts.matrix import matrix
from app.infra.settings import config
from app.infra.db.db_config import engine
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.core.shared.models.enums import UserRoleName
from app.core.rbac.models import RolePermission, Role, Permission
from uuid import UUID
from datetime import datetime


now = datetime.now()
KADEMIA_ID = UUID(config.KADEMIA_ID)


def init_super_user_permissions():
    try:
        role_permissions = matrix.get("SUPERUSER")
        super_user_permissions = []

        with Session(engine) as session:
            #role
            stmt = select(Role).where(Role.name == UserRoleName.SUPERUSER)
            super_user = session.execute(stmt).scalar_one()
            role_id = super_user.id

            #find permission obj for each str in the matrix
            for permission_str in role_permissions:

                permission_obj = session.execute(
                    select(Permission).where(Permission.name == permission_str)
                ).scalar_one()

                super_user_permission = RolePermission(
                    role_id=role_id,
                    permission_id=permission_obj.id,
                    created_by = KADEMIA_ID,
                    last_modified_by = KADEMIA_ID
                )
                super_user_permissions.append(super_user_permission)

            session.add_all(super_user_permissions)
            session.commit()
            print(f"All super user permissions created")

    except Exception as e:
        print(f"Error: {e} \n xxxxxxxxxxxxxxxxxxxxxxxxx")
        session.rollback()

