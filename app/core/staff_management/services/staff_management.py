from uuid import UUID
from sqlalchemy.orm import Session
from app.core.shared.validators.entity_validators import EntityValidator
from app.core.staff_management.factories.department import StaffDepartmentFactory


class StaffManagementService:
    def __init__(self, session: Session, current_user=None):
        self.session = session
        self.factory = StaffDepartmentFactory(session, current_user=current_user)
        self.entity_validator = EntityValidator(session)

    def assign_manager(self, department_id: UUID, manager_id: UUID | None = None):
        department = self.factory.get_staff_department(department_id)

        if not manager_id:
            return self.factory.update_staff_department(
                department_id, {"manager_id": None}
            )

        validated_manager_id = self.entity_validator.validate_staff_exists(manager_id)
        department.manager_id = validated_manager_id

        return self.factory.update_staff_department(
            department_id, {"manager_id": validated_manager_id}
        )
