from app.bootstrap.python_scripts.matrix import matrix
from app.infra.settings import config
from app.infra.db.db_config import engine
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.core.shared.models.enums import Action, Resource
from app.core.rbac.models import RolePermission
from uuid import UUID, uuid4
from datetime import datetime

session = Session(engine)

now = datetime.now()
KADEMIA_ID = UUID(config.KADEMIA_ID)


def init_super_user_permissions():
    try:
        super_user_stmt = ""
        super_user = session.execute(super_user_stmt)


        super_user_permissions = None
        role_permissions = []

        role_permission = RolePermission(

        )
        role_permissions.append(role_permission)

        session.add_all(role_permissions)
        session.commit()

        for permission in role_permissions:
            print(f"{permission.name} created purr")

    except Exception as e:
        print(f"Error: {e} \n xxxxxxxxxxxxxxxxxxxxxxxxx")
        session.rollback()

