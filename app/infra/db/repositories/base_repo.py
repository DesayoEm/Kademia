from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Optional
from uuid import UUID
from app.core.shared.models.common_imports import Base


T = TypeVar('T', bound=Base)


class Repository(ABC, Generic[T]):
    """
    Abstract base class defining the interface for repository operations.
    Handles both active and archived entity operations.
    """

    @abstractmethod
    def create(self, entity: T) -> T:
        """
        Create a new entity in the db.
        Args:
            entity: The entity to create
        Returns:
            The created entity with populated ID and timestamps
        """
        pass

    @abstractmethod
    def exists(self, entity_id: UUID) -> bool:
        """
        Check if an active (non-archived) entity exists in the db.
        Args:
            entity_id (UUID): The unique identifier of the entity to check.
        Returns:
            bool: True if the entity exists and is active, False otherwise.
        """
        pass

    @abstractmethod
    def get_by_id(self, entity_id: UUID) -> Optional[T]:
        """
        Retrieve an active entity by its ID.
        Args:
            entity_id: The UUID of the entity to retrieve
        Returns:
            The entity if found, None otherwise
        """
        pass

    @abstractmethod
    def apply_filters(self, query, fields: List, filters):
        """
        Apply filters to a query for active entities.
        Args:
            query: The base query to filter
            fields: List of fields that support text search
            filters: Filter parameters
        Returns:
            The filtered query
        """
        pass

    @abstractmethod
    def execute_query(self, fields, filters) -> List[T]:
        """
        Execute a query for active entities with filtering, sorting, and pagination.
        Args:
            fields: List of fields that support text search
            filters: Filter, sorting, and pagination parameters
        Returns:
            List of entities matching the query
        """
        pass

    @abstractmethod
    def update(self, entity_id: UUID, updated_entity: T) -> T:
        """
        Update an existing active entity.
        Args:
            entity_id: The UUID of the entity to update
            updated_entity: The entity with updated values
        Returns:
            The updated entity
        """
        pass

    @abstractmethod
    def archive(self, entity_id: UUID, archived_by_id: UUID, reason) -> T:
        """
        Archive an active entity (soft delete).
        Args:
            entity_id: The UUID of the entity to archive
            archived_by_id: The UUID of the users performing the archive
            reason: The reason for archiving
        Returns:
            The archived entity
        """
        pass

    @abstractmethod
    def delete(self, entity_id: UUID) -> None:
        """
        Permanently delete an active entity.
        Args:
            entity_id: The UUID of the entity to delete
        """
        pass

    @abstractmethod
    def get_archive_by_id(self, entity_id: UUID) -> Optional[T]:
        """
        Retrieve an archived entity by its ID.
        Args:
            entity_id: The UUID of the archived entity to retrieve
        Returns:
            The archived entity if found, None otherwise
        """
        pass


    @abstractmethod
    def execute_archive_query(self, fields, filters) -> List[T]:
        """
        Execute a query for archived entities with filtering, sorting, and pagination.
        Args:
            fields: List of fields that support text search
            filters: Filter, sorting, and pagination parameters
        Returns:
            List of archived entities matching the query
        """
        pass

    @abstractmethod
    def restore(self, entity_id: UUID) -> T:
        """
        Restore an archived entity to active status.
        Args:
            entity_id: The UUID of the archived entity to restore
        Returns:
            The restored entity
        """
        pass

    @abstractmethod
    def delete_archive(self, entity_id: UUID) -> None:
        """
        Permanently delete an archived entity.
        Args:
            entity_id: The UUID of the archived entity to delete
        """
        pass