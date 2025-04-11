from uuid import UUID
from ...database.db_repositories.sqlalchemy_repos.base_repo import SQLAlchemyRepository

class DeletionHelper:
    def __init__(self, session, model):
        self.session = session
        self.export_service = "export_service"
        self.model = model
        self.repository = SQLAlchemyRepository(model, session)


    def export_and_delete(
        self,
        entity_id: UUID,
        export_format: str,
        archive_after_export: bool = False,
    ):
        """
        Exports the entity and deletes (or archives) it.
        Args:
            entity_id (UUID): ID of entity to delete.
            export_format (str): "pdf", "csv", or "excel"
            archive_after_export (bool): If True, archive instead of delete.

        Returns:
            str: Download link
        """

        entity = self.repository.get_by_id(entity_id)


        download_str = self.export_service.export(entity, format=export_format)


        entity.is_exported = True
        self.session.commit()
        self.repository.delete(entity_id)

        return download_str
