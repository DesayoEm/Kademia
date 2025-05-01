from functools import wraps
from V2.app.core.shared.errors.maps.fk_mapper import fk_error_map
from V2.app.core.shared.errors import RelationshipError, RelatedEntityNotFoundError


class FKResolver:
    @staticmethod
    def resolve_fk_violation(factory_class, error_message, context_obj, operation, fk_map):
        """
        Resolves a foreign key constraint violation to a user-friendly error.

        This method looks up the constraint name found in the error message and matches it to a known
        mapping (defined in `fk_mapper.py`) using the factory class name. If a matching constraint is found,
        it constructs a `RelatedEntityNotFoundError` with the appropriate context extracted from the
        provided object.

        Args:
            factory_class (Type): The factory class from which the error originated. Used to look up the mapping.
            error_message (str): The raw error message from the database (usually from a ForeignKeyViolation).
            context_obj (Any): SQLAlchemy model that holds the foreign key values.
            operation (str): The type of operation being performed (e.g., "create", "update", "delete").
            fk_map (dict): The mapping of foreign key constraint names to their associated model, attribute, and display name.

        Returns:
            RelatedEntityNotFoundError: A more specific, user-friendly exception describing the FK failure.
            None: If no matching constraint is found in the error message.
        """
        factory_key = factory_class.__name__
        mappings = {**fk_map.get("common", {}), **fk_map.get(factory_key, {})}

        error_message = error_message.lower()

        for constraint_name, (model, attr, label) in mappings.items():
            constraint_patterns = [
                constraint_name.lower(),
                f'"{constraint_name.lower()}"',
                f"'{constraint_name.lower()}'"
            ]

            if any(p in error_message for p in constraint_patterns):
                attr_value = getattr(context_obj, attr, "unknown")

                return RelatedEntityNotFoundError(
                    entity_model=model,
                    identifier=attr_value,
                    display_name=label,
                    operation=operation,
                    detail=error_message
                )

        return None


def resolve_fk_on_create():
    """
    Decorator to resolve foreign key errors during CREATE operations.
    Parses the error message to identify the specific foreign key constraint.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except RelationshipError as e:
                context_obj = kwargs.get("data")
                if context_obj is None and len(args) > 1:
                    context_obj = args[1]

                resolved = FKResolver.resolve_fk_violation(
                    factory_class=self.__class__,
                    error_message=str(e),
                    context_obj=context_obj,
                    operation="create",
                    fk_map=fk_error_map
                )
                if resolved:
                    raise resolved
                raise e
        return wrapper
    return decorator


def resolve_fk_on_update():
    """
    Decorator to resolve foreign key errors during UPDATE operations.
    Expects the updated object (e.g. existing entity) to be assigned to a local variable inside the method.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except RelationshipError as e:
                existing = kwargs.get("existing") or getattr(self, "existing", None)
                resolved = FKResolver.resolve_fk_violation(
                    factory_class=self.__class__,
                    error_message=str(e),
                    context_obj=existing,
                    operation="update",
                    fk_map=fk_error_map
                )
                if resolved:
                    raise resolved
                raise RelationshipError(
                    error=str(e), operation="update"
                )
        return wrapper
    return decorator


def resolve_fk_on_delete():
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except RelationshipError as e:
                raise RelationshipError(
                    error=str(e),
                    operation="delete"
                )
        return wrapper
    return decorator
