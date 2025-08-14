from datetime import datetime
from typing import List
from uuid import UUID, uuid4
from sqlalchemy.orm import Session
from app.core.rbac.models import RoleHistory
from app.core.rbac.services.role_change_service import RoleChangeService
from app.core.identity.factories.staff import StaffFactory
from app.core.identity.models.staff import Staff
from app.core.shared.factory.base_factory import BaseFactory
from app.core.shared.validators.entity_validators import EntityValidator
from app.infra.db.repositories.sqlalchemy_repos.base_repo import SQLAlchemyRepository
from app.core.shared.exceptions.decorators.resolve_fk_violation import resolve_fk_on_create, resolve_fk_on_delete
from app.core.shared.exceptions import EntityNotFoundError
from app.core.shared.exceptions.maps.error_map import error_map



class RoleHistoryFactory(BaseFactory):
    """Factory class for managing role history operations."""

    def __init__(self, session: Session, model=RoleHistory, current_user = None):
        super().__init__(current_user)
        """Initialize factory with db session, model, and current actor.
            Args:
                session: SQLAlchemy db session
                model: Model class, defaults to RoleHistory
                current_user: The authenticated user performing the operation, if any.
        """
        self.session = session
        self.model = model
        self.repository = SQLAlchemyRepository(self.model, session)
        self.entity_validator = EntityValidator(session)
        self.error_details = error_map.get(self.model)
        self.entity_model, self.display_name = self.error_details
        self.service = RoleChangeService()
        self.actor_id: UUID = self.get_actor_id()
        self.domain = "role history"

    def raise_not_found(self, identifier, error):
        raise EntityNotFoundError(
            entity_model=self.entity_model,
            identifier=identifier,
            error=str(error),
            display_name=self.display_name
        )

    @resolve_fk_on_create()
    def create_role_change(self, staff_id: UUID, data) -> RoleHistory:
        """Create a new role history.
        Args:
            staff_id: ID of staff to change role history for
            data: role history data containing previous and new level
        Returns:
            RoleHistory: Created role history record
        """
        staff_factory = StaffFactory(self.session, Staff, current_user=self.current_user)
        staff = staff_factory.get_staff(staff_id)

        history = RoleHistory(
            id=uuid4(),
            staff_id = staff.id,
            previous_role=staff.current_role,
            new_role=self.service.prevent_redundant_changes(staff.current_role, data.new_role),
            reason=data.reason,
            changed_at=datetime.now(),
            changed_by_id=self.actor_id
        )
        staff.current_role = history.new_role
        return self.repository.create(history)


    def get_role_change(self, history_id: UUID) -> RoleHistory:
        """Get a specific role history by ID.
        Args:
            history_id (UUID): ID of role history to retrieve
        Returns:
            RoleHistory: Retrieved role history record
        """
        try:
            return self.repository.get_by_id(history_id)
        except EntityNotFoundError as e:
            self.raise_not_found(history_id, e)


    def get_all_role_changes(self, filters) -> List[RoleHistory]:
        """Get all active history with filtering.
        Returns:
            List[RoleHistory]: List of active departments
        """
        fields = ['changed_by', 'staff_id']
        return self.repository.execute_query(fields, filters)
    

    def archive_role_change(self, history_id: UUID, reason) -> RoleHistory:
        """Archive role history .
        Args:
            history_id (UUID): ID of role history to archive
            reason: Reason for archiving
        Returns:
            RoleHistory: Archived role history record
        """
        try:
            return self.repository.archive(history_id, self.actor_id, reason)

        except EntityNotFoundError as e:
            self.raise_not_found(history_id, e)


    @resolve_fk_on_delete(display="role history")
    def delete_role_change(self, history_id: UUID) -> None:
        """Permanently delete a role history if there are no dependent entities.
        Args:
            history_id (UUID): ID of role history to delete
        """
        try:
            self.repository.delete(history_id)

        except EntityNotFoundError as e:
            self.raise_not_found(history_id, e)


    def get_all_archived_role_changes(self, filters) -> List[RoleHistory]:
        """Get all archived role history with filtering.
        Returns:
            List[RoleHistory]: List of archived role history records
        """
        fields = ['changed_by', 'staff_id']
        return self.repository.execute_archive_query(fields, filters)


    def get_archived_role_change(self, history_id: UUID) -> RoleHistory:
        """Get an archived role history by ID.
        Args:
            history_id: ID of role history to retrieve
        Returns:
            RoleHistory: Retrieved role history record
        """
        try:
            return self.repository.get_archive_by_id(history_id)
        except EntityNotFoundError as e:
            self.raise_not_found(history_id, e)


    def restore_role_change(self, history_id: UUID) -> RoleHistory:
        """Restore an archived role history.
        Args:
            history_id: ID of role history to restore
        Returns:
            RoleHistory: Restored role history record
        """
        try:
            return self.repository.restore(history_id)
        except EntityNotFoundError as e:
            self.raise_not_found(history_id, e)


    @resolve_fk_on_delete(display="role history")
    def delete_archived_role_change(self, history_id: UUID) -> None:
        """Permanently delete an archived role history if there are no dependent entities.
        Args:
            history_id: ID of role history to delete
        """
        try:
            self.repository.delete_archive(history_id)

        except EntityNotFoundError as e:
            self.raise_not_found(history_id, e)
