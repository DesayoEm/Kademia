from typing import List
from uuid import UUID, uuid4
from sqlalchemy.orm import Session

from V2.app.core.academic_structure.factories.academic_level import AcademicLevelFactory
from V2.app.core.identity.factories.student import StudentFactory
from V2.app.core.identity.models.student import Student
from V2.app.core.progression.models.progression import Repetition
from V2.app.core.progression.validators import ProgressionValidator
from V2.app.core.shared.factory.base_factory import BaseFactory
from V2.app.core.shared.models.enums import AcademicLevel
from V2.app.core.shared.services.lifecycle_service.archive_service import ArchiveService
from V2.app.core.shared.services.lifecycle_service.delete_service import DeleteService
from V2.app.infra.db.repositories.sqlalchemy_repos.base_repo import SQLAlchemyRepository
from V2.app.core.shared.exceptions.decorators.resolve_fk_violation import resolve_fk_on_create, resolve_fk_on_delete
from V2.app.core.shared.exceptions import EntityNotFoundError, ArchiveDependencyError
from V2.app.core.shared.exceptions.maps.error_map import error_map



class RepetitionFactory(BaseFactory):
    """Factory class for managing repetition operations."""

    def __init__(self, session: Session, model=Repetition, current_user = None):
        super().__init__(current_user)
        """Initialize factory with db session, model and current user.
        Args:
            session: SQLAlchemy db session
            model: Model class, defaults to Repetition
            current_user: The authenticated user performing the operation, if any.
        """
        self.session = session
        self.model = model
        self.repository = SQLAlchemyRepository(self.model, session)
        self.delete_service = DeleteService(self.model, session)
        self.archive_service = ArchiveService(session)
        self.error_details = error_map.get(self.model)
        self.validator = ProgressionValidator()
        self.entity_model, self.display_name = self.error_details
        self.actor_id: UUID = self.get_actor_id()
        self.domain = "Repetition"

    def raise_not_found(self, identifier, error):
        raise EntityNotFoundError(
            entity_model=self.entity_model,
            identifier=identifier,
            error=str(error),
            display_name=self.display_name
        )

    @resolve_fk_on_create()
    def create_repetition(self, student_id: UUID, data) -> Repetition:
        """Create a new repetition record for a student."""
        student_factory = StudentFactory(self.session, Student)
        academic_factory = AcademicLevelFactory(self.session, AcademicLevel)

        student = student_factory.get_student(student_id)

        previous_level = academic_factory.get_academic_level(student.level_id)
        new_level = academic_factory.get_academic_level(data.new_level_id)

        validated_new_level = self.validator.validate_repetition_level(previous_level, new_level)

        new_repetition = Repetition(
            id=uuid4(),
            student_id=student_id,
            academic_session=data.academic_session,
            previous_level_id=data.previous_level_id,
            new_level_id=validated_new_level,
            reason=data.reason,
            status=data.status,
            status_updated_by=data.status_updated_by,
            status_updated_at=data.status_updated_at,
            rejection_reason=data.rejection_reason,
            created_by=self.actor_id,
            last_modified_by=self.actor_id
        )
        return self.repository.create(new_repetition)


    def get_repetition(self, repetition_id: UUID) -> Repetition:
        """Get a specific repetition record by ID."""
        try:
            return self.repository.get_by_id(repetition_id)
        except EntityNotFoundError as e:
            self.raise_not_found(repetition_id, e)


    def get_all_repetitions(self, filters) -> List[Repetition]:
        """Get all active repetition records with filtering."""
        fields = ['academic_session', 'status']
        return self.repository.execute_query(fields, filters)


    def archive_repetition(self, repetition_id: UUID, reason) -> Repetition:
        """Archive a repetition record."""
        try:
            failed_dependencies = self.archive_service.check_active_dependencies_exists(
                entity_model=self.model,
                target_id=repetition_id
            )
            if failed_dependencies:
                raise ArchiveDependencyError(
                    entity_model=self.entity_model, identifier=repetition_id,
                    display_name=self.display_name, related_entities=", ".join(failed_dependencies)
                )
            return self.repository.archive(repetition_id, self.actor_id, reason)

        except EntityNotFoundError as e:
            self.raise_not_found(repetition_id, e)


    @resolve_fk_on_delete()
    def delete_repetition(self, repetition_id: UUID, is_archived=False) -> None:
        """Permanently delete a repetition record."""
        try:
            self.delete_service.check_safe_delete(self.model, repetition_id, is_archived)
            return self.repository.delete(repetition_id)

        except EntityNotFoundError as e:
            self.raise_not_found(repetition_id, e)


    def get_all_archived_repetitions(self, filters) -> List[Repetition]:
        """Get all archived repetition records with filtering."""
        fields = ['academic_session', 'status']
        return self.repository.execute_archive_query(fields, filters)


    def get_archived_repetition(self, repetition_id: UUID) -> Repetition:
        """Get an archived repetition record by ID."""
        try:
            return self.repository.get_archive_by_id(repetition_id)
        except EntityNotFoundError as e:
            self.raise_not_found(repetition_id, e)


    def restore_repetition(self, repetition_id: UUID) -> Repetition:
        """Restore an archived repetition record."""
        try:
            return self.repository.restore(repetition_id)
        except EntityNotFoundError as e:
            self.raise_not_found(repetition_id, e)


    @resolve_fk_on_delete()
    def delete_archived_repetition(self, repetition_id: UUID, is_archived=True) -> None:
        """Permanently delete an archived repetition record."""
        try:
            self.delete_service.check_safe_delete(self.model, repetition_id, is_archived)
            self.repository.delete_archive(repetition_id)

        except EntityNotFoundError as e:
            self.raise_not_found(repetition_id, e)
