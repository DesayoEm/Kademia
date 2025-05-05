from typing import List
from uuid import UUID, uuid4
from sqlalchemy.orm import Session
from V2.app.core.progression.models.progression import Promotion
from V2.app.core.shared.services.lifecycle_service.archive_service import ArchiveService
from V2.app.core.shared.services.lifecycle_service.delete_service import DeleteService
from V2.app.infra.db.repositories.sqlalchemy_repos.base_repo import SQLAlchemyRepository
from V2.app.core.shared.exceptions.decorators.resolve_unique_violation import resolve_unique_violation
from V2.app.core.shared.exceptions.decorators.resolve_fk_violation import resolve_fk_on_create, resolve_fk_on_update, resolve_fk_on_delete
from V2.app.core.shared.exceptions import EntityNotFoundError, ArchiveDependencyError
from V2.app.core.shared.exceptions.maps.error_map import error_map

SYSTEM_USER_ID = UUID('00000000-0000-0000-0000-000000000000')


class PromotionFactory:
    """Factory class for managing promotion operations."""

    def __init__(self, session: Session, model=Promotion):
        self.model = model
        self.repository = SQLAlchemyRepository(self.model, session)
        self.delete_service = DeleteService(self.model, session)
        self.archive_service = ArchiveService(session)
        self.error_details = error_map.get(self.model)
        self.entity_model, self.display_name = self.error_details
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
        new_promotion = Promotion(
            id=uuid4(),
            student_id=student_id,
            academic_session=data.academic_session,
            previous_level_id=data.previous_level_id,
            new_level_id=data.new_level_id,
            previous_class_id=data.previous_class_id,
            new_class_id=data.new_class_id,
            status=data.status,
            status_updated_by=data.status_updated_by,
            status_updated_at=data.status_updated_at,
            rejection_reason=data.rejection_reason,
            created_by=SYSTEM_USER_ID,
            last_modified_by=SYSTEM_USER_ID
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

            existing.last_modified_by = SYSTEM_USER_ID
            return self.repository.update(promotion_id, existing)

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
            return self.repository.archive(promotion_id, SYSTEM_USER_ID, reason)

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
