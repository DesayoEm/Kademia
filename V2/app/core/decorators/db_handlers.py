from sqlalchemy.exc import SQLAlchemyError, IntegrityError, OperationalError
from psycopg2.errors import StringDataRightTruncation

from ..errors import EntityNotFoundError
from ..errors.database_errors import (
    UniqueViolationError, RelationshipError,
    DBConnectionError, DatabaseError as TKDatabaseError
)
from ..errors.entry_validation_errors import DBTextTooLongError


def handle_write_errors(operation: str = "unknown"):
    def decorator(fn):
        def wrapper(self, *args, **kwargs):
            try:
                return fn(self, *args, **kwargs)

            except StringDataRightTruncation as e:
                raise DBTextTooLongError(error= str(e))

            except IntegrityError as e:
                self.session.rollback()
                msg = str(e.orig).lower() if e.orig else str(e).lower()
                if 'unique' in msg:
                    raise UniqueViolationError(error=msg)
                if 'foreign key' in msg:
                    raise RelationshipError(operation=operation, error=msg,
                                entity_model=self.model.__name__, domain = "None")

                raise TKDatabaseError(error=f"Database integrity error: {msg}")

            except OperationalError as e:
                self.session.rollback()
                raise DBConnectionError(error=str(e))

            except SQLAlchemyError as e:
                self.session.rollback()
                raise TKDatabaseError(error=str(e))

            except Exception as e:
                raise TKDatabaseError(error=str(e))
        return wrapper
    return decorator


def handle_read_errors():
    def decorator(fn):
        def wrapper(self, *args, **kwargs):
            try:
                return fn(self, *args, **kwargs)

            except EntityNotFoundError:
                raise EntityNotFoundError

            except OperationalError as e:
                self.session.rollback()
                raise DBConnectionError(error=str(e))

            except SQLAlchemyError as e:
                self.session.rollback()
                raise TKDatabaseError(error=str(e))

            except Exception as e:
                raise TKDatabaseError(error=str(e))
        return wrapper
    return decorator