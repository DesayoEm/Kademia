from uuid import UUID

class DeletionHelper:
    def __init__(self, session, export_service, repository):
        self.session = session
        self.export_service = export_service
        self.repository = repository

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
            str: Download link or file path to exported file.
        """

        # 1. Fetch entity
        entity = self.repository.get_by_id(entity_id)

        # 2. Export it
        file_path = self.export_service.export(entity, format=export_format)

        # 3. Mark entity as exported
        entity.is_exported = True
        self.session.commit()

        # 4. Delete or archive
        if archive_after_export:
            entity.is_archived = True
            self.session.commit()
        else:
            self.repository.delete(entity_id)

        return file_path
