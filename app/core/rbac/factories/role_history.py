from datetime import datetime
from typing import List
from uuid import UUID, uuid4
from sqlalchemy.orm import Session
from app.core.rbac.models import RoleHistory
from app.core.rbac.services.role_service import RBACService
from app.core.identity.factories.staff import StaffFactory
from app.core.identity.models.staff import Staff
from app.core.shared.factory.base_factory import BaseFactory
from app.core.shared.validators.entity_validators import EntityValidator
from app.infra.db.repositories.sqlalchemy_repos.base_repo import SQLAlchemyRepository
from app.core.shared.exceptions.decorators.resolve_fk_violation import (
    resolve_fk_on_create,
    resolve_fk_on_delete,
)
from app.core.shared.exceptions import EntityNotFoundError
from app.core.shared.exceptions.maps.error_map import error_map


class RoleHistoryFactory(BaseFactory):
    """
    Factory for managing staff role change history records.

    Handles creation and retrieval of role change audit records, which track
    when staff members are assigned new roles, who authorized the change, and
    why. Also updates the staff member's current_role_id when a new role change
    is recorded.

    Supports soft-delete (archive) for historical records that need to be
    hidden but preserved for compliance.

    Attributes:
        session: SQLAlchemy database session.
        model: The RoleHistory model class.
        repository: SQLAlchemyRepository instance for database operations.
        entity_validator: Validates entity relationships and references.
        service: RBACService for role-specific business logic.
        actor_id: UUID of the current user performing operations (for audit).
        domain: String identifier for this factory's domain ("role history").

    Example:
        factory = RoleHistoryFactory(session, current_user=admin_user)
        change = factory.create_role_change(
            staff_id=teacher.id,
            data=RoleChangeSchema(new_role_id=admin_role.id, reason="Promotion")
        )
    """

    def __init__(self, session: Session, model=RoleHistory, current_user=None):
        """
        Initialize the RoleHistoryFactory with database session and optional authenticated user.

        Args:
            session: SQLAlchemy database session for all operations.
            model: The model class to operate on. Defaults to RoleHistory.
            current_user: The authenticated user performing operations. Used to
                populate the changed_by_id audit field. Can be None for system
                operations.
        """
        super().__init__(current_user)

        self.session = session
        self.model = model
        self.repository = SQLAlchemyRepository(self.model, session)
        self.entity_validator = EntityValidator(session)
        self.error_details = error_map.get(self.model)
        self.entity_model, self.display_name = self.error_details
        self.service = RBACService(self.session)
        self.actor_id: UUID = self.get_actor_id()
        self.domain = "role history"

    def raise_not_found(self, identifier, error):
        """
        Raise a standardized EntityNotFoundError for role history lookups.

        Args:
            identifier: The history record ID that was not found.
            error: The original exception to include in the error message.

        Raises:
            EntityNotFoundError: Always raised with role history-specific context.
        """
        raise EntityNotFoundError(
            entity_model=self.entity_model,
            identifier=identifier,
            error=str(error),
            display_name=self.display_name,
        )

    @resolve_fk_on_create()
    def create_role_change(self, staff_id: UUID, data) -> RoleHistory:
        """
        Record a role change for a staff member and update their current role.

        Creates a RoleHistory audit record capturing the previous role, new role,
        reason for change, and who authorized it. Also updates the staff member's
        current_role_id to reflect the new assignment.

        Args:
            staff_id: UUID of the staff member whose role is changing.
            data: Schema object containing:
                - new_role_id: UUID of the role to assign.
                - reason: Required explanation for the role change.

        Returns:
            RoleHistory: The newly created audit record.

        Raises:
            EntityNotFoundError: If the staff member doesn't exist.
            RedundantChangeError: If new_role_id matches current role (via
                service.prevent_redundant_changes).
            ForeignKeyViolationError: If new_role_id references a non-existent
                role (handled by @resolve_fk_on_create decorator).

        Side Effects:
            Updates staff.current_role_id to the new role.
        """
        staff_factory = StaffFactory(
            self.session, Staff, current_user=self.current_user
        )
        staff = staff_factory.get_staff(staff_id)

        history = RoleHistory(
            id=uuid4(),
            staff_id=staff.id,
            previous_role_id=staff.current_role_id,
            new_role_id=self.service.prevent_redundant_changes(
                staff.current_role_id, data.new_role_id
            ),
            change_reason=data.reason,
            changed_at=datetime.now(),
            changed_by_id=self.actor_id,
        )
        staff.current_role_id = history.new_role_id
        return self.repository.create(history)

    def get_role_change(self, history_id: UUID) -> RoleHistory:
        """
        Retrieve a specific role history record by its UUID.

        Args:
            history_id: The UUID of the history record to retrieve.

        Returns:
            RoleHistory: The requested audit record.

        Raises:
            EntityNotFoundError: If no record exists with the given ID.
        """
        try:
            return self.repository.get_by_id(history_id)
        except EntityNotFoundError as e:
            self.raise_not_found(history_id, e)

    def get_all_role_changes(self, filters) -> List[RoleHistory]:
        """
        Retrieve all active (non-archived) role history records with optional filtering.

        Args:
            filters: Filter parameters for the query. Supports filtering by
                changed_by (who made the change) and staff_id (whose role changed).

        Returns:
            List[RoleHistory]: List of matching role history records.
        """
        fields = ["changed_by", "staff_id"]
        return self.repository.execute_query(fields, filters)

    def archive_role_change(self, history_id: UUID, reason) -> RoleHistory:
        """
        Soft-delete a role history record by moving it to archived state.

        Archived records are hidden from normal queries but preserved for
        compliance and audit purposes.

        Args:
            history_id: The UUID of the history record to archive.
            reason: Required explanation for why the record is being archived.

        Returns:
            RoleHistory: The archived record.

        Raises:
            EntityNotFoundError: If no record exists with the given ID.
        """
        try:
            return self.repository.archive(history_id, self.actor_id, reason)

        except EntityNotFoundError as e:
            self.raise_not_found(history_id, e)

    @resolve_fk_on_delete(display="role history")
    def delete_role_change(self, history_id: UUID) -> None:
        """
        Permanently delete a role history record from the database.

        This is a hard delete—the record cannot be recovered. Use
        archive_role_change() for soft-delete behavior. Generally discouraged
        for audit records.

        Args:
            history_id: The UUID of the history record to delete.

        Raises:
            EntityNotFoundError: If no record exists with the given ID.
            ForeignKeyViolationError: If other entities reference this record
                (handled by @resolve_fk_on_delete decorator).
        """
        try:
            self.repository.delete(history_id)

        except EntityNotFoundError as e:
            self.raise_not_found(history_id, e)

    def get_all_archived_role_changes(self, filters) -> List[RoleHistory]:
        """
        Retrieve all archived role history records with optional filtering.

        Args:
            filters: Filter parameters for the query. Supports filtering by
                changed_by and staff_id.

        Returns:
            List[RoleHistory]: List of archived records matching the filters.
        """
        fields = ["changed_by", "staff_id"]
        return self.repository.execute_archive_query(fields, filters)

    def get_archived_role_change(self, history_id: UUID) -> RoleHistory:
        """
        Retrieve a specific archived role history record by ID.

        Args:
            history_id: The UUID of the archived record to retrieve.

        Returns:
            RoleHistory: The archived record.

        Raises:
            EntityNotFoundError: If no archived record exists with the given ID.
        """
        try:
            return self.repository.get_archive_by_id(history_id)
        except EntityNotFoundError as e:
            self.raise_not_found(history_id, e)

    def restore_role_change(self, history_id: UUID) -> RoleHistory:
        """
        Restore an archived role history record to active state.

        Args:
            history_id: The UUID of the archived record to restore.

        Returns:
            RoleHistory: The restored record (now active).

        Raises:
            EntityNotFoundError: If no archived record exists with the given ID.
        """
        try:
            return self.repository.restore(history_id)
        except EntityNotFoundError as e:
            self.raise_not_found(history_id, e)

    @resolve_fk_on_delete(display="role history")
    def delete_archived_role_change(self, history_id: UUID) -> None:
        """
        Permanently delete an archived role history record from the database.

        Args:
            history_id: The UUID of the archived record to delete.

        Raises:
            EntityNotFoundError: If no archived record exists with the given ID.
            ForeignKeyViolationError: If other entities reference this record
                (handled by @resolve_fk_on_delete decorator).
        """
        try:
            self.repository.delete_archive(history_id)

        except EntityNotFoundError as e:
            self.raise_not_found(history_id, e)
