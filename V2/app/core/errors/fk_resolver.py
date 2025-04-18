from ..errors import RelatedEntityNotFoundError

class FKResolver:
    def __init__(self):
        pass

    @staticmethod
    def resolve_fk_violation(factory_class, error_message, context_obj, operation, fk_map):
        mappings = fk_map.get(factory_class, {}) | fk_map.get("common", {})

        for fk_key, (model, attr, label) in mappings.items():
            if fk_key in error_message:
                return RelatedEntityNotFoundError(
                    entity_model=model,
                    identifier=getattr(context_obj, attr, "unknown"),
                    display_name=label,
                    operation=operation
                )
        return None

