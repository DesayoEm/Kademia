from sqlalchemy.orm import Session
from uuid import UUID
from app.core.shared.exceptions import RelatedEntityNotFoundError
from app.infra.db.repositories.sqlalchemy_repos.base_repo import SQLAlchemyRepository


class EntityValidator:
    """Centralized validation service for entity relationships."""

    def __init__(self, session: Session):
        self.session = session
        self.repository = SQLAlchemyRepository

    def validate_department_exists(self, department_id: UUID) -> UUID:
        """Validate that a staff department exists."""
        from app.core.staff_management.models import StaffDepartment

        repo = self.repository(StaffDepartment, self.session)
        if not repo.exists(department_id):

            raise RelatedEntityNotFoundError(
                entity_model=StaffDepartment,
                display_name="department",
                identifier=department_id,
                operation="create",
                detail="Department not found by EntityValidator ",
            )
        return department_id

    def validate_role_exists(self, role_id: UUID) -> UUID:  # Cache later
        """Validate that a role exists."""
        from app.core.staff_management.models import StaffRole

        repo = self.repository(StaffRole, self.session)
        if not repo.exists(role_id):
            raise RelatedEntityNotFoundError(
                entity_model=StaffRole,
                display_name="role",
                identifier=role_id,
                operation="create",
                detail="Role not found by EntityValidator ",
            )

        return role_id

    def validate_staff_exists(self, staff_id: UUID) -> UUID:  # Cache later
        """Validate that a staff member id exists."""
        from app.core.identity.models.staff import Staff

        repo = self.repository(Staff, self.session)
        if not repo.exists(staff_id):
            raise RelatedEntityNotFoundError(
                entity_model=Staff,
                display_name="staff",
                identifier=staff_id,
                operation="create",
                detail="Staff not found by EntityValidator ",
            )

        return staff_id
