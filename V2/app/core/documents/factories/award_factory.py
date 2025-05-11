from typing import List
from uuid import UUID, uuid4
from sqlalchemy.orm import Session
from V2.app.core.documents.models.documents import StudentAward
from V2.app.core.documents.validators import DocumentValidator
from V2.app.core.shared.factory.base_factory import BaseFactory
from V2.app.core.shared.services.lifecycle_service.archive_service import ArchiveService
from V2.app.core.shared.services.lifecycle_service.delete_service import DeleteService
from V2.app.infra.db.repositories.sqlalchemy_repos.base_repo import SQLAlchemyRepository
from V2.app.core.shared.exceptions.decorators.resolve_unique_violation import resolve_unique_violation
from V2.app.core.shared.exceptions.decorators.resolve_fk_violation import resolve_fk_on_create, resolve_fk_on_update, resolve_fk_on_delete
from V2.app.core.shared.exceptions import EntityNotFoundError
from V2.app.core.shared.exceptions.maps.error_map import error_map


class AwardFactory(BaseFactory):
    """Factory class for managing Award operations."""

    def __init__(self, session: Session, model = StudentAward, current_user = None):
        super().__init__(current_user)
        """Initialize factory.
            Args:
            session: SQLAlchemy db session
            model: Model class, defaults to Award
            current_user: The authenticated user performing the operation, if any.
        """
        self.model = model
        self.repository = SQLAlchemyRepository(self.model, session)
        self.validator = DocumentValidator()
        self.delete_service = DeleteService(self.model, session)
        self.archive_service = ArchiveService(session)
        self.error_details = error_map.get(self.model)
        self.entity_model, self.display_name = self.error_details
        self.actor_id: UUID = self.get_actor_id()
        self.domain = "Award"

    def raise_not_found(self, identifier, error):
        raise EntityNotFoundError(
            entity_model=self.entity_model,
            identifier=identifier,
            error=str(error),
            display_name=self.display_name
        )


    @resolve_unique_violation({
        "uq_student_award_title_owner_id": ("title", lambda self, data: data.title)
    })
    @resolve_fk_on_create()
    def create_award(self, owner_id: UUID, data) -> StudentAward:
        """Create a new Award.
        Args:
            data: Award data
            owner_id: id of award owner
        Returns:
            Award: Created Award record
        """
        new_award = StudentAward(
            id=uuid4(),
            title=self.validator.validate_name(data.title),
            owner_id=owner_id,
            academic_session=self.validator.validate_academic_session(data.academic_session),

            created_by=self.actor_id,
            last_modified_by=self.actor_id
        )
        return self.repository.create(new_award)


    def get_award(self, award_id: UUID) -> StudentAward:
        """Get a specific Award by ID.
        Args:
            award_id (UUID): ID of Award to retrieve
        Returns:
            Award: Retrieved Award record
        """
        try:
            return self.repository.get_by_id(award_id)
        except EntityNotFoundError as e:
            self.raise_not_found(award_id, e)


    def get_all_awards(self, filters) -> List[StudentAward]:
        """Get all active Awards with filtering.
        Returns:
            List[Award]: List of active Awards
        """
        fields = ['title', 'academic_session']
        return self.repository.execute_query(fields, filters)


    @resolve_unique_violation({
        "uq_student_award_title_owner_id": ("title", lambda self, *a: a[-1].get("title"))
    })
    @resolve_fk_on_update()
    def update_award(self, award_id: UUID, data: dict) -> StudentAward:
        """Update Award information.
        Args:
            award_id (UUID): ID of Award to update
            data (dict): Dictionary containing fields to update
        Returns:
            Award: Updated Award record
        """
        copied_data = data.copy()
        try:
            existing = self.get_award(award_id)
            validations = {
                "title": (self.validator.validate_name, "title"),
            }

            for field, (validator_func, model_attr) in validations.items():
                if field in copied_data:
                    validated_value = validator_func(copied_data.pop(field))
                    setattr(existing, model_attr, validated_value)

            for key, value in copied_data.items():
                if hasattr(existing, key):
                    setattr(existing, key, value)

            return self.repository.update(award_id, existing, modified_by=self.actor_id)

        except EntityNotFoundError as e:
                self.raise_not_found(award_id, e)


    def archive_award(self, award_id: UUID, reason) -> None:
        """Archive Award
        Args:
            award_id (UUID): ID of Award to archive
            reason: Reason for archiving
        Returns:
            Award: Archived Award record
        """
        try:
            self.repository.archive(award_id, self.actor_id, reason)

        except EntityNotFoundError as e:
            self.raise_not_found(award_id, e)


    @resolve_fk_on_delete()
    def delete_award(self, award_id: UUID) -> None:
        """Permanently delete an Award
        Args:
            award_id (UUID): ID of Award to delete
        """
        try:
            self.repository.delete(award_id)

        except EntityNotFoundError as e:
            self.raise_not_found(award_id, e)

    def get_all_archived_awards(self, filters) -> List[StudentAward]:
        """Get all archived Awards with filtering.
        Returns:
            List[Award]: List of archived Award records
        """
        fields = ['title', 'academic_session']
        return self.repository.execute_archive_query(fields, filters)


    def get_archived_award(self, award_id: UUID) -> StudentAward:
        """Get an archived Award by ID.
        Args:
            award_id: ID of Award to retrieve
        Returns:
            Award: Retrieved Award record
        """
        try:
            return self.repository.get_archive_by_id(award_id)
        except EntityNotFoundError as e:
            self.raise_not_found(award_id, e)


    def restore_award(self, award_id: UUID) -> StudentAward:
        """Restore an archived Award.
        Args:
            award_id: ID of Award to restore
        Returns:
            Award: Restored Award record
        """
        try:
            return self.repository.restore(award_id)
        except EntityNotFoundError as e:
            self.raise_not_found(award_id, e)


    @resolve_fk_on_delete()
    def delete_archived_award(self, award_id: UUID) -> None:
        """Permanently delete an archived Award
        Args:
            award_id: ID of Award to delete
        """
        try:
            self.repository.delete_archive(award_id)

        except EntityNotFoundError as e:
            self.raise_not_found(award_id, e)
