from functools import wraps
from V2.app.core.shared.errors import UniqueViolationError, DuplicateEntityError

def resolve_unique_violation(constraint_map: dict):
    """
    Decorator to translate UniqueViolationError to a identity-facing DuplicateEntityError.
    `constraint_map` format:
        {
            "db_constraint": ("field_name", lambda self, context_obj: context_obj.some_field)
        }
    This decorator automatically passes the second positional argument (after self)
    as `context_obj` to the value resolver lambda.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except UniqueViolationError as e:
                constraint = getattr(e, "constraint", "").lower()
                mapping = constraint_map.get(constraint)

                if mapping:
                    field, value_provider = mapping
                    context_obj = args[1] if len(args) > 1 else None
                    value = (
                        value_provider(self, context_obj)
                        if callable(value_provider) and context_obj is not None
                        else value_provider
                    )
                    raise DuplicateEntityError(
                        entity_model=self.entity_model,
                        entry=value,
                        field=field,
                        display_name=self.display_name,
                        detail=e.error
                    )

                # fallback
                raise DuplicateEntityError(
                    entity_model=self.entity_model,
                    entry="value",
                    field="unknown",
                    display_name=self.display_name,
                    detail=e.error
                )
        return wrapper
    return decorator
