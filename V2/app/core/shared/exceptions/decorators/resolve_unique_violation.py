from functools import wraps
from V2.app.core.shared.exceptions import DuplicateEntityError

def resolve_unique_violation(constraint_map):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except Exception as e:
                constraint = getattr(e, 'constraint', None)

                if constraint in constraint_map:
                    field_name, value_provider = constraint_map[constraint]
                    value = value_provider(self, *args, **kwargs) if callable(value_provider) else value_provider
                    raise DuplicateEntityError(
                        entity_model=self.entity_model,
                        field=field_name,
                        entry=value,
                        display_name=self.display_name,
                        detail=str(e)
                    )
                raise e
        return wrapper
    return decorator