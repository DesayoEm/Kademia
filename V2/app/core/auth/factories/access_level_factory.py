from datetime import datetime
from typing import List
from uuid import UUID, uuid4
from sqlalchemy.orm import Session
from V2.app.core.auth.models.auth import AccessLevelChange
from V2.app.core.auth.validators.access_level import AccessLevelValidator
from V2.app.core.identity.factories.staff import StaffFactory
from V2.app.core.identity.models.staff import Staff
from V2.app.core.shared.factory.base_factory import BaseFactory
from V2.app.core.shared.validators.entity_validators import EntityValidator
from V2.app.infra.db.repositories.sqlalchemy_repos.base_repo import SQLAlchemyRepository
from V2.app.core.shared.exceptions.decorators.resolve_fk_violation import resolve_fk_on_create, resolve_fk_on_delete
from V2.app.core.shared.exceptions import EntityNotFoundError
from V2.app.core.shared.exceptions.maps.error_map import error_map



class AccessLevelChangeFactory(BaseFactory):
    """Factory class for managing access level operations."""

    def __init__(self, session: Session, model=AccessLevelChange, current_user = None):
        super().__init__(current_user)
        """Initialize factory with db session and current actor.
            Args:
                session: SQLAlchemy db session
                model: Model class, defaults to AccessLevelChange
        """
        self.session = session
        self.model = model
        self.repository = SQLAlchemyRepository(self.model, session)
        self.entity_validator = EntityValidator(session)
        self.error_details = error_map.get(self.model)
        self.entity_model, self.display_name = self.error_details
        self.validator = AccessLevelValidator()
        self.actor_id: UUID = self.get_actor_id()
        self.domain = "Level Change"

    def raise_not_found(self, identifier, error):
        raise EntityNotFoundError(
            entity_model=self.entity_model,
            identifier=identifier,
            error=str(error),
            display_name=self.display_name
        )

    @resolve_fk_on_create()
    def create_level_change(self, staff_id: UUID, data) -> AccessLevelChange:
        """Create a new access level.
        Args:
            staff_id: ID of staff to change access level for
            data: Level change data containing previous and new level
        Returns:
            AccessLevelChange: Created level change record
        """
        staff_factory = StaffFactory(self.session, Staff)
        staff = staff_factory.get_staff(staff_id)

        level_change = AccessLevelChange(
            id=uuid4(),
            staff_id = staff.id,
            previous_level=staff.access_level,
            new_level=self.validator.prevent_redundant_changes(staff.access_level, data.new_level),
            reason=data.reason,
            changed_at=datetime.now(),
            changed_by_id=self.actor_id
        )
        staff.access_level = level_change.new_level
        return self.repository.create(level_change)


    def get_level_change(self, level_change_id: UUID) -> AccessLevelChange:
        """Get a specific level change by ID.
        Args:
            level_change_id (UUID): ID of level change to retrieve
        Returns:
            AccessLevelChange: Retrieved level change record
        """
        try:
            return self.repository.get_by_id(level_change_id)
        except EntityNotFoundError as e:
            self.raise_not_found(level_change_id, e)


    def get_all_level_changes(self, filters) -> List[AccessLevelChange]:
        """Get all active departments with filtering.
        Returns:
            List[AccessLevelChange]: List of active departments
        """
        fields = ['changed_by']
        return self.repository.execute_query(fields, filters)
    

    def archive_level_change(self, level_change_id: UUID, reason) -> AccessLevelChange:
        """Archive an access level .
        Args:
            level_change_id (UUID): ID of level change to archive
            reason: Reason for archiving
        Returns:
            AccessLevelChange: Archived level change record
        """
        try:
            return self.repository.archive(level_change_id, self.actor_id, reason)

        except EntityNotFoundError as e:
            self.raise_not_found(level_change_id, e)


    @resolve_fk_on_delete()
    def delete_level_change(self, level_change_id: UUID) -> None:
        """Permanently delete an access level if there are no dependent entities.
        Args:
            level_change_id (UUID): ID of level change to delete
        """
        try:
            self.repository.delete(level_change_id)

        except EntityNotFoundError as e:
            self.raise_not_found(level_change_id, e)


    def get_all_archived_level_changes(self, filters) -> List[AccessLevelChange]:
        """Get all archived departments with filtering.
        Returns:
            List[AccessLevelChange]: List of archived level change records
        """
        fields = ['changed_by']
        return self.repository.execute_archive_query(fields, filters)


    def get_archived_level_change(self, level_change_id: UUID) -> AccessLevelChange:
        """Get an archived level change by ID.
        Args:
            level_change_id: ID of level change to retrieve
        Returns:
            AccessLevelChange: Retrieved level change record
        """
        try:
            return self.repository.get_archive_by_id(level_change_id)
        except EntityNotFoundError as e:
            self.raise_not_found(level_change_id, e)


    def restore_level_change(self, level_change_id: UUID) -> AccessLevelChange:
        """Restore an archived department.
        Args:
            level_change_id: ID of level change to restore
        Returns:
            AccessLevelChange: Restored level change record
        """
        try:
            return self.repository.restore(level_change_id)
        except EntityNotFoundError as e:
            self.raise_not_found(level_change_id, e)


    def delete_archived_level_change(self, level_change_id: UUID) -> None:
        """Permanently delete an archived level change if there are no dependent entities.
        Args:
            level_change_id: ID of level change to delete
        """
        try:
            self.repository.delete_archive(level_change_id)

        except EntityNotFoundError as e:
            self.raise_not_found(level_change_id, e)
