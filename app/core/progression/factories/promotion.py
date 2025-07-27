from typing import List
from uuid import UUID, uuid4
from sqlalchemy.orm import Session

from app.core.progression.models.progression import Promotion
from app.core.shared.exceptions.database_errors import CompositeDuplicateEntityError
from app.core.shared.exceptions.decorators.resolve_unique_violation import resolve_unique_violation
from app.core.shared.factory.base_factory import BaseFactory
from app.core.shared.models.enums import ApprovalStatus
from app.core.shared.services.lifecycle_service.archive_service import ArchiveService
from app.core.shared.services.lifecycle_service.delete_service import DeleteService
from app.infra.db.repositories.sqlalchemy_repos.base_repo import SQLAlchemyRepository
from app.core.shared.exceptions.decorators.resolve_fk_violation import resolve_fk_on_create, resolve_fk_on_delete, \
    resolve_fk_on_update
from app.core.shared.exceptions import EntityNotFoundError, ArchiveDependencyError, UniqueViolationError
from app.core.shared.exceptions.maps.error_map import error_map



class PromotionFactory(BaseFactory):
    """Factory class for managing promotion operations."""

    def __init__(self, session: Session, model=Promotion, current_user = None):
        super().__init__(current_user)
        """Initialize factory with db session, model and current user.
        Args:
            session: SQLAlchemy db session
            model: Model class, defaults to Promotion
            current_user: The authenticated user performing the operation, if any.
        """

        self.model = model
        self.session = session
        self.current_user = current_user
        self.repository = SQLAlchemyRepository(self.model, session)
        self.delete_service = DeleteService(self.model, session)
        self.archive_service = ArchiveService(session)
        self.entity_model, self.display_name = error_map.get(self.model)
        self.actor_id: UUID = self.get_actor_id()
        self.domain = "Promotion"

    def raise_not_found(self, identifier, error):
        raise EntityNotFoundError(
            entity_model=self.entity_model,
            identifier=identifier,
            error=str(error),
            display_name=self.display_name
        )

    @resolve_unique_violation({
        "uq_promotion_student_session": (
                "_", "This student has an existing promotion record for the specified academic session"
        )
    })
    @resolve_fk_on_create()
    def create_promotion(self, student_id: UUID, data) -> Promotion:
        """Create a new promotion record for a student."""
        from app.core.identity.models.student import Student
        from app.core.identity.factories.student import StudentFactory
        student_factory = StudentFactory(self.session, Student, self.current_user)
        student = student_factory.get_student(student_id)


        from app.core.progression.services.promotion_service import PromotionService
        service = PromotionService(self.session, self.current_user)
        validated_new_level_id = service.validate_promotion_level(
            student.level_id, data.promoted_level_id, student_id, data.academic_session
        )


        try:
            new_promotion = Promotion(
            id=uuid4(),
            student_id=student_id,
            academic_session=data.academic_session,
            notes=data.notes,
            previous_level_id=student.level_id,
            promoted_level_id=validated_new_level_id,

            status=ApprovalStatus.PENDING,
            created_by=self.actor_id,
            last_modified_by=self.actor_id
        )
            return self.repository.create(new_promotion)

        except UniqueViolationError as e:
            raise CompositeDuplicateEntityError(
                Promotion, str(e),
                f"This student has an existing promotion record for the {data.academic_session} session")



    def get_promotion(self, promotion_id: UUID) -> Promotion:
        """Get a specific promotion by ID."""
        try:
            return self.repository.get_by_id(promotion_id)
        except EntityNotFoundError as e:
            self.raise_not_found(promotion_id, e)


    def get_all_promotions(self, filters) -> List[Promotion]:
        """Get all active promotions with filtering."""
        fields = ['student_id', 'academic_session', 'status','status_completed_by']
        return self.repository.execute_query(fields, filters)

    @resolve_unique_violation({
        "uq_promotion_student_session": (
                "_", "This student has an existing promotion record for the specified academic session"
        )
    })
    @resolve_fk_on_update()
    def update_promotion(self, promotion_id: UUID, data: dict) -> Promotion:
        """Update a promotion record information."""
        try:
            existing = self.get_promotion(promotion_id)

            for key, value in data.items():
                if hasattr(existing, key):
                    setattr(existing, key, value)

            return self.repository.update(promotion_id, existing, modified_by=self.actor_id)

        except EntityNotFoundError as e:
            self.raise_not_found(promotion_id, e)



    def archive_promotion(self, promotion_id: UUID, reason) -> None:
        """Archive a promotion record."""
        try:
            failed_dependencies = self.archive_service.check_active_dependencies_exists(
                entity_model=self.model,
                target_id=promotion_id
            )
            if failed_dependencies:
                raise ArchiveDependencyError(
                    entity_model=self.entity_model, identifier=promotion_id,
                    display_name=self.display_name, related_entities=", ".join(failed_dependencies)
                )
            return self.repository.archive(promotion_id, self.actor_id, reason)

        except EntityNotFoundError as e:
            self.raise_not_found(promotion_id, e)


    @resolve_fk_on_delete()
    def delete_promotion(self, promotion_id: UUID, is_archived=False) -> None:
        """Permanently delete a promotion record."""
        try:
            self.delete_service.check_safe_delete(self.model, promotion_id, is_archived)
            return self.repository.delete(promotion_id)

        except EntityNotFoundError as e:
            self.raise_not_found(promotion_id, e)


    def get_all_archived_promotions(self, filters) -> List[Promotion]:
        """Get all archived promotion records with filtering."""
        fields = ['student_id', 'academic_session', 'status','status_completed_by']
        return self.repository.execute_archive_query(fields, filters)


    def get_archived_promotion(self, promotion_id: UUID) -> Promotion:
        """Get an archived promotion record by ID."""
        try:
            return self.repository.get_archive_by_id(promotion_id)
        except EntityNotFoundError as e:
            self.raise_not_found(promotion_id, e)


    def restore_promotion(self, promotion_id: UUID) -> Promotion:
        """Restore an archived promotion record."""
        try:
            return self.repository.restore(promotion_id)
        except EntityNotFoundError as e:
            self.raise_not_found(promotion_id, e)


    @resolve_fk_on_delete()
    def delete_archived_promotion(self, promotion_id: UUID, is_archived=True) -> None:
        """Permanently delete an archived promotion record."""
        try:
            self.delete_service.check_safe_delete(self.model, promotion_id, is_archived)
            self.repository.delete_archive(promotion_id)

        except EntityNotFoundError as e:
            self.raise_not_found(promotion_id, e)
