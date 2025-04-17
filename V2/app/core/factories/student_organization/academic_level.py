from typing import List
from uuid import uuid4, UUID
from sqlalchemy.orm import Session

from ....core.services.student_organization.academic_level import AcademicLevelService
from ....database.db_repositories.sqlalchemy_repos.base_repo import SQLAlchemyRepository
from ....database.models.enums import ArchiveReason
from ....core.errors.database_errors import EntityNotFoundError, UniqueViolationError, RelationshipError
from ....core.validators.student_organization import StudentOrganizationValidator
from ....database.models.student_organization import AcademicLevel


SYSTEM_USER_ID = UUID('00000000-0000-0000-0000-000000000000')

class AcademicLevelFactory:
    """Factory class for managing academic level operations."""
    def __init__(self, session: Session):
        self.repository = SQLAlchemyRepository(AcademicLevel, session)
        self.validator = StudentOrganizationValidator()
        self.service = AcademicLevelService(session)
        self.session = session


    def create_academic_level(self, new_academic_level) -> AcademicLevel:
        """Create a new academic level.
        Args:
            new_academic_level: Academic_level data containing name and description
        Returns:
            AcademicLevel: Created academic_level record
        """
        academic_level = AcademicLevel(
            id = uuid4(),
            name = self.validator.validate_level_name(new_academic_level.name),
            description = self.validator.validate_description(new_academic_level.description),
            order = self.service.return_default_order(),

            created_by=SYSTEM_USER_ID,
            last_modified_by=SYSTEM_USER_ID
        )
        try:
            return self.repository.create(academic_level)

        except UniqueViolationError as e:
            error_message = str(e).lower()
            if "academic_levels_name_key" in error_message:
                raise DuplicateLevelError(
                    entry=new_academic_level.name, field = "name",detail=error_message)
            elif "academic_levels_order_key" in error_message:
                raise DuplicateLevelError(
                    entry=str(new_academic_level.order),field = "order",detail=error_message)
            else:
                raise DuplicateLevelError(
                    entry="unknown field", field = "unknown", detail=error_message)


    def get_academic_level(self, academic_level_id: UUID) -> AcademicLevel:
        """Get a specific academic level by ID.
        Args:
            academic_level_id (UUID): ID of academic_level to retrieve
        Returns:
            AcademicLevel: Retrieved academic_level record
        """
        try:
            return self.repository.get_by_id(academic_level_id)

        except EntityNotFoundError as e:
            raise LevelNotFoundError(identifier=academic_level_id, detail= str(e))


    def get_all_academic_levels(self, filters) -> List[AcademicLevel]:
        """Get all active academic_levels with filtering.
        Returns:
            List[AcademicLevel]: List of active academic_levels
        """
        fields = ['name']
        return self.repository.execute_query(fields, filters)


    def update_academic_level(self, academic_level_id: UUID, data: dict) -> AcademicLevel:
        """Update an academic level's information.
        Args:
            academic_level_id (UUID): ID of academic_level to update
            data (dict): Dictionary containing fields to update
        Returns:
            AcademicLevel: Updated academic_level record
        """
        original = data.copy()
        try:
            existing = self.get_academic_level(academic_level_id)

            validations = {
                "name": (self.validator.validate_level_name, "name"),
                "description": (self.validator.validate_description, "description"),
                "order": (self.validator.validate_order, "order"),
            }

            for field, (validator_func, model_attr) in validations.items():
                if field in data:
                    validated_value = validator_func(data.pop(field))
                    setattr(existing, model_attr, validated_value)

            for key, value in data.items():
                if hasattr(existing, key):
                    setattr(existing, key, value)
            existing.last_modified_by = SYSTEM_USER_ID

            return self.repository.update(academic_level_id, existing)

        except EntityNotFoundError as e:
            raise LevelNotFoundError(identifier=academic_level_id, detail=str(e))

        except UniqueViolationError as e:  # Could either be on name or order
            error_message = str(e)
            if "academic_levels_name_key" in error_message.lower():
                raise DuplicateLevelError(
                    entry=original.get('name', 'unknown'), field="name", detail=error_message)
            elif "academic_levels_order_key" in error_message.lower():
                raise DuplicateLevelError(
                    entry=original.get('order', 'unknown'), field="order", detail=error_message)
            else:
                raise DuplicateLevelError(
                    entry="unknown field", field="unknown", detail=error_message)


    def archive_academic_level(self, academic_level_id: UUID, reason: ArchiveReason) -> AcademicLevel:
        """Archive aN academic level.
        Args:
            academic_level_id (UUID): ID of academic_level to archive
            reason (ArchiveReason): Reason for archiving
        Returns:
            AcademicLevel: Archived academic_level record
        """
        try:
            return self.repository.archive(academic_level_id, SYSTEM_USER_ID, reason)

        except EntityNotFoundError as e:
            raise LevelNotFoundError(identifier=academic_level_id, detail=str(e))


    def delete_academic_level(self, academic_level_id: UUID) -> None:
        """Permanently delete an academic level.
        Args:
            academic_level_id (UUID): ID of academic_level to delete
        """
        try:
            level = self.session.execute(
                select(AcademicLevel)
                .options(selectinload(AcademicLevel.classes))
                .where(AcademicLevel.id == academic_level_id)
            ).scalar_one_or_none()

            if level.classes:
                raise LevelInUseError(entity_name="a class",
                    detail=f"Deletion attempt blocked for AcademicLevel {academic_level_id}: linked to a class. "
                    f"Raised manually during pre-deletion validation.")

            self.repository.delete(academic_level_id)

        except EntityNotFoundError as e:
            raise LevelNotFoundError(identifier=academic_level_id, detail=str(e))

        except RelationshipError as e: #Failsafe
            raise RelationshipError(error=str(e), operation='delete', entity='unknown_entity')


    def get_all_archived_academic_levels(self, filters) -> List[AcademicLevel]:
        """Get all archived academic_levels with filtering.
        Returns:
            List[AcademicLevel]: List of archived academic_level records
        """
        fields = ['name']
        return self.repository.execute_archive_query(fields, filters)


    def get_archived_academic_level(self, academic_level_id: UUID) -> AcademicLevel:
        """Get an archived academic_level by ID.
        Args:
            academic_level_id: ID of academic_level to retrieve
        Returns:
            AcademicLevel: Retrieved academic_level record
        """
        try:
            return self.repository.get_archive_by_id(academic_level_id)

        except EntityNotFoundError as e:
            raise LevelNotFoundError(identifier=academic_level_id, detail=str(e))

    def restore_academic_level(self, academic_level_id: UUID) -> AcademicLevel:
        """Restore an archived academic_level.
        Args:
            academic_level_id: ID of academic_level to restore
        Returns:
            AcademicLevel: Restored academic_level record
        """
        try:
            archived = self.get_archived_academic_level(academic_level_id)
            archived.last_modified_by = SYSTEM_USER_ID
            return self.repository.restore(academic_level_id)

        except EntityNotFoundError as e:
            raise LevelNotFoundError(identifier=academic_level_id, detail=str(e))


    def delete_archived_academic_level(self, academic_level_id: UUID) -> None:
        """Permanently delete an archived academic_level.
        Args:
            academic_level_id: ID of academic_level to delete
        """
        try:
            self.repository.delete_archive(academic_level_id)

        except EntityNotFoundError as e:
            raise LevelNotFoundError(identifier=academic_level_id, detail=str(e))

        except RelationshipError as e:
            error_message = str(e)
            # Note: There are no referenced FKs, so RelationshipError may not trigger here,
            # but it is being kept for unexpected constraint issues.
            raise RelationshipError(error=error_message, operation='delete', entity='unknown_entity')
