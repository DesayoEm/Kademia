from typing import List
from uuid import UUID, uuid4
from sqlalchemy.orm import Session

from V2.app.core.academic_structure.factories.academic_level import AcademicLevelFactory
from V2.app.core.academic_structure.models.academic_structure import AcademicLevel
from V2.app.core.identity.factories.student import StudentFactory
from V2.app.core.identity.models.student import Student
from V2.app.core.progression.models.progression import Promotion
from V2.app.core.progression.validators import ProgressionValidator
from V2.app.core.shared.factory.base_factory import BaseFactory
from V2.app.core.shared.services.lifecycle_service.archive_service import ArchiveService
from V2.app.core.shared.services.lifecycle_service.delete_service import DeleteService
from V2.app.infra.db.repositories.sqlalchemy_repos.base_repo import SQLAlchemyRepository
from V2.app.core.shared.exceptions.decorators.resolve_unique_violation import resolve_unique_violation
from V2.app.core.shared.exceptions.decorators.resolve_fk_violation import resolve_fk_on_create, resolve_fk_on_update, resolve_fk_on_delete
from V2.app.core.shared.exceptions import EntityNotFoundError, ArchiveDependencyError
from V2.app.core.shared.exceptions.maps.error_map import error_map



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
        self.repository = SQLAlchemyRepository(self.model, session)
        self.delete_service = DeleteService(self.model, session)
        self.archive_service = ArchiveService(session)
        self.validator = ProgressionValidator()
        self.error_details = error_map.get(self.model)
        self.entity_model, self.display_name = self.error_details
        self.actor_id: UUID = self.get_actor_id()
        self.domain = "Promotion"

    def raise_not_found(self, identifier, error):
        raise EntityNotFoundError(
            entity_model=self.entity_model,
            identifier=identifier,
            error=str(error),
            display_name=self.display_name
        )

    @resolve_fk_on_create()
    def create_promotion(self, student_id: UUID, data) -> Promotion:
        """Create a new promotion record for a student."""
        student_factory = StudentFactory(self.session, Student)
        academic_factory = AcademicLevelFactory(self.session, AcademicLevel)

        student = student_factory.get_student(student_id)

        previous_level = academic_factory.get_academic_level(student.level_id)
        new_level = academic_factory.get_academic_level(data.new_level_id)

        validated_new_level = self.validator.validate_next_level(previous_level, new_level)

        new_promotion = Promotion(
            id=uuid4(),
            student_id=student_id,
            academic_session=data.academic_session,
            previous_level_id=previous_level.id,
            new_level_id=validated_new_level.id,

            status=data.status,
            created_by=self.actor_id,
            last_modified_by=self.actor_id
        )
        return self.repository.create(new_promotion)


    def get_promotion(self, promotion_id: UUID) -> Promotion:
        """Get a specific promotion by ID."""
        try:
            return self.repository.get_by_id(promotion_id)
        except EntityNotFoundError as e:
            self.raise_not_found(promotion_id, e)


    def get_all_promotions(self, filters) -> List[Promotion]:
        """Get all active promotions with filtering."""
        fields = ['academic_session', 'status']
        return self.repository.execute_query(fields, filters)


    @resolve_fk_on_update()
    def update_promotion(self, promotion_id: UUID, data: dict) -> Promotion:
        """Update a promotion record."""
        copied_data = data.copy()
        try:
            existing = self.get_promotion(promotion_id)

            for key, value in copied_data.items():
                if hasattr(existing, key):
                    setattr(existing, key, value)

            return self.repository.update(promotion_id, existing, modified_by=self.actor_id)

        except EntityNotFoundError as e:
            self.raise_not_found(promotion_id, e)


    def archive_promotion(self, promotion_id: UUID, reason) -> Promotion:
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
        fields = ['academic_session', 'status']
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
