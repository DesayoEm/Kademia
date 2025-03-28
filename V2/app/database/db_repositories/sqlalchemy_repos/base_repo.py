from uuid import UUID
from typing import Optional, List, Type
from sqlalchemy import desc, asc, select, Select
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, OperationalError
from sqlalchemy.orm import Session
from ....core.errors.database_errors import (
    UniqueViolationError, EntityNotFoundError, RelationshipError, DBConnectionError)
from ....core.errors.database_errors import DatabaseError as TKDatabaseError
from ..base_repo import Repository, T
from ....core.decorators.db_handlers import handle_write_errors, handle_read_errors

NOT_FOUND_ERROR = "Object not found"

class BaseRepository(Repository[T]):
    """Base repository class"""

    def __init__(self, model: Type[T], session: Session):
        """Initialize the repository with a model and session.
        Args:
            model: The SQLAlchemy model class
            session: The SQLAlchemy database session
        """
        super().__init__()
        self.model = model
        self.session = session

    def active_query(self) -> Select:
        """Get a SELECT statement for non-archived entities."""
        return select(self.model).where(self.model.is_archived == False)

    def archive_query(self) -> Select:
        """Get a SELECT statement for archived entities."""
        return select(self.model).where(self.model.is_archived == True)


class SQLAlchemyRepository(BaseRepository[T]):
    """Repository implementation for SQLAlchemy with combined active and archive operations."""

    @handle_write_errors("create")
    def create(self, entity: T) -> T:
        """Create a new entity in the database."""
        self.session.add(entity)
        self.session.flush()
        self.session.commit()
        self.session.refresh(entity)
        return entity

    @handle_read_errors()
    def get_by_id(self, entity_id: UUID) -> Optional[T]:
        """Get an active entity by its id."""
        stmt = self.active_query().where(self.model.id == entity_id)
        entity = self.session.execute(stmt).scalar_one_or_none()

        if not entity:
            raise EntityNotFoundError(
                entity_type=self.model.__name__,
                identifier=str(entity_id), error = NOT_FOUND_ERROR
            )
            
        return entity


    def apply_filters(self, stmt: Select, fields: List[str], filters) -> Select:
        """
        Apply filters to a SELECT statement based on filter parameters.

        Args:
            stmt: SQLAlchemy SELECT statement
            fields: List of fields that support text search
            filters: Pydantic-like object with filter fields

        Returns:
            Select: Filtered SQLAlchemy SELECT statement
        """
        for field, value in filters.model_dump(exclude_unset=True).items():
            if field in {'limit', 'offset', 'order_by', 'order_dir'}:
                continue
            if value is not None and hasattr(self.model, field):
                column = getattr(self.model, field)
                if isinstance(value, str) and field in fields:
                    stmt = stmt.where(column.ilike(f"%{value}%"))
                else:
                    stmt = stmt.where(column == value)

        return stmt


    @handle_read_errors()
    def execute_query(self, fields, filters) -> List[T]:
        """Execute a query for active entities with sorting and pagination."""
        stmt = self.active_query()
        stmt = self.apply_filters(stmt, fields, filters)

        order_by = getattr(filters, 'order_by', 'created_at')
        order_dir = getattr(filters, 'order_dir', 'asc')

        if order_by and hasattr(self.model, order_by):
            order_column = getattr(self.model, order_by)
            order_func = desc if order_dir == 'desc' else asc
            stmt = stmt.order_by(order_func(order_column))

        limit = getattr(filters, 'limit', 100)
        offset = getattr(filters, 'offset', 0)
        stmt = stmt.limit(limit).offset(offset)

        result = self.session.execute(stmt).scalars().all()
        return result or []


    @handle_write_errors("update")
    def update(self, entity_id: UUID, entity: T) -> T:
        """Update an existing active entity."""
        stmt = self.active_query().where(self.model.id == entity_id)
        existing = self.session.execute(stmt).scalar_one_or_none()

        if not existing:
            raise EntityNotFoundError(
                entity_type=self.model.__name__,
                identifier=str(entity_id),
                error=NOT_FOUND_ERROR
             )
        self.session.commit()
        self.session.refresh(entity)
        return entity


    @handle_read_errors()
    def archive(self, entity_id: UUID, archived_by_id: UUID, reason: str) -> T:
        """Archive an active entity."""
        stmt = self.active_query().where(self.model.id == entity_id)
        entity = self.session.execute(stmt).scalar_one_or_none()

        if not entity:
            raise EntityNotFoundError(
                entity_type=self.model.__name__,
                identifier=str(entity_id),
                error=NOT_FOUND_ERROR
            )

        entity.archive(archived_by_id, reason)
        self.session.commit()
        self.session.refresh(entity)
        return entity


    @handle_write_errors("delete")
    def delete(self, entity_id: UUID) -> None:
        """Permanently delete an active entity."""
        stmt = self.active_query().where(self.model.id == entity_id)
        entity = self.session.execute(stmt).scalar_one_or_none()

        if not entity:
            raise EntityNotFoundError(
                entity_type=self.model.__name__,
                identifier=str(entity_id),
                error=NOT_FOUND_ERROR
            )

        self.session.delete(entity)
        self.session.commit()


    @handle_read_errors()
    def get_archive_by_id(self, entity_id: UUID) -> Optional[T]:
        """Get an archived entity by its id"""
        stmt = self.archive_query().where(self.model.id == entity_id)
        entity = self.session.execute(stmt).scalar_one_or_none()
        if not entity:
            raise EntityNotFoundError(
                entity_type=self.model.__name__,
                identifier=str(entity_id), error=NOT_FOUND_ERROR
            )

        return entity


    @handle_read_errors()
    def execute_archive_query(self, fields, filters) -> List[T]:
        """Execute a query for archived entities with sorting and pagination."""
        stmt = self.archive_query()
        stmt = self.apply_filters(stmt, fields, filters)

        order_by = getattr(filters, 'order_by', 'created_at')
        order_dir = getattr(filters, 'order_dir', 'asc')

        if order_by and hasattr(self.model, order_by):
            order_column = getattr(self.model, order_by)
            order_func = desc if order_dir == 'desc' else asc
            stmt = stmt.order_by(order_func(order_column))

        limit = getattr(filters, 'limit', 100)
        offset = getattr(filters, 'offset', 0)
        stmt = stmt.limit(limit).offset(offset)

        result = self.session.execute(stmt).scalars().all()
        return result or []


    @handle_read_errors()
    def restore(self, entity_id: UUID) -> T:
        """Restore an archived entity to active status."""
        stmt = self.archive_query().where(self.model.id == entity_id)
        entity = self.session.execute(stmt).scalar_one_or_none()

        if not entity:
            raise EntityNotFoundError(
                entity_type=self.model.__name__,
                identifier=str(entity_id),
                error=NOT_FOUND_ERROR
            )

        entity.restore()
        self.session.commit()
        self.session.refresh(entity)
        return entity


    @handle_write_errors("delete")
    def delete_archive(self, entity_id: UUID) -> None:
        """Permanently delete an archived entity."""
        stmt = self.archive_query().where(self.model.id == entity_id)
        entity = self.session.execute(stmt).scalar_one_or_none()

        if not entity:
            raise EntityNotFoundError(
                entity_type=self.model.__name__,
                identifier=str(entity_id),
                error=NOT_FOUND_ERROR
            )

        self.session.delete(entity)
        self.session.commit()
