from app.bootstrap.python_scripts.matrix import matrix
from app.infra.settings import config
from app.infra.db.db_config import engine
from sqlalchemy.orm import Session
from app.core.shared.models.enums import Action, Resource
from app.core.rbac.models import Permission
from uuid import UUID, uuid4
from datetime import datetime


resources = [resource for resource in Resource]
actions = [action for action in Action]
approved_and_rejected_resources = [
    Resource.TRANSFERS, Resource.PROMOTIONS, Resource.REPETITIONS,
]

historical_resources = [
    Resource.STUDENT_SUBJECTS, Resource.SUBJECT_EDUCATORS,
]

session = Session(engine)
now = datetime.now()
KADEMIA_ID = UUID(config.KADEMIA_ID)


def create_permissions():
    try:
        permissions = []
        for resource in resources:
            for action in actions:
                if resource not in approved_and_rejected_resources and action in [Action.APPROVE, Action.REJECT]:
                    continue

                if resource in historical_resources and action == Action.UPDATE:
                    continue

                else:
                    permission = Permission(
                        id = uuid4(),
                        resource=resource,
                        action = action,
                        name = f"{(resource.value.upper() +"_" + action.value.upper())}",
                        description=f"{(resource.value.title() + " " + action.value.lower())}",
                        created_by=KADEMIA_ID,
                        last_modified_by=KADEMIA_ID,
                    )
                    permissions.append(permission)

        session.add_all(permissions)
        session.commit()

        for permission in permissions:
            print(f"{permission.name} created purr")

    except Exception as e:
        print(f"Error: {e} \n xxxxxxxxxxxxxxxxxxxxxxxxx")
        session.rollback()

