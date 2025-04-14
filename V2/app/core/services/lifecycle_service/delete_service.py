from uuid import UUID
from ...errors.archive_delete_errors import CascadeDeletionError, DeletionDependencyError
from ...errors.error_map import deletion_dependency_map
from V2.app.core.services.lifecycle_service.dependency_config import DEPENDENCY_CONFIG
from ..export_service.export import ExportService
from ....database.db_repositories.sqlalchemy_repos.base_repo import SQLAlchemyRepository


class DeletionService:
    def __init__(self, session, model):
        self.session = session
        self.export_service = ExportService(session)
        self.model = model
        self.repository = SQLAlchemyRepository(model, session)


    @staticmethod
    def check_dependent_entities(entity, entity_model):
        """Check if the entity has active related entities."""

        dependent_fields = []

        for field_name, _, display_name in DEPENDENCY_CONFIG.get(entity_model, []):
            related = getattr(entity, field_name, None)

            if related:
                if isinstance(related, list) and len(related) > 0:
                    dependent_fields.append(display_name)
                elif related is not None:
                    dependent_fields.append(display_name)

        return dependent_fields



    def safe_delete(self, entity_model, entity_id: UUID):
        """Safely delete if no dependent entities exist."""

        entity = self.repository.get_by_id(entity_id)
        error_info = deletion_dependency_map.get(entity_model)

        error_class, display_name = error_info

        dependent_fields = self.check_dependent_entities(entity, entity_model)

        if dependent_fields:
            if error_info:
                raise error_class(entity_name=display_name,
                    identifier=entity_id, related_entities=", ".join(dependent_fields)
                )
            else:  #fallback
                raise DeletionDependencyError(entity_name=display_name,
                    identifier=entity_id, related_entities=", ".join(dependent_fields)
                )

        self.session.delete(entity)
        self.session.commit()


    def cascade_deletion(self, entity, related_entities: list):
        """Cascade delete related entities first, then delete the main entity."""
        try:
            with self.session.begin():
                if not entity.is_exported:
                    raise CascadeDeletionError(error="Entity not exported before attempted deletion")

                for field_name in related_entities:
                    related = getattr(entity, field_name, None)

                    if related is None:
                        continue

                    if isinstance(related, list):
                        for item in related:
                            if item is not None:
                                self.repository.delete(item)
                    else:
                        self.repository.delete(related)

                self.repository.delete(entity)

        except Exception as e:
            raise CascadeDeletionError(error=str(e))


    def export_and_force_delete(self, entity_model,
                                entity_id: UUID,
                                export_format: str
                    ) -> str:
        """Export the entity, then force delete it and its related entities."""

        dependent_models = [
            dependent_model for dependent_model, _, _ in DEPENDENCY_CONFIG.get(entity_model)
        ]

        export_path = self.export_service.export_entity(entity_model, entity_id, export_format)
        entity = self.repository.get_by_id(entity_id)
        entity.is_exported = True
        self.cascade_deletion(entity, dependent_models)

        return export_path