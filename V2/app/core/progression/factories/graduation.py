from typing import List
from uuid import UUID, uuid4
from sqlalchemy.orm import Session
from V2.app.core.progression.models.progression import Graduation
from V2.app.core.shared.factory.base_factory import BaseFactory
from V2.app.core.shared.services.lifecycle_service.archive_service import ArchiveService
from V2.app.core.shared.services.lifecycle_service.delete_service import DeleteService
from V2.app.infra.db.repositories.sqlalchemy_repos.base_repo import SQLAlchemyRepository
from V2.app.core.shared.exceptions.decorators.resolve_fk_violation import resolve_fk_on_create, resolve_fk_on_update, resolve_fk_on_delete
from V2.app.core.shared.exceptions import EntityNotFoundError, ArchiveDependencyError
from V2.app.core.shared.exceptions.maps.error_map import error_map



class GraduationFactory(BaseFactory):
    """Factory class for managing graduation operations."""

    def __init__(self, session: Session, model=Graduation, current_user = None):
        super().__init__(current_user)
        """Initialize factory with db session, model and current user.
        Args:
            session: SQLAlchemy db session
            model: Model class, defaults to Graduation
            current_user: The authenticated user performing the operation, if any.
        """
        self.model = model
        self.repository = SQLAlchemyRepository(self.model, session)
        self.delete_service = DeleteService(self.model, session)
        self.archive_service = ArchiveService(session)
        self.error_details = error_map.get(self.model)
        self.entity_model, self.display_name = self.error_details
        self.actor_id: UUID = self.get_actor_id()
        self.domain = "Graduation"

    def raise_not_found(self, identifier, error):
        raise EntityNotFoundError(
            entity_model=self.entity_model,
            identifier=identifier,
            error=str(error),
            display_name=self.display_name
        )

    @resolve_fk_on_create()
    def create_graduation(self, student_id: UUID, data) -> Graduation:
        """Create a new graduation record."""
        new_graduation = Graduation(
            id=uuid4(),
            student_id=student_id,
            academic_session=data.academic_session,
            status=data.status,

            status_updated_by=data.status_updated_by,
            status_updated_at=data.status_updated_at,
            rejection_reason=data.rejection_reason,
            created_by=self.domain,
            last_modified_by=self.domain
        )
        return self.repository.create(new_graduation)

    def get_graduation(self, graduation_id: UUID) -> Graduation:
        """Get a specific graduation record by ID."""
        try:
            return self.repository.get_by_id(graduation_id)
        except EntityNotFoundError as e:
            self.raise_not_found(graduation_id, e)


    def get_all_graduations(self, filters) -> List[Graduation]:
        """Get all active graduation records with filtering."""
        fields = ['academic_session', 'status']
        return self.repository.execute_query(fields, filters)


    def archive_graduation(self, graduation_id: UUID, reason) -> Graduation:
        """Archive a graduation record."""
        try:
            failed_dependencies = self.archive_service.check_active_dependencies_exists(
                entity_model=self.model,
                target_id=graduation_id
            )
            if failed_dependencies:
                raise ArchiveDependencyError(
                    entity_model=self.entity_model, identifier=graduation_id,
                    display_name=self.display_name, related_entities=", ".join(failed_dependencies)
                )
            return self.repository.archive(graduation_id, self.actor_id, reason)

        except EntityNotFoundError as e:
            self.raise_not_found(graduation_id, e)

    @resolve_fk_on_delete()
    def delete_graduation(self, graduation_id: UUID, is_archived=False) -> None:
        """Permanently delete a graduation record."""
        try:
            self.delete_service.check_safe_delete(self.model, graduation_id, is_archived)
            return self.repository.delete(graduation_id)

        except EntityNotFoundError as e:
            self.raise_not_found(graduation_id, e)


    def get_all_archived_graduations(self, filters) -> List[Graduation]:
        """Get all archived graduation records with filtering."""
        fields = ['academic_session', 'status']
        return self.repository.execute_archive_query(fields, filters)


    def get_archived_graduation(self, graduation_id: UUID) -> Graduation:
        """Get an archived graduation record by ID."""
        try:
            return self.repository.get_archive_by_id(graduation_id)
        except EntityNotFoundError as e:
            self.raise_not_found(graduation_id, e)


    def restore_graduation(self, graduation_id: UUID) -> Graduation:
        """Restore an archived graduation record."""
        try:
            return self.repository.restore(graduation_id)
        except EntityNotFoundError as e:
            self.raise_not_found(graduation_id, e)


    @resolve_fk_on_delete()
    def delete_archived_graduation(self, graduation_id: UUID, is_archived=True) -> None:
        """Permanently delete an archived graduation record."""
        try:
            self.delete_service.check_safe_delete(self.model, graduation_id, is_archived)
            self.repository.delete_archive(graduation_id)

        except EntityNotFoundError as e:
            self.raise_not_found(graduation_id, e)
