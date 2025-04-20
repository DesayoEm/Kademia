from uuid import UUID
from typing import Optional, List, Type
from sqlalchemy import desc, asc, select, Select, func, or_, Enum
from sqlalchemy.orm import Session

from ..base_repo import Repository, T
from V2.app.core.shared.errors import  EntityNotFoundError
from V2.app.core.shared.errors.decorators.repo_error_handlers import handle_write_errors, handle_read_errors

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
    def exists(self, entity_id: UUID) -> bool:
        """Check if an active entity exists by ID."""
        stmt = select(func.count()).select_from(self.model).where(
            self.model.id == entity_id,
            self.model.is_archived == False
        )
        count = self.session.execute(stmt).scalar()
        return count > 0


    @handle_read_errors()
    def get_by_id(self, entity_id: UUID) -> Optional[T]:
        """Get an active entity by its id."""
        stmt = self.active_query().where(self.model.id == entity_id)
        entity = self.session.execute(stmt).scalar_one_or_none()

        if not entity:
            raise EntityNotFoundError(
                entity_model=self.model.__name__,
                identifier=entity_id, error = NOT_FOUND_ERROR, display_name="Unknown"
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

            if value is not None:

                if field == "full_name" and hasattr(self.model, "first_name") and hasattr(self.model, "last_name"):
                    full_name = func.concat(self.model.first_name, ' ', self.model.last_name)
                    reversed_full_name = func.concat(self.model.last_name, ' ', self.model.first_name)

                    stmt = stmt.where(
                        or_(
                            full_name.ilike(f"%{value}%"),
                            reversed_full_name.ilike(f"%{value}%")
                        )
                    )

                elif hasattr(self.model, field):
                    column = getattr(self.model, field)

                    if isinstance(column.type, Enum):
                        stmt = stmt.where(column == value)

                    elif isinstance(value, str) and field in fields:
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

        order_func = desc if order_dir == 'desc' else asc

        if order_by == "full_name":
            stmt = stmt.order_by(
                order_func(self.model.first_name),
                order_func(self.model.last_name)
            )

        elif hasattr(self.model, order_by):
            order_column = getattr(self.model, order_by)
            stmt = stmt.order_by(order_func(order_column))
        else:
            stmt = stmt.order_by(order_func(self.model.created_at))


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
            if not entity:
                raise EntityNotFoundError(
                    entity_model=self.model.__name__,
                    identifier=entity_id, error=NOT_FOUND_ERROR, display_name="Unknown"
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
            if not entity:
                raise EntityNotFoundError(
                    entity_model=self.model.__name__,
                    identifier=entity_id, error=NOT_FOUND_ERROR, display_name="Unknown"
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
            if not entity:
                raise EntityNotFoundError(
                    entity_model=self.model.__name__,
                    identifier=entity_id, error=NOT_FOUND_ERROR, display_name="Unknown"
                )

        self.session.delete(entity)
        self.session.commit()


    @handle_read_errors()
    def get_archive_by_id(self, entity_id: UUID) -> Optional[T]:
        """Get an archived entity by its id"""
        stmt = self.archive_query().where(self.model.id == entity_id)
        entity = self.session.execute(stmt).scalar_one_or_none()
        if not entity:
            if not entity:
                raise EntityNotFoundError(
                    entity_model=self.model.__name__,
                    identifier=entity_id, error=NOT_FOUND_ERROR, display_name="Unknown"
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
            if not entity:
                raise EntityNotFoundError(
                    entity_model=self.model.__name__,
                    identifier=entity_id, error=NOT_FOUND_ERROR, display_name="Unknown"
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
            if not entity:
                raise EntityNotFoundError(
                    entity_model=self.model.__name__,
                    identifier=entity_id, error=NOT_FOUND_ERROR, display_name="Unknown"
                )

        self.session.delete(entity)
        self.session.commit()
