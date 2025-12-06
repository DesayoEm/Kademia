from typing import List
from uuid import UUID, uuid4
from datetime import date

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.core.curriculum.models.curriculum import SubjectEducator
from app.core.curriculum.services.validators import CurriculumValidator
from app.core.shared.exceptions.database_errors import CompositeDuplicateEntityError
from app.core.shared.factory.base_factory import BaseFactory
from app.core.shared.services.lifecycle_service.archive_service import ArchiveService
from app.core.shared.services.lifecycle_service.delete_service import DeleteService
from app.infra.db.repositories.sqlalchemy_repos.base_repo import SQLAlchemyRepository
from app.core.shared.exceptions.decorators.resolve_unique_violation import (
    resolve_unique_violation,
)
from app.core.shared.exceptions.decorators.resolve_fk_violation import (
    resolve_fk_on_create,
    resolve_fk_on_delete,
)
from app.core.shared.exceptions import (
    EntityNotFoundError,
    ArchiveDependencyError,
    UniqueViolationError,
)
from app.core.shared.exceptions.maps.error_map import error_map


class SubjectEducatorFactory(BaseFactory):
    """Factory class for managing SubjectEducator operations."""

    def __init__(self, session: Session, model=SubjectEducator, current_user=None):
        super().__init__(current_user)
        """Initialize factory.
            Args:
            session: SQLAlchemy db session
            model: Model class, defaults to SubjectEducator
            current_user: The authenticated user performing the operation, if any.
        """

        self.model = model
        self.repository = SQLAlchemyRepository(self.model, session)
        self.validator = CurriculumValidator()
        self.delete_service = DeleteService(self.model, session)
        self.archive_service = ArchiveService(session, current_user)
        self.error_details = error_map.get(self.model)
        self.entity_model, self.display_name = self.error_details
        self.actor_id: UUID = self.get_actor_id()
        self.domain = "SubjectEducator"

    def raise_not_found(self, identifier, error):
        raise EntityNotFoundError(
            entity_model=self.entity_model,
            identifier=identifier,
            error=str(error),
            display_name=self.display_name,
        )

    @resolve_fk_on_create()
    def create_subject_educator(self, educator_id: UUID, data) -> SubjectEducator:
        """Create a new SubjectEducator.
        Args:
            educator_id: id of the educator to be assigned a subject
            data: SubjectEducator data
        Returns:
            SubjectEducator: Created SubjectEducator record
        """
        try:
            new_subject_educator = SubjectEducator(
                id=uuid4(),
                academic_level_subject_id=data.academic_level_subject_id,
                educator_id=educator_id,
                is_active=data.is_active,
                academic_session=self.validator.validate_academic_session(
                    data.academic_session
                ),
                date_assigned=date.today(),
                created_by=self.actor_id,
                last_modified_by=self.actor_id,
            )
            return self.repository.create(new_subject_educator)

        except UniqueViolationError as e:
            if (
                "subject_educators_educator_id_subject_id_academic_session_term_key"
                in str(e)
            ):
                raise CompositeDuplicateEntityError(  # fix.not raised
                    SubjectEducator,
                    str(e),
                    "This subject is already assigned to this educator for the specified session",
                )
            raise

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
        fields = [
            "academic_session",
            "is_active",
            "date_assigned",
            "term",
            "academic_level_subject_id",
            "educator_id",
        ]
        return self.repository.execute_query(fields, filters)

    def archive_subject_educator(
        self, subject_educator_id: UUID, reason
    ) -> SubjectEducator:
        """Archive a SubjectEducator if no active dependencies exist.
        Args:
            subject_educator_id (UUID): ID of SubjectEducator to archive
            reason: Reason for archiving
        Returns:
            SubjectEducator: Archived SubjectEducator record
        """
        try:
            failed_dependencies = self.archive_service.check_active_dependencies_exists(
                entity_model=self.model, target_id=subject_educator_id
            )
            if failed_dependencies:
                raise ArchiveDependencyError(
                    entity_model=self.entity_model,
                    identifier=subject_educator_id,
                    display_name=self.display_name,
                    related_entities=", ".join(failed_dependencies),
                )
            return self.repository.archive(subject_educator_id, self.actor_id, reason)

        except EntityNotFoundError as e:
            self.raise_not_found(subject_educator_id, e)

    @resolve_fk_on_delete(display="subject educator")
    def delete_subject_educator(self, subject_educator_id: UUID) -> None:
        """Permanently delete an SubjectEducator
        Args:
            subject_educator_id (UUID): ID of SubjectEducator to delete
        """
        try:
            return self.repository.delete(subject_educator_id)

        except EntityNotFoundError as e:
            self.raise_not_found(subject_educator_id, e)

    def get_all_archived_subject_educators(self, filters) -> List[SubjectEducator]:
        """Get all archived SubjectEducators with filtering.
        Returns:
            List[SubjectEducator]: List of archived SubjectEducator records
        """
        fields = [
            "academic_session",
            "is_active",
            "date_assigned",
            "term",
            "academic_level_subject_id",
            "educator_id",
        ]
        return self.repository.execute_archive_query(fields, filters)

    def get_archived_subject_educator(
        self, subject_educator_id: UUID
    ) -> SubjectEducator:
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

    @resolve_fk_on_delete(display="subject educator")
    def delete_archived_subject_educator(self, subject_educator_id: UUID) -> None:
        """Permanently delete an archived SubjectEducator if there are no dependent entities.
        Args:
            subject_educator_id: ID of SubjectEducator to delete
        """
        try:
            self.repository.delete_archive(subject_educator_id)

        except EntityNotFoundError as e:
            self.raise_not_found(subject_educator_id, e)
