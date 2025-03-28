from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional
from sqlalchemy import select, exists

from V2.app.core.errors.staff_organisation_errors import RelatedDepartmentNotFoundError, RelatedRoleNotFoundError
from V2.app.core.errors.user_profile_errors import RelatedStaffNotFoundError
from V2.app.database.models import StaffRole


class EntityValidator:
    """Centralized validation service for entity relationships."""

    def __init__(self, session: Session):
        self.session = session

    def validate_department_exists(self, department_id: UUID) -> bool:#Cache later
        """Validate that a staff department exists."""
        from ...database.models import StaffDepartment

        stmt = select(
            exists().where(StaffDepartment.id == department_id)
        )
        if not self.session.execute(stmt).scalar():
            raise RelatedDepartmentNotFoundError(
                id=department_id,
                detail="Department entity validation failed",
                action="None"
            )
        return True

    def validate_role_exists(self, role_id: UUID) -> bool:#Cache later
        """Validate that a role department exists."""
        from ...database.models import StaffDepartment

        stmt = select(
            exists().where(StaffRole.id == role_id)
        )
        if not self.session.execute(stmt).scalar():
            raise RelatedRoleNotFoundError(
                id=role_id,
                detail="Role entity validation failed",
                action="None"
            )
        return True

    def validate_staff_exists(self, staff_id: UUID) -> bool:#Cache later
        """Validate that a staff member id exists."""
        from ...database.models import Staff

        stmt = select(
            exists().where(Staff.id == staff_id)
        )
        if not self.session.execute(stmt).scalar():
            raise RelatedStaffNotFoundError(
                id=staff_id,
                detail="Staff entity validation failed",
                action="None"
            )
        return True

