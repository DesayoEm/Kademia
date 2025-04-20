from sqlalchemy.orm import Session
from uuid import UUID

from V2.app.core.shared.errors import RelatedEntityNotFoundError
from V2.app.core.shared.database.db_repositories.sqlalchemy_repos.base_repo import SQLAlchemyRepository


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

            raise RelatedEntityNotFoundError(
                    entity_model=StaffDepartment, display_name="department",
                    identifier=department_id, operation="create"
                # Operation field will be overriden in the creation layer but 'create' is a fail-safe
            )
        return department_id


    def validate_role_exists(self, role_id: UUID) -> UUID:#Cache later
        """Validate that a role exists."""
        from ...database.models import StaffRole

        repo = self.repository(StaffRole, self.session)
        if not repo.exists(role_id):
            raise RelatedEntityNotFoundError(
                entity_model=StaffRole, display_name="role",
                identifier=role_id, operation="create"
                # Operation field will be overriden in the creation layer but 'create' is a fail-safe
            )

        return role_id


    def validate_staff_exists(self, staff_id: UUID) -> UUID:#Cache later
        """Validate that a staff member id exists."""
        from ...database.models import Staff

        repo = self.repository(Staff, self.session)
        if not repo.exists(staff_id):
            raise RelatedEntityNotFoundError(
                entity_model=Staff, display_name="staff",
                identifier=staff_id, operation="create"
                # Operation field will be overriden in the creation layer but 'create' is a fail-safe
            )

        return staff_id

