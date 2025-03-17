from typing import List
from uuid import uuid4, UUID
from sqlalchemy.orm import Session
from ....database.db_repositories.sqlalchemy_repos.main_repo import SQLAlchemyRepository
from ....database.models.data_enums import ArchiveReason
from ....services.errors.database_errors import EntityNotFoundError, UniqueViolationError
from ....services.student_organization.validators import StudentOrganizationValidators
from ....database.models.student_organization import AcademicLevel
from ....services.errors.student_organisation_errors import (
    DuplicateLevelError, LevelNotFoundError
)

SYSTEM_USER_ID = UUID('00000000-0000-0000-0000-000000000000')

class AcademicLevelFactory:
    """Factory class for managing academic level operations."""
    def __init__(self, session: Session):
        self.repository = SQLAlchemyRepository(AcademicLevel, session)
        self.validator = StudentOrganizationValidators()

    def create_academic_level(self, new_academic_level) -> AcademicLevel:
        """Create a new academic level.
        Args:
            new_academic_level: Academic_level data containing name and description
        Returns:
            AcademicLevel: Created academic_level record
        """
        academic_level = AcademicLevel(
            id = uuid4(),
            name = self.validator.validate_name(new_academic_level.name),
            description = self.validator.validate_name(new_academic_level.description),
            order = new_academic_level.order,
            created_by=SYSTEM_USER_ID,#Placeholder until auth is implemented
            last_modified_by=SYSTEM_USER_ID
        )
        try:
            return self.repository.create(academic_level)
        except UniqueViolationError as e:#Could either be on name or order
            error_message = str(e)
            if "academic_levels_name_key" in error_message.lower():
                raise DuplicateLevelError(
                    input_value=new_academic_level.name, field = "name",detail=error_message)
            elif "academic_levels_order_key" in error_message.lower():
                raise DuplicateLevelError(
                    input_value=str(new_academic_level.order),field = "order",detail=error_message)
            else:#edge case idk
                raise DuplicateLevelError(
                    input_value="unknown field", field = "unknown", detail=error_message)


    def get_academic_level(self, academic_level_id: UUID) -> AcademicLevel:
        """Get a specific academic level by ID.
        Args:
            academic_level_id (UUID): ID of academic_level to retrieve
        Returns:
            AcademicLevel: Retrieved academic_level record
        """
        try:
            return self.repository.get_by_id(academic_level_id)
        except EntityNotFoundError:
            raise LevelNotFoundError(id=academic_level_id)


    def get_all_academic_levels(self, filters) -> List[AcademicLevel]:
        """Get all active academic_levels with filtering.
        Returns:
            List[AcademicLevel]: List of active academic_levels
        """
        fields = ['name', 'description']
        return self.repository.execute_query(fields, filters)

    def update_academic_level(self, academic_level_id: UUID, data: dict) -> AcademicLevel:
        """Update an academic level's information.
        Args:
            academic_level_id (UUID): ID of academic_level to update
            data (dict): Dictionary containing fields to update
        Returns:
            AcademicLevel: Updated academic_level record
        """
        try:
            existing = self.get_academic_level(academic_level_id)
            if 'name' in data:
                existing.name = self.validator.validate_name(data['name'])
            if 'description' in data:
                existing.description = self.validator.validate_name(data['description'])
            if 'order' in data:
                existing.order = int(data['order'])

            existing.last_modified_by = SYSTEM_USER_ID

            return self.repository.update(academic_level_id, existing)
        except EntityNotFoundError:
            raise LevelNotFoundError(id=academic_level_id)
        except UniqueViolationError as e:  # Could either be on name or order
            error_message = str(e)
            if "academic_levels_name_key" in error_message.lower():
                raise DuplicateLevelError(
                    input_value=data['name'], field="name", detail=error_message)
            elif "academic_levels_order_key" in error_message.lower():
                raise DuplicateLevelError(
                    input_value=str(data['order']), field="order", detail=error_message)
            else:
                raise DuplicateLevelError(
                    input_value="unknown field", field="unknown", detail=error_message)


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
        except EntityNotFoundError:
            raise LevelNotFoundError(id=academic_level_id)


    def delete_academic_level(self, academic_level_id: UUID) -> None:
        """Permanently delete an academic level.
        Args:
            academic_level_id (UUID): ID of academic_level to delete
        """
        try:
            self.repository.delete(academic_level_id)
        except EntityNotFoundError:
            raise LevelNotFoundError(id=academic_level_id)


    def get_all_archived_academic_levels(self, filters) -> List[AcademicLevel]:
        """Get all archived academic_levels with filtering.
        Returns:
            List[AcademicLevel]: List of archived academic_level records
        """
        fields = ['name', 'description']
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
        except EntityNotFoundError:
            raise LevelNotFoundError(id=academic_level_id)

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
        except EntityNotFoundError:
            raise LevelNotFoundError(id=academic_level_id)


    def delete_archived_academic_level(self, academic_level_id: UUID) -> None:
        """Permanently delete an archived academic_level.
        Args:
            academic_level_id: ID of academic_level to delete
        """
        try:
            self.repository.delete_archive(academic_level_id)
        except EntityNotFoundError:
            raise LevelNotFoundError(id=academic_level_id)

