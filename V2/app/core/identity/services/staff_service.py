from uuid import UUID
from sqlalchemy.orm import Session

from V2.app.core.identity.factories.staff import StaffFactory
from V2.app.core.identity.models.staff import Staff
from V2.app.core.shared.models.enums import StaffAvailability
from V2.app.core.shared.services.audit_export_service.export import ExportService


class StaffService:
    def __init__(self, session: Session, current_user):
        self.session = session
        self.current_user = current_user
        self.factory = StaffFactory(session, Staff, current_user= current_user)
        self.export_service = ExportService(session)


    def assign_role(self, staff_id: UUID, role_id: UUID | None = None):
        """Assign a role to staff member"""
        if not role_id:
            return self.factory.update_staff(staff_id, {"role_id": None})

        return self.factory.update_staff(staff_id, {"role_id": role_id})


    def assign_department(self, staff_id: UUID, department_id: UUID | None = None):
        """Assign a department to staff member"""
        if not department_id:
            return self.factory.update_staff(staff_id, {"department_id": None})

        return self.factory.update_staff(staff_id, {"department_id": department_id})


    def update_staff_availability(self, staff_id: UUID, availability: StaffAvailability):
        """Update staff availability status."""
        return self.factory.update_staff(staff_id, {"availability": availability.value})


    def export_staff(self, staff_id: UUID, export_format: str) -> str:
        """Export staff object and its associated data
        Args:
            staff_id: Staff UUID
            export_format: Preferred export format
        """
        return self.export_service.export_entity(
            Staff, staff_id, export_format
        )