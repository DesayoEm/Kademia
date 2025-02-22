from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Optional
from uuid import UUID
from ...database.models.common_imports import Base

T = TypeVar('T', bound=Base)

class Repository(ABC, Generic[T]):
    """Abstract base class for repositories"""

    @abstractmethod
    def create(self, entity: T) -> T:
        """Create a new entity"""
        pass

    @abstractmethod
    def get_by_id(self, entity_id: UUID) -> Optional[T]:
        """Get entity by ID"""
        pass

    @abstractmethod
    def get_all(self) -> List[T]:
        """Get all entities"""
        pass

    @abstractmethod
    def update(self, entity: T) -> T:
        """Update an entity"""
        pass

    @abstractmethod
    def archive(self, entity: T) -> T:
        """Update an entity"""
        pass

    @abstractmethod
    def delete(self, entity_id: UUID) -> None:
        """Delete an entity"""
        pass