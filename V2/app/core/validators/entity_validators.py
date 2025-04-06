from sqlalchemy.orm import Session
from uuid import UUID
from sqlalchemy import select, exists

from ..errors.database_errors import RelationshipError
from ..errors.staff_organisation_errors import RelatedRoleNotFoundError
from ..errors.user_errors import RelatedStaffNotFoundError



class EntityValidator:
    """Centralized validation service for entity relationships."""

    def __init__(self, session: Session):
        self.session = session

    def validate_department_exists(self, department_id: UUID) -> UUID:#Cache later
        """Validate that a staff department exists."""
        from ...database.models import StaffDepartment

        stmt = select(
            exists().where(StaffDepartment.id == department_id)
        )
        if not self.session.execute(stmt).scalar():
            #Note: The error message here is hardcoded because RelationshipError is not triggered organically
            raise RelationshipError(
                    error=f"Failed to validate department with id {department_id}",
                    operation="create",
                    entity="department"
                # Operation field will be overriden in the creation layer but 'create' is a fail-safe
            )
        return department_id

    def validate_role_exists(self, role_id: UUID) -> UUID:#Cache later
        """Validate that a role exists."""
        from ...database.models import StaffRole

        stmt = select(
            exists().where(StaffRole.id == role_id)
        )
        if not self.session.execute(stmt).scalar():
            # Note: The error message here is hardcoded because RelationshipError is not triggered organically
            raise RelationshipError(
                error=f"Failed to validate role with id {role_id}",
                operation="create",
                entity="role"
                # Operation field will be overriden in the creation layer but 'create' is a fail-safe
            )
        return role_id


    def validate_staff_exists(self, staff_id: UUID) -> UUID:#Cache later
        """Validate that a staff member id exists."""
        from ...database.models import Staff

        stmt = select(
            exists().where(Staff.id == staff_id)
        )
        if not self.session.execute(stmt).scalar():
            raise RelationshipError(
                error=f"Failed to validate staff with id {staff_id}",
                operation="create",
                entity="staff"
                # Operation field will be overriden in the creation layer but 'create' is a fail-safe
            )
        return staff_id

