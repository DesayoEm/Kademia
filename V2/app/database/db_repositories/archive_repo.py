from abc import ABC, abstractmethod
from uuid import UUID
from typing import TypeVar, Generic, List, Optional
from ...database.models.common_imports import Base

T = TypeVar('T', bound=Base)

class ArchiveRepo(ABC, Generic[T]):
    """Abstract base class for archive repositories"""

    @abstractmethod
    def get_by_id(self, entity_id: UUID) -> Optional[T]:
        """Get entity by ID"""
        pass

    @abstractmethod
    def get_all(self) -> List[T]:
        """Get all entities"""
        pass

    @abstractmethod
    def restore(self, entity: T) -> T:
        """Restore an archived entity"""
        pass

    @abstractmethod
    def delete(self, entity_id: UUID) -> None:
        """Delete an archived entity"""
        pass


