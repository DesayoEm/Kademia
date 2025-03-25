from uuid import UUID
from typing import Optional, List, Type
from sqlalchemy import or_, desc, asc
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, OperationalError
from sqlalchemy.orm import Session, Query
from ....core.errors.database_errors import (
    UniqueViolationError, EntityNotFoundError, RelationshipError, DBConnectionError)
from ....core.errors.database_errors import DatabaseError as TKDatabaseError
from ....database.db_repositories.main_repo import Repository, T


class BaseRepository(Repository[T]):
    """Base repository class that implements common query functionality."""

    def __init__(self, model: Type[T], session: Session):
        """Initialize the repository with a model and session.
        Args:
            model: The SQLAlchemy model class
            session: The SQLAlchemy database session
        """
        super().__init__()
        self.model = model
        self.session = session

    def active_query(self) -> Query:
        """Get a base query for active (non-archived) entities.
        Returns:
            Query: SQLAlchemy query filtered to non-archived entities
        """
        return self.session.query(self.model).filter(
            self.model.is_archived == False
        )

    def archive_query(self) -> Query:
        """Get a base query for archived entities.
        Returns:
            Query: SQLAlchemy query filtered to archived entities
        """
        return self.session.query(self.model).filter(
            self.model.is_archived == True
        )

class SQLAlchemyRepository(BaseRepository[T]):
    """Repository implementation for SQLAlchemy with combined active and archive operations."""

    def create(self, entity: T) -> T:
        """Create a new entity in the database.

        Args:
            entity: The entity to create
        Returns:
            T: The created entity with updated ID and timestamps
        Raises:
            UniqueViolationError: If the entity violates a unique constraint
            RelationshipError: If the entity violates a foreign key constraint
            ConnectionError: If there is a database connection issue
            TKDatabaseError: For other database errors
        """
        try:
            self.session.add(entity)
            self.session.commit()
            self.session.refresh(entity)
            return entity
        except IntegrityError as e:
            self.session.rollback()
            details = str(e).lower()
            if 'unique constraint' in details:
                raise UniqueViolationError(error= details)
            elif 'foreign key constraint' in details:
                raise RelationshipError(operation = "create", error=str(e), entity ='Unknown')
            else:
                raise TKDatabaseError(error=f"Database integrity error: {details}")
        except OperationalError as e:
            self.session.rollback()
            raise DBConnectionError(error=str(e))
        except SQLAlchemyError as e:
            self.session.rollback()
            raise TKDatabaseError(error=str(e))


    def get_by_id(self, id: UUID) -> Optional[T]:
        """Get an active entity by its ID.
        Args:
            id: The UUID of the entity to retrieve
        Returns:
            T: The retrieved entity
        Raises:
            EntityNotFoundError: If no active entity with the given ID exists
            TKDatabaseError: For other database errors
        """
        try:
            entity = self.active_query().filter(
                self.model.id == id).first()
            if not entity:
                raise EntityNotFoundError(
                    entity_type=self.model.__name__,
                    identifier=str(id), error = 'Record not found')
            return entity
        except SQLAlchemyError as e:
            raise TKDatabaseError(error=str(e))


    def apply_filters(self, query: Query, fields: List, filters) -> Query:
        """Apply filters to a query based on the provided filter parameters.

        Args:
            query: The base SQLAlchemy query
            fields: List of fields that support text search
            filters: Filter parameters

        Returns:
            Query: The filtered SQLAlchemy query
        """
        for field, value in filters.model_dump(exclude_unset=True).items():
            if field in ['limit', 'offset', 'order_by', 'order_dir']:
                continue
            if value is not None and hasattr(self.model, field):
                if isinstance(value, str) and field in fields:
                    query = query.filter(getattr(self.model, field).ilike(f"%{value}%"))
                else:
                    query = query.filter(getattr(self.model, field) == value)

        return query


    def execute_query(self, fields, filters) -> List[T]:
        """Execute a query for active entities with sorting and pagination.

        Args:
            fields: List of fields that support text search
            filters: Filter, sorting, and pagination parameters
        Returns:
            List[T]: List of entities matching the query parameters
        Raises:
            TKDatabaseError: For database errors
        """
        try:
            query = self.active_query()
            query = self.apply_filters(query, fields, filters)


            order_by = getattr(filters, 'order_by', 'created_at')
            order_dir = getattr(filters, 'order_dir', 'asc')
            if order_by and hasattr(self.model, order_by):
                order_func = desc if order_dir == 'desc' else asc
                query = query.order_by(order_func(getattr(self.model, order_by)))

            limit = getattr(filters, 'limit', 100)
            offset = getattr(filters, 'offset', 0)

            result = query.offset(offset).limit(limit).all()

            if not result:
                return []
            return result

        except SQLAlchemyError as e:
            raise TKDatabaseError(error=str(e))


    def update(self, id, updated_entity: T) -> T:
        """Update an existing active entity.

        Args:
            id: The UUID of the entity to update
            updated_entity: The entity with updated values
        Returns:
            T: The updated entity
        Raises:
            EntityNotFoundError: If no active entity with the given ID exists
            UniqueViolationError: If the update violates a unique constraint
            TKDatabaseError: For other database errors
        """
        try:
            existing = self.active_query().filter(self.model.id == id).first()
            if not existing:
                raise EntityNotFoundError(
                    entity_type=self.model.__name__,
                    identifier=str(id),
                    error = 'object not found'
                )
            self.session.merge(updated_entity)
            self.session.commit()
            self.session.refresh(existing)
            return existing

        except IntegrityError as e:
            self.session.rollback()
            details = str(e).lower()
            if 'unique constraint' in details:
                raise UniqueViolationError(error=details)
            elif 'foreign key constraint' in str(e).lower():
                raise RelationshipError(operation="create", error=str(e), entity ='Unknown')
        except SQLAlchemyError as e:
            self.session.rollback()
            raise TKDatabaseError(error=str(e))


    def archive(self, id, archived_by_id, reason) -> T:
        """Archive an active entity.

        Args:
            id: The UUID of the entity to archive
            archived_by_id: The UUID of the users performing the archive
            reason: The reason for archiving
        Returns:
            T: The archived entity
        Raises:
            EntityNotFoundError: If no active entity with the given ID exists
            TKDatabaseError: For other database errors
        """
        try:
            entity = self.active_query().filter(
                self.model.id == id
            ).first()
            if not entity:
                raise EntityNotFoundError(
                    entity_type=self.model.__name__,
                    identifier=str(id),
                    error='object not found'
                )

            entity.archive(archived_by_id, reason)
            self.session.commit()
            self.session.refresh(entity)
            return entity
        except SQLAlchemyError as e:
            self.session.rollback()
            raise TKDatabaseError(error=str(e))


    def delete(self, id: UUID) -> None:
        """Permanently delete an active entity.
        Args:
            id: The UUID of the entity to delete
        Raises:
            EntityNotFoundError: If no active entity with the given ID exists
            TKDatabaseError: For other database errors
        """
        try:
            entity = self.active_query().filter(
                self.model.id == id).first()
            if not entity:
                raise EntityNotFoundError(
                    entity_type=self.model.__name__,
                    identifier=str(id),
                    error='object not found'
                )

            self.session.delete(entity)
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            raise TKDatabaseError(error=str(e))

    def get_archive_by_id(self, id: UUID) -> Optional[T]:
        """Get an archived entity by its ID.

        Args:
            id: The UUID of the archived entity to retrieve
        Returns:
            T: The retrieved archived entity
        Raises:
            EntityNotFoundError: If no archived entity with the given ID exists
            TKDatabaseError: For other database errors
        """
        try:
            entity = self.archive_query().filter(
                self.model.id == id
            ).first()
            if not entity:
                raise EntityNotFoundError(
                    entity_type=self.model.__name__,
                    identifier=str(id),
                    error='object not found'
                )
            return entity
        except SQLAlchemyError as e:
            raise TKDatabaseError(error=str(e))


    def apply_archive_filters(self, query: Query, fields: List, filters) -> Query:
        """Apply filters to a query for archived entities.

        Args:
            query: The base SQLAlchemy query
            fields: List of fields that support text search
            filters: Filter parameters
        Returns:
            Query: The filtered SQLAlchemy query
        """
        for field, value in filters.model_dump(exclude_unset=True).items():
            if field in ['limit', 'offset', 'order_by', 'order_dir']:
                continue
            if value is not None and hasattr(self.model, field):
                if isinstance(value, str) and field in fields:
                    query = query.filter(getattr(self.model, field).ilike(f"%{value}%"))
                else:
                    query = query.filter(getattr(self.model, field) == value)
        return query


    def execute_archive_query(self, fields, filters) -> List[T]:
        """Execute a query for archived entities with sorting and pagination.

        Args:
            fields: List of fields that support text search
            filters: Filter, sorting, and pagination parameters
        Returns:
            List[T]: List of archived entities matching the query parameters
        Raises:
            TKDatabaseError: For database errors
        """
        try:
            query = self.archive_query()
            query = self.apply_filters(query, fields, filters)

            order_by = getattr(filters, 'order_by', 'created_at')
            order_dir = getattr(filters, 'order_dir', 'asc')
            if order_by and hasattr(self.model, order_by):
                order_func = desc if order_dir == 'desc' else asc
                query = query.order_by(order_func(getattr(self.model, order_by)))
            limit = getattr(filters, 'limit', 100)
            offset = getattr(filters, 'offset', 0)

            result = query.offset(offset).limit(limit).all()
            if not result:
                return []
            return result

        except SQLAlchemyError as e:
            raise TKDatabaseError(error=str(e))


    def restore(self, id: UUID) -> T:
        """Restore an archived entity to active status.

        Args:
            id: The UUID of the archived entity to restore
        Returns:
            T: The restored entity
        Raises:
            EntityNotFoundError: If no archived entity with the given ID exists
            TKDatabaseError: For other database errors
        """
        try:
            entity = self.archive_query().filter(
                self.model.id == id
            ).first()
            if not entity:
                raise EntityNotFoundError(
                    entity_type=self.model.__name__,
                    identifier=str(id),
                    error='object not found'
                )
            entity.is_archived = False
            self.session.commit()
            return entity
        except SQLAlchemyError as e:
            self.session.rollback()
            raise TKDatabaseError(error=str(e))


    def delete_archive(self, id: UUID) -> None:
        """Permanently delete an archived entity.
        Args:
            id: The UUID of the archived entity to delete
        Raises:
            EntityNotFoundError: If no archived entity with the given ID exists
            TKDatabaseError: For other database errors
        """
        try:
            entity = self.archive_query().filter(
                self.model.id == id).first()
            if not entity:
                raise EntityNotFoundError(
                    entity_type=self.model.__name__,
                    identifier=str(id),
                    error='object not found'
                )
            self.session.delete(entity)
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            raise TKDatabaseError(error=str(e))