from uuid import UUID
from V2.app.core.errors.archive_delete_errors import CascadeDeletionError
from V2.app.core.services.export_service.export import ExportService
from V2.app.database.db_repositories.sqlalchemy_repos.base_repo import SQLAlchemyRepository


class DeletionService:
    def __init__(self, session, model):
        self.session = session
        self.export_service = ExportService(session)
        self.model = model
        self.repository = SQLAlchemyRepository(model, session)


    def check_dependent_entities(self, entity) -> bool:
        """Check if the entity has active related entities."""

        # Logic here: e.g., check if entity.classes, entity.staff_assigned, etc.
        has_dependents = bool(entity.related_field)  # pseudo-code
        return has_dependents


    def safe_delete(self, entity_model, entity_id: UUID):
        """Safely delete if no dependent entities exist."""

        entity = self.repository.get_by_id(entity_id)

        if self.check_dependent_entities(entity):
            raise

        self.session.delete(entity)
        self.session.commit()


    def cascade_deletion(self, entity, related_entities: list):
        """Cascade delete related entities first, then delete the main entity."""

        try:
            with self.session.begin():
                for related_entity in related_entities:
                    if isinstance(related_entity, list):
                        for item in related_entity:
                            self.repository.delete(item)
                    else:
                        self.repository.delete(related_entity)

                self.repository.delete(entity)

        except Exception as e:
            raise CascadeDeletionError(error=str(e))


    def force_export_and_delete(self, entity_model,
                                entity_id: UUID,
                                related_entities: list,
                                export_format: str
                    ) -> str:
        """Export the entity, then force delete it and its related entities."""

        export_path = self.export_service.export_entity(entity_model, entity_id, export_format)
        entity = self.repository.get_by_id(entity_id)
        self.cascade_deletion(entity, related_entities)

        return export_path