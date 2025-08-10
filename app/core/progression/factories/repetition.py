from typing import List
from uuid import UUID, uuid4
from sqlalchemy.orm import Session
from app.core.identity.factories.student import StudentFactory
from app.core.identity.models.student import Student
from app.core.progression.models.progression import Repetition
from app.core.shared.exceptions.database_errors import CompositeDuplicateEntityError
from app.core.shared.factory.base_factory import BaseFactory
from app.core.shared.schemas.enums import ApprovalStatus
from app.core.shared.services.lifecycle_service.archive_service import ArchiveService
from app.core.shared.services.lifecycle_service.delete_service import DeleteService
from app.infra.db.repositories.sqlalchemy_repos.base_repo import SQLAlchemyRepository
from app.core.shared.exceptions import EntityNotFoundError, ArchiveDependencyError, UniqueViolationError
from app.core.shared.exceptions.maps.error_map import error_map
from app.core.shared.exceptions.decorators.resolve_fk_violation import (
    resolve_fk_on_update, resolve_fk_on_create, resolve_fk_on_delete
)




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
        self.current_user = current_user
        self.repository = SQLAlchemyRepository(self.model, session)
        self.delete_service = DeleteService(self.model, session)
        self.archive_service = ArchiveService(session, self.current_user)
        self.error_details = error_map.get(self.model)
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
        from app.core.progression.services.repetition_service import RepetitionService
        service = RepetitionService(self.session, self.current_user)

        try:
            student_factory = StudentFactory(self.session, Student, self.current_user)

            student = student_factory.get_student(student_id)

            new_repetition = Repetition(
                id=uuid4(),
                student_id=student_id,
                academic_session=data.academic_session,
                failed_level_id=student.level_id,
                repeat_level_id=service.validate_repetition_level(student.level_id, data.repeat_level_id),
                repetition_reason=data.repetition_reason,
                status=ApprovalStatus.PENDING,
                created_by=self.actor_id,
                last_modified_by=self.actor_id
            )
            return self.repository.create(new_repetition)

        except UniqueViolationError as e:
            raise CompositeDuplicateEntityError(
                Repetition, str(e),
                f"This student has an existing repetition record for the {data.academic_session} session")


    def get_repetition(self, repetition_id: UUID) -> Repetition:
        """Get a specific repetition record by ID."""
        try:
            return self.repository.get_by_id(repetition_id)
        except EntityNotFoundError as e:
            self.raise_not_found(repetition_id, e)


    def get_all_repetitions(self, filters) -> List[Repetition]:
        """Get all active repetition records with filtering."""
        fields = ['student_id', 'failed_level_id', 'academic_session', 'status','status_completed_by']
        return self.repository.execute_query(fields, filters)


    @resolve_fk_on_update()
    def update_repetition(self, repetition_id: UUID, data: dict) -> Repetition:
        """Update a repetition record information."""
        from app.core.progression.services.repetition_service import RepetitionService
        service = RepetitionService(self.session, self.current_user)

        try:
            existing = self.get_repetition(repetition_id)

            if "repeat_level_id" in data:
                existing.repeat_level_id = service.validate_repetition_level(
                    existing.failed_level_id, data["repeat_level_id"])

            if "repetition_reason" in data:
                existing.repetition_reason = data["repetition_reason"]

            for key, value in data.items():
                if hasattr(existing, key):
                    setattr(existing, key, value)

            return self.repository.update(repetition_id, existing, modified_by=self.actor_id)

        except EntityNotFoundError as e:
            self.raise_not_found(repetition_id, e)
            


    def archive_repetition(self, repetition_id: UUID, reason) -> Repetition:
        """Archive a repetition record."""
        try:
            return self.repository.archive(repetition_id, self.actor_id, reason)

        except EntityNotFoundError as e:
            self.raise_not_found(repetition_id, e)


    @resolve_fk_on_delete(display="repetition")
    def delete_repetition(self, repetition_id: UUID, is_archived=False) -> None:
        """Permanently delete a repetition record."""
        try:
            return self.repository.delete(repetition_id)

        except EntityNotFoundError as e:
            self.raise_not_found(repetition_id, e)


    def get_all_archived_repetitions(self, filters) -> List[Repetition]:
        """Get all archived repetition records with filtering."""
        fields = ['student_id', 'failed_level_id', 'academic_session', 'status','status_completed_by']
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


    @resolve_fk_on_delete(display="repetition")
    def delete_archived_repetition(self, repetition_id: UUID) -> None:
        """Permanently delete an archived repetition record."""
        try:
            self.repository.delete_archive(repetition_id)

        except EntityNotFoundError as e:
            self.raise_not_found(repetition_id, e)
