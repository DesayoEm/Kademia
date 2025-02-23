from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Optional
from uuid import UUID
from ...database.models.common_imports import Base
from ...database.models.data_enums import ArchiveReason

T = TypeVar('T', bound=Base)


class Repository(ABC, Generic[T]):
    @abstractmethod
    def create(self, entity: T) -> T:
        pass

    @abstractmethod
    def get_by_id(self, entity_id: UUID) -> Optional[T]:
        pass

    @abstractmethod
    def get_all(self) -> List[T]:
        pass

    @abstractmethod
    def update(self, id: UUID, updated_entity: T) -> T:
        pass

    @abstractmethod
    def archive(self, id: UUID, archived_by_id: UUID, reason: ArchiveReason) -> T:
        pass

    @abstractmethod
    def delete(self, entity_id: UUID) -> None:
        pass