from uuid import UUID
from sqlalchemy.orm import Session
from V2.app.core.shared.validators.entity_validators import EntityValidator
from V2.app.core.staff_management.factories.department import StaffDepartmentFactory
from V2.app.core.staff_management.models import StaffDepartment, StaffRole
from V2.app.core.shared.services.export_service.export import ExportService


class StaffManagementService:
    def __init__(self, session: Session, current_user=None):
        self.session = session
        self.factory = StaffDepartmentFactory(session, current_user=current_user)
        self.entity_validator = EntityValidator(session)
        self.export_service = ExportService(session)


    def assign_manager(self, department_id: UUID, manager_id: UUID):
        department = self.factory.get_staff_department(department_id)

        validated_manager_id = self.entity_validator.validate_staff_exists(manager_id)
        department.manager_id = validated_manager_id

        return self.factory.update_staff_department(
            department_id, {"manager_id": validated_manager_id}
        )


    def remove_manager(self, department_id: UUID):
        """Remove manager from a department."""
        return self.factory.update_staff_department(department_id, {"manager_id": None})


    def export_department(self, department_id: UUID, export_format: str) -> str:
        """Export department and its associated data
        Args:
            department_id: level UUID
            export_format: Preferred export format
        """
        return self.export_service.export_entity(
            StaffDepartment, department_id, export_format
        )


    def export_role(self, role_id: UUID, export_format: str) -> str:
        """Export role and its associated data
        Args:
            role_id: Role UUID
            export_format: Preferred export format
        """
        return self.export_service.export_entity(
            StaffRole, role_id, export_format
        )



