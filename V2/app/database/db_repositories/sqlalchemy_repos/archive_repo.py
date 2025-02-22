from abc import ABC, abstractmethod
from typing import Optional, List, Type, Callable
from uuid import UUID
from sqlalchemy.orm import Session
from V2.app.services.errors.database_errors import DatabaseError as TKDatabaseError
from V2.app.services.errors.database_errors import (
    UniqueViolationError, EntityNotFoundError, TransactionError, RelationshipError)
from sqlalchemy.exc import (
    SQLAlchemyError, IntegrityError, OperationalError
)
from V2.app.database.db_repositories.archive_repo import ArchiveRepo, T


class ArchiveRepository(ArchiveRepo[T]):
    def __init__(self, model: Type[T], session: Session):
        self.session = session
        self.model = model

    def base_archive_query(self):
        return self.session.query(self.model).filter(
            self.model.is_archived == True
        )


class SqlAlchemyArchiveRepository(ArchiveRepository[T]):
    """Archive CRUD operations"""
    def get_by_id(self, id: UUID) -> Optional[T]:
        try:
            entity = self.base_archive_query().filter(
                self.model.id == id
            ).first()
            if not entity:
                raise EntityNotFoundError(
                    entity_type=self.model.__name__,
                    identifier=str(id)
                )
            return entity
        except SQLAlchemyError as e:
            raise TKDatabaseError(error=str(e))


    def get_all(self) -> List[T]:
        try:
            result = self.base_archive_query().all()
            if not result:
                raise EntityNotFoundError(
                    entity_type=self.model.__name__
                )
            return result
        except SQLAlchemyError as e:
            raise TKDatabaseError(error=str(e))


    def restore(self, id: UUID) -> T:
        try:
            entity = self.base_archive_query().filter(
                self.model.id == id
            ).first()
            if not entity:
                raise EntityNotFoundError(
                    entity_type=self.model.__name__,
                    identifier=str(id)
                )
            entity.is_archived = False
            self.session.commit()
            return entity
        except SQLAlchemyError as e:
            self.session.rollback()
            raise TKDatabaseError(error=str(e))


    def delete(self, id:UUID):
        try:
            entity = self.base_archive_query().filter(
                self.model.id == id).first()
            if not entity:
                raise EntityNotFoundError(
                    entity_type=self.model.__name__,
                    identifier=str(id)
                )
            self.session.delete(entity)
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            raise TKDatabaseError(error=str(e))




