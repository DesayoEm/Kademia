from ...core.errors.decorators.fk_resolver_decorators import resolve_fk_on_create
from ...core.services.export_service.export import ExportService
from ...database.models import Staff
from ...database.models.enums import ArchiveReason
from ...schemas.users.staff import (
    StaffCreate, StaffUpdate, StaffResponse, StaffFilterParams
)
from ...core.factories.users.staff import StaffFactory
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List


class StaffCrud:
    """CRUD operations for staff."""

    def __init__(self, session: Session):
        """Initialize CRUD service.
        Args:
            session: SQLAlchemy database session
        """
        self.session = session
        self.factory = StaffFactory(session)
        self.export_service = ExportService(session)

    @resolve_fk_on_create()
    def create_staff(self, data: StaffCreate) -> StaffResponse:
        """Create a new staff.
        Args:
            data: Validated staff creation data
        Returns:
            StaffResponse: Created staff
        """
        staff = self.factory.create_staff(data)
        return StaffResponse.model_validate(staff)


    def get_staff(self, staff_id: UUID) -> StaffResponse:
        """Get staff by ID.
        Args:
            staff_id: staff UUID
        Returns:
            StaffResponse: Retrieved staff
        """
        staff = self.factory.get_staff(staff_id)
        return StaffResponse.model_validate(staff)


    def get_all_staff(self, filters: StaffFilterParams) -> List[StaffResponse]:
        """Get all active staff.
        Returns:
            List[StaffResponse]: List of active staff
        """
        all_staff = self.factory.get_all_staff(filters)
        return [StaffResponse.model_validate(staff) for staff in all_staff]


    def update_staff(self, staff_id: UUID, data: StaffUpdate) -> StaffResponse:
        """Update staff information.
        Args:
            staff_id: staff UUID
            data: Validated update data
        Returns:
            StaffResponse: Updated staff
        """
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
        """Export role and its associated data
        Args:
            staff_id: staff member UUID
            export_format: Preferred export format
        """
        return self.export_service.export_entity(
            Staff, staff_id, export_format
        )

    def delete_staff(self, staff_id: UUID) -> None:
        """Permanently delete a staff.
        Args:
            staff_id: staff UUID
        """
        self.factory.delete_staff(staff_id)


    # Archived staff operations
    def get_archived_staff(self, staff_id: UUID) -> StaffResponse:
        """Get an archived staff by ID.
        Args:
            staff_id: staff UUID
        Returns:
            StaffResponse: Retrieved archived staff
        """
        staff = self.factory.get_archived_staff(staff_id)
        return StaffResponse.model_validate(staff)

    def get_all_archived_staff(self, filters: StaffFilterParams) -> List[StaffResponse]:
        """Get all archived staff.
        Args:
            filters: Filter parameters
        Returns:
            List[StaffResponse]: List of archived staff
        """
        all_staff = self.factory.get_all_archived_staff(filters)
        return [StaffResponse.model_validate(staff) for staff in all_staff]

    def restore_staff(self, staff_id: UUID) -> StaffResponse:
        """Restore an archived staff.
        Args:
            staff_id: staff UUID
        Returns:
            StaffResponse: Restored staff
        """
        staff = self.factory.restore_staff(staff_id)
        return StaffResponse.model_validate(staff)

    def delete_archived_staff(self, staff_id: UUID) -> None:
        """Permanently delete an archived staff.
        Args:
            staff_id: staff UUID
        """
        self.factory.delete_archived_staff(staff_id)