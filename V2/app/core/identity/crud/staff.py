from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from V2.app.core.shared.services.export_service.export import ExportService
from V2.app.core.identity.factories.staff import StaffFactory
from V2.app.core.identity.models.staff import Staff
from V2.app.core.shared.schemas.enums import ArchiveReason
from V2.app.core.identity.schemas.staff import (
    StaffCreate, StaffUpdate, StaffResponse, StaffFilterParams
)


class StaffCrud:
    """CRUD operations for staff."""

    def __init__(self, session: Session, current_user = None):
        """Initialize CRUD service.
        Args:
            session: SQLAlchemy db session
            current_user: The authenticated user performing the operation, if any.
        """
        self.session = session
        self.current_user = current_user
        self.factory = StaffFactory(session, current_user=current_user)
        self.export_service = ExportService(session)


    def create_staff(self, data: StaffCreate) -> StaffResponse:
        """Create a new staff."""
        staff = self.factory.create_staff(data)
        return StaffResponse.model_validate(staff)


    def get_staff(self, staff_id: UUID) -> StaffResponse:
        """Get staff by ID."""
        staff = self.factory.get_staff(staff_id)
        return StaffResponse.model_validate(staff)


    def get_all_staff(self, filters: StaffFilterParams) -> List[StaffResponse]:
        """Get all active staff."""
        all_staff = self.factory.get_all_staff(filters)
        return [StaffResponse.model_validate(staff) for staff in all_staff]


    def update_staff(self, staff_id: UUID, data: StaffUpdate) -> StaffResponse:
        """Update staff information."""
        data = data.model_dump()
        updated_staff = self.factory.update_staff(staff_id, data)
        return StaffResponse.model_validate(updated_staff)

    def archive_staff(self, staff_id: UUID, reason: ArchiveReason) -> None:
        """Archive a staff.
        Args:
            staff_id: staff UUID
            reason: Reason for archiving
        Returns:
            StaffResponse: Archived staff
        """
        self.factory.archive_staff(staff_id, reason)


    def export_staff(self, staff_id: UUID, export_format: str) -> str:
        """Export staff object and its associated data
        Args:
            staff_id: staff member UUID
            export_format: Preferred export format
        """
        return self.export_service.export_entity(
            Staff, staff_id, export_format
        )


    def delete_staff(self, staff_id: UUID) -> None:
        """Permanently delete a staff object."""
        self.factory.delete_staff(staff_id)


    # Archived staff operations
    def get_archived_staff(self, staff_id: UUID) -> StaffResponse:
        """Get an archived staff object by ID."""
        staff = self.factory.get_archived_staff(staff_id)
        return StaffResponse.model_validate(staff)


    def get_all_archived_staff(self, filters: StaffFilterParams) -> List[StaffResponse]:
        """Get all archived staff."""
        all_staff = self.factory.get_all_archived_staff(filters)
        return [StaffResponse.model_validate(staff) for staff in all_staff]


    def restore_staff(self, staff_id: UUID) -> StaffResponse:
        """Restore an archived staff object."""
        staff = self.factory.restore_staff(staff_id)
        return StaffResponse.model_validate(staff)


    def delete_archived_staff(self, staff_id: UUID) -> None:
        """Permanently delete an archived staff."""
        self.factory.delete_archived_staff(staff_id)