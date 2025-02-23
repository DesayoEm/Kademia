from sqlalchemy.exc import (
    SQLAlchemyError, IntegrityError, OperationalError
)
from sqlalchemy.orm import Session, Query

from V2.app.services.errors.database_errors import (
    UniqueViolationError, EntityNotFoundError, TransactionError, RelationshipError)
from V2.app.services.errors.database_errors import DatabaseError as TKDatabaseError
from uuid import UUID

from typing import Optional, List, Type

from V2.app.database.db_repositories.core_repo import Repository, T


class BaseRepository(Repository[T]):
    def __init__(self, model: Type[T], session: Session):
        super().__init__()
        self.model = model
        self.session = session


    def base_query(self) -> Query:
        return self.session.query(self.model).filter(
            self.model.is_archived == False
        )

class SQLAlchemyRepository(BaseRepository[T]):
    """Core CRUD operations"""

    def create(self, entity: T) -> T:
        try:
            self.session.add(entity)
            self.session.commit()
            self.session.refresh(entity)
            return entity
        except IntegrityError as e:
            self.session.rollback()
            if 'unique constraint' in str(e).lower():
                raise UniqueViolationError(
                    field_name=self._extract_constraint_field(str(e))
                )
            elif 'foreign key constraint' in str(e).lower():
                raise RelationshipError(operation = "create", detail=str(e))
        except OperationalError as e:
            self.session.rollback()
            raise ConnectionError(details=str(e))
        except SQLAlchemyError as e:
            self.session.rollback()
            raise TKDatabaseError(error=str(e))


    def get_by_id(self, id: UUID) -> Optional[T]:
        try:
            entity = self.base_query().filter(
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
            result = self.base_query().all()
            if not result:
                raise EntityNotFoundError(
                    entity_type=self.model.__name__
                )
            return result
        except SQLAlchemyError as e:
            raise TKDatabaseError(error=str(e))


    def update(self, id, updated_entity: T) -> T:
        try:
            existing = self.base_query().filter(self.model.id == id).first()
            if not existing:
                raise EntityNotFoundError(
                    entity_type=self.model.__name__,
                    identifier=str(id)
                )
            self.session.merge(updated_entity)
            self.session.commit()
            self.session.refresh(existing)
            return existing

        except IntegrityError as e:
            self.session.rollback()
            raise UniqueViolationError(
                field_name=self._extract_constraint_field(str(e)))
        except SQLAlchemyError as e:
            self.session.rollback()
            raise TKDatabaseError(error=str(e))


    def archive(self, id, archived_by_id, reason) -> T:
        try:
            entity = self.base_query().filter(
                self.model.id == id
            ).first()
            if not entity:
                raise EntityNotFoundError(
                    entity_type=self.model.__name__,
                    identifier=str(id)
                )

            entity.archive(archived_by_id, reason)
            self.session.commit()
            self.session.refresh(entity)
            return entity
        except SQLAlchemyError as e:
            self.session.rollback()
            raise TKDatabaseError(error=str(e))


    def delete(self, id: UUID) -> None:
        try:
            entity = self.base_query().filter(
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