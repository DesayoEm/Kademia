from sqlalchemy.orm import Session
from uuid import UUID
from sqlalchemy import select, exists

from ..errors.database_errors import RelationshipError
from ...database.db_repositories.sqlalchemy_repos.base_repo import SQLAlchemyRepository


class EntityValidator:
    """Centralized validation service for entity relationships."""

    def __init__(self, session: Session):
        self.session = session
        self.repository = SQLAlchemyRepository

    def validate_department_exists(self, department_id: UUID) -> UUID:#Cache later
        """Validate that a staff department exists."""
        from ...database.models import StaffDepartment

        repo = self.repository(StaffDepartment, self.session)
        if not repo.exists(department_id):

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

        repo = self.repository(StaffRole, self.session)
        if not repo.exists(role_id):
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

        repo = self.repository(Staff, self.session)
        if not repo.exists(staff_id):
            raise RelationshipError(
                error=f"Failed to validate staff with id {staff_id}",
                operation="create",
                entity="staff"
                # Operation field will be overriden in the creation layer but 'create' is a fail-safe
            )
        return staff_id

