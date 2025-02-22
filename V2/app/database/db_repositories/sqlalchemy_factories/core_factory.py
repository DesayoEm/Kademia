from abc import ABC, abstractmethod
from sqlalchemy.exc import (
    SQLAlchemyError, IntegrityError, DatabaseError, OperationalError, StatementError
)

from V2.app.services.errors.database_errors import (
    UniqueViolationError, EntityNotFoundError, TransactionError, RelationshipError)
from V2.app.services.errors.database_errors import DatabaseError as TKDatabaseError
from uuid import UUID
from typing import Optional, List
from V2.app.database.db_repositories.template_factory import Repository, T

class BaseRepository(Repository[T]):
    def __init__(self, session_factory, model):
        self.session_factory = session_factory
        self.model = model

    def _base_query(self, session):
        return session.query(self.model).filter(
            self.model.is_archived == False
        )


class SQLAlchemyRepository(BaseRepository[T]):
    """Core CRUD operations"""

    def create(self, entity: T) -> T:
        try:
            with self.session_factory() as session:
                session.add(entity)
                session.commit()
                session.refresh(entity)
                return entity
        except IntegrityError as e:
            session.rollback()  # Added missing rollback
            if 'unique constraint' in str(e).lower():
                raise UniqueViolationError(
                    field_name=self._extract_constraint_field(str(e))
                )
            elif 'foreign key constraint' in str(e).lower():
                raise RelationshipError(details=str(e))
            raise # Re-raise if not handled
        except OperationalError as e:
            session.rollback()
            raise ConnectionError(details=str(e))
        except SQLAlchemyError as e:
            session.rollback()
            raise TKDatabaseError(str(e))


    def get_by_id(self, id: UUID) -> Optional[T]:
        try:
            with self.session_factory() as session:
                entity = self._base_query(session).filter_by(id=id).first()
                if not entity:
                    raise EntityNotFoundError(
                        entity_type=self.model.__name__,
                        identifier=str(id)
                    )
                return entity
        except SQLAlchemyError as e:
            raise TKDatabaseError(str(e))

    def get_all(self) -> List[T]:
        try:
            with self.session_factory() as session:
                result = self._base_query(session).all()  # Fixed redundant query
                if not result:
                    raise EntityNotFoundError(
                        entity_type=self.model.__name__
                    )
                return result
        except SQLAlchemyError as e:
            raise TKDatabaseError(str(e))


    def update(self, id: UUID, updated_data: dict) -> T:
        try:
            with self.session_factory() as session:
                existing = self._base_query(session).filter_by(id=id).first()  # Use base query
                if not existing:
                    raise EntityNotFoundError(self.model.__name__)

                for key, value in updated_data.items():
                    if hasattr(existing, key):
                        setattr(existing, key, value)

                session.commit()
                session.refresh(existing)
                return existing
        except IntegrityError as e:
            session.rollback()
            raise UniqueViolationError(field_name="field")
        except SQLAlchemyError as e:
            session.rollback()
            raise TKDatabaseError(str(e))

    def archive(self, id: UUID) -> T:
        try:
            with self.session_factory() as session:
                entity = self._base_query(session).filter_by(id=id).first()  # Use base query
                if not entity:
                    raise EntityNotFoundError(self.model.__name__)

                entity.is_archived = True
                session.commit()
                session.refresh(entity)
                return entity
        except SQLAlchemyError as e:
            session.rollback()
            raise TKDatabaseError(str(e))

    def delete(self, id: UUID) -> None:
        try:
            with self.session_factory() as session:
                entity = self._base_query(session).filter_by(id=id).first()  # Use base query
                if not entity:
                    raise EntityNotFoundError(self.model.__name__)

                session.delete(entity)
                session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise TKDatabaseError(str(e))