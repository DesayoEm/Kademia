from functools import wraps
from ....core.errors.fk_resolver import FKResolver
from ....core.errors.maps.fk_mapper import fk_error_map
from ....core.errors import RelationshipError


def resolve_fk_on_create():
    """
    Decorator to resolve foreign key errors during CREATE operations.
    Expects the context object (e.g. new_student, new_staff) to be passed as the first or second argument.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except RelationshipError as e:
                context_obj = kwargs.get("context_obj") or (args[1] if len(args) > 1 else None)
                resolved = FKResolver.resolve_fk_violation(
                    factory_class=self.__class__,
                    error_message=str(e),
                    context_obj=context_obj,
                    operation="create",
                    fk_map=fk_error_map
                )
                if resolved:
                    raise resolved
                raise RelationshipError(
                    error=str(e), operation="create", entity_model="unknown", domain=self.domain
                )
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
                    error=str(e), operation="update", entity_model="unknown", domain=self.domain
                )
        return wrapper
    return decorator
