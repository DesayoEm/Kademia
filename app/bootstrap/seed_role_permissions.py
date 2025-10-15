
from app.settings import config
from app.infra.db.db_config import engine
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.bootstrap.matrix import matrix
from app.core.shared.models.enums import UserRoleName
from app.core.rbac.models import Permission, RolePermission, Role
from uuid import UUID, uuid4
from datetime import datetime

session = Session(engine)
now = datetime.now()
KADEMIA_ID = UUID(config.KADEMIA_ID)



def seed_roles():
    try:
        roles = []
        role_names = ["SUPERUSER", "SUPER_EDUCATOR", "EDUCATOR",
                      "STUDENT", "GUARDIAN", "ADMIN"]

        for role_name in role_names:
            name = UserRoleName[role_name]
            role = Role(
                id=uuid4(),
                name=name,
                description=name,

                created_by=KADEMIA_ID,
                last_modified_by=KADEMIA_ID,

                created_at=now,
                last_modified_at=now,
                is_archived=False,
            )

            roles.append(role)



        session.add_all(roles)
        session.commit()
        print(f"Roles created successfully.\n ========================")

    except Exception as e:
        print(f"Error: {e} \n xxxxxxxxxxxxxxxxxxxxxxxxx")
        session.rollback()



def seed_super_user_permissions():
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



def seed_student_permissions():
    try:
        role_permissions = matrix.get("STUDENT")
        student_permissions = []

        with Session(engine) as session:
            #role
            stmt = select(Role).where(Role.name == UserRoleName.STUDENT)
            student = session.execute(stmt).scalar_one()
            role_id = student.id

            #find permission obj for each str in the matrix
            for permission_str in role_permissions:

                permission_obj = session.execute(
                    select(Permission).where(Permission.name == permission_str)
                ).scalar_one()

                student_permission = RolePermission(
                    role_id=role_id,
                    permission_id=permission_obj.id,
                    created_by = KADEMIA_ID,
                    last_modified_by = KADEMIA_ID
                )
                student_permissions.append(student_permission)

            session.add_all(student_permissions)
            session.commit()
            print(f"All student permissions created")

    except Exception as e:
        print(f"Error: {e} \n xxxxxxxxxxxxxxxxxxxxxxxxx")
        session.rollback()


def seed_guardian_permissions():
    try:
        role_permissions = matrix.get("GUARDIAN")
        guardian_permissions = []

        with Session(engine) as session:
            #role
            stmt = select(Role).where(Role.name == UserRoleName.GUARDIAN)
            guardian = session.execute(stmt).scalar_one()
            role_id = guardian.id

            #find permission obj for each str in the matrix
            for permission_str in role_permissions:

                permission_obj = session.execute(
                    select(Permission).where(Permission.name == permission_str)
                ).scalar_one()

                guardian_permission = RolePermission(
                    role_id=role_id,
                    permission_id=permission_obj.id,
                    created_by = KADEMIA_ID,
                    last_modified_by = KADEMIA_ID
                )
                guardian_permissions.append(guardian_permission)

            session.add_all(guardian_permissions)
            session.commit()
            print(f"All guardian permissions created")

    except Exception as e:
        print(f"Error: {e} \n xxxxxxxxxxxxxxxxxxxxxxxxx")
        session.rollback()


