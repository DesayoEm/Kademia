from typing import List
from uuid import UUID, uuid4
from datetime import date
from sqlalchemy.orm import Session
from V2.app.core.curriculum.models.curriculum import SubjectEducator
from V2.app.core.curriculum.validators import CurriculumValidator
from V2.app.core.shared.services.lifecycle_service.archive_service import ArchiveService
from V2.app.core.shared.services.lifecycle_service.delete_service import DeleteService
from V2.app.infra.db.repositories.sqlalchemy_repos.base_repo import SQLAlchemyRepository
from V2.app.core.shared.exceptions.decorators.resolve_unique_violation import resolve_unique_violation
from V2.app.core.shared.exceptions.decorators.resolve_fk_violation import resolve_fk_on_create, resolve_fk_on_delete
from V2.app.core.shared.exceptions import EntityNotFoundError, ArchiveDependencyError
from V2.app.core.shared.exceptions.maps.error_map import error_map

SYSTEM_USER_ID = UUID('00000000-0000-0000-0000-000000000000')


class SubjectEducatorFactory:
    """Factory class for managing SubjectEducator operations."""

    def __init__(self, session: Session, model = SubjectEducator):
        """Initialize factory with model and db session.
            Args:
            session: SQLAlchemy db session
            model: Model class, defaults to SubjectEducator
        """
        self.model = model
        self.repository = SQLAlchemyRepository(self.model, session)
        self.validator = CurriculumValidator()
        self.delete_service = DeleteService(self.model, session)
        self.archive_service = ArchiveService(session)
        self.error_details = error_map.get(self.model)
        self.entity_model, self.display_name = self.error_details
        self.domain = "SubjectEducator"

    def raise_not_found(self, identifier, error):
        raise EntityNotFoundError(
            entity_model=self.entity_model,
            identifier=identifier,
            error=str(error),
            display_name=self.display_name
        )


    @resolve_unique_violation({
        "subject_educators_educator_id_subject_id_academic_session_term__key": ("name", lambda self, data: data.educator_id)
    })
    @resolve_fk_on_create()
    def create_subject_educator(self, data) -> SubjectEducator:
        """Create a new SubjectEducator.
        Args:
            data: SubjectEducator data
        Returns:
            SubjectEducator: Created SubjectEducator record
        """
        new_subject_educator = SubjectEducator(
            id=uuid4(),
            academic_level_subject_id=data.academic_level_subject_id,
            educator_id=data.educator_id,
            level_id=data.level_id,
            is_active=data.is_active,
            term=data.term,
            date_assigned=date.today(),
            academic_session=self.validator.validate_academic_session(data.academic_session),

            created_by=SYSTEM_USER_ID,
            last_modified_by=SYSTEM_USER_ID
        )
        return self.repository.create(new_subject_educator)


    def get_subject_educator(self, subject_educator_id: UUID) -> SubjectEducator:
        """Get a specific SubjectEducator by ID.
        Args:
            subject_educator_id (UUID): ID of SubjectEducator to retrieve
        Returns:
            SubjectEducator: Retrieved SubjectEducator record
        """
        try:
            return self.repository.get_by_id(subject_educator_id)
        except EntityNotFoundError as e:
            self.raise_not_found(subject_educator_id, e)


    def get_all_subject_educators(self, filters) -> List[SubjectEducator]:
        """Get all active SubjectEducators with filtering.
        Returns:
            List[SubjectEducator]: List of active SubjectEducators
        """
        fields = ['academic_session','is_active', 'date_assigned','term']
        return self.repository.execute_query(fields, filters)


    def archive_subject_educator(self, subject_educator_id: UUID, reason) -> SubjectEducator:
        """Archive a SubjectEducator if no active dependencies exist.
        Args:
            subject_educator_id (UUID): ID of SubjectEducator to archive
            reason: Reason for archiving
        Returns:
            SubjectEducator: Archived SubjectEducator record
        """
        try:
            failed_dependencies = self.archive_service.check_active_dependencies_exists(
                entity_model=self.model,
                target_id=subject_educator_id
            )
            if failed_dependencies:
                raise ArchiveDependencyError(
                    entity_model=self.entity_model, identifier=subject_educator_id,
                    display_name=self.display_name, related_entities=", ".join(failed_dependencies)
                )
            return self.repository.archive(subject_educator_id, SYSTEM_USER_ID, reason)

        except EntityNotFoundError as e:
            self.raise_not_found(subject_educator_id, e)


    @resolve_fk_on_delete()
    def delete_subject_educator(self, subject_educator_id: UUID, is_archived=False) -> None:
        """Permanently delete an SubjectEducator if there are no dependent entities
        Args:
            subject_educator_id (UUID): ID of SubjectEducator to delete
            is_archived: Whether to check archived or active entities
        """
        try:
            self.delete_service.check_safe_delete(self.model, subject_educator_id, is_archived)
            return self.repository.delete(subject_educator_id)

        except EntityNotFoundError as e:
            self.raise_not_found(subject_educator_id, e)


    def get_all_archived_subject_educators(self, filters) -> List[SubjectEducator]:
        """Get all archived SubjectEducators with filtering.
        Returns:
            List[SubjectEducator]: List of archived SubjectEducator records
        """
        fields = ['academic_session','is_active', 'date_assigned','term']
        return self.repository.execute_archive_query(fields, filters)


    def get_archived_subject_educator(self, subject_educator_id: UUID) -> SubjectEducator:
        """Get an archived SubjectEducator by ID.
        Args:
            subject_educator_id: ID of SubjectEducator to retrieve
        Returns:
            SubjectEducator: Retrieved SubjectEducator record
        """
        try:
            return self.repository.get_archive_by_id(subject_educator_id)
        except EntityNotFoundError as e:
            self.raise_not_found(subject_educator_id, e)


    def restore_subject_educator(self, subject_educator_id: UUID) -> SubjectEducator:
        """Restore an archived SubjectEducator.
        Args:
            subject_educator_id: ID of SubjectEducator to restore
        Returns:
            SubjectEducator: Restored SubjectEducator record
        """
        try:
            return self.repository.restore(subject_educator_id)
        except EntityNotFoundError as e:
            self.raise_not_found(subject_educator_id, e)


    @resolve_fk_on_delete()
    def delete_archived_subject_educator(self, subject_educator_id: UUID, is_archived = True) -> None:
        """Permanently delete an archived SubjectEducator if there are no dependent entities.
        Args:
            subject_educator_id: ID of SubjectEducator to delete
            is_archived: Whether to check archived or active entities
        """
        try:
            self.delete_service.check_safe_delete(self.model, subject_educator_id, is_archived)
            self.repository.delete_archive(subject_educator_id)

        except EntityNotFoundError as e:
            self.raise_not_found(subject_educator_id, e)
