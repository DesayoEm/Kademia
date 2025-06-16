from typing import List
from uuid import UUID
from sqlalchemy.orm import Session

from V2.app.core.shared.factory.base_factory import BaseFactory
from V2.app.infra.db.repositories.sqlalchemy_repos.base_repo import SQLAlchemyRepository
from V2.app.core.identity.models.staff import Educator
from ...shared.exceptions.maps.error_map import error_map
from ...shared.exceptions import EntityNotFoundError



class EducatorFactory(BaseFactory):
    """Factory class for managing educator operations."""

    def __init__(self, session: Session, model = Educator, current_user = None):
        super().__init__(current_user)
        """Initialize factory with db session, model and current actor.
            Args:
                session: SQLAlchemy db session
                model: Model class, defaults to Educator
                current_user: The authenticated user performing the operation, if any.
        """

        self.model = model
        self.repository = SQLAlchemyRepository(self.model, session)
        self.error_details = error_map.get(self.model)
        self.entity_model, self.display_name = self.error_details
        self.actor_id: UUID = self.get_actor_id()
        self.domain = "Educator"

    def raise_not_found(self, identifier, error):
        raise EntityNotFoundError(
            entity_model=self.entity_model,
            identifier=identifier,
            error=str(error),
            display_name=self.display_name
        )

    
    def get_educator(self, educator_id: UUID) -> Educator:
        """Get a specific educator by ID.
        Args:
            educator_id (UUID): ID of educator to retrieve
        Returns:
            Educator: Retrieved educator record
        """
        try:
            return self.repository.get_by_id(educator_id)

        except EntityNotFoundError as e:
            raise EntityNotFoundError(
                entity_model=self.entity_model, identifier=educator_id, error=str(e),
                display_name=self.display_name
            )

    def get_all_educators(self, filters) -> List[Educator]:
        """Get all active educator with filtering.
        Returns:
            List[Educator]: List of active educators
        """
        fields = ['name', 'educator_type']
        return self.repository.execute_query(fields, filters)


    def get_all_archived_educators(self, filters) -> List[Educator]:
        """Get all archived educator with filtering.
        Returns:
            List[Educator]: List of archived educator records
        """
        fields = ['name', 'educator_type']
        return self.repository.execute_archive_query(fields, filters)


    def get_archived_educator(self, educator_id: UUID) -> Educator:
        """Get an archived educator by ID.
        Args:
            educator_id: ID of educator to retrieve
        Returns:
            Educator: Retrieved educator record
        """
        try:
            return self.repository.get_archive_by_id(educator_id)

        except EntityNotFoundError as e:
            self.raise_not_found(educator_id, e)


    def restore_educator(self, educator_id: UUID) -> Educator:
        """Restore an archived educator.
        Args:
            educator_id: ID of educator to restore
        Returns:
            Educator: Restored educator record
        """
        try:
            return self.repository.restore(educator_id)

        except EntityNotFoundError as e:
            self.raise_not_found(educator_id, e)
