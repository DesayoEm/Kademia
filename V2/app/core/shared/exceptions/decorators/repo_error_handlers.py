from sqlalchemy.exc import SQLAlchemyError, IntegrityError, OperationalError
from psycopg2.errors import StringDataRightTruncation
from psycopg2 import errors as pg_errors

from V2.app.core.shared.exceptions import (
    EntityNotFoundError, UniqueViolationError, RelationshipError, DBConnectionError,
    KDDatabaseError, DBTextTooLongError
)


def handle_write_errors(operation: str = "unknown"):
    def decorator(fn):
        def wrapper(self, *args, **kwargs):
            try:
                return fn(self, *args, **kwargs)
            except EntityNotFoundError:
                raise

            except StringDataRightTruncation as e:
                raise DBTextTooLongError(error=str(e))

            except IntegrityError as e:
                self.session.rollback()
                orig = getattr(e, 'orig', None)
                msg = str(orig).lower() if orig else str(e).lower()

                constraint_name = None
                if hasattr(orig, 'diag') and hasattr(orig.diag, 'constraint_name'):
                    constraint_name = orig.diag.constraint_name

                if 'unique' in msg or isinstance(orig, pg_errors.UniqueViolation):
                    raise UniqueViolationError(error=msg, constraint=constraint_name)

                if 'foreign key' in msg or isinstance(orig, pg_errors.ForeignKeyViolation):
                    raise RelationshipError(
                        error=msg,
                        operation=operation,
                        constraint=constraint_name
                    )

                raise KDDatabaseError(error=f"Database integrity error: {msg}")

            except OperationalError as e:
                self.session.rollback()
                raise DBConnectionError(error=str(e))

            except SQLAlchemyError as e:
                self.session.rollback()
                raise KDDatabaseError(error=str(e))

            except Exception:
                raise

        return wrapper

    return decorator


def handle_read_errors():
    def decorator(fn):
        def wrapper(self, *args, **kwargs):
            try:
                return fn(self, *args, **kwargs)
            except EntityNotFoundError:
                raise
            except OperationalError as e:
                self.session.rollback()
                raise DBConnectionError(error=str(e))
            except SQLAlchemyError as e:
                self.session.rollback()
                raise KDDatabaseError(error=str(e))
            except Exception:
                raise

        return wrapper

    return decorator