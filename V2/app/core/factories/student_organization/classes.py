from typing import List
from uuid import uuid4, UUID
from sqlalchemy.orm import Session
from V2.app.core.errors.database_errors import RelationshipError
from V2.app.core.errors.student_organisation_errors import LevelNotFoundError
from V2.app.core.errors.student_organisation_errors import (
    DuplicateClassError, ClassNotFoundError
)
from V2.app.core.errors.database_errors import EntityNotFoundError, UniqueViolationError
from V2.app.database.db_repositories.sqlalchemy_repos.main_repo import SQLAlchemyRepository
from V2.app.database.models.data_enums import ArchiveReason
from V2.app.core.services.student_organization.classes import ClassService
from V2.app.core.validators.student_organization import StudentOrganizationValidators
from V2.app.database.models.student_organization import Classes



SYSTEM_USER_ID = UUID('00000000-0000-0000-0000-000000000000')

class ClassFactory:
    """Factory class for managing class operations."""
    def __init__(self, session: Session):
        self.repository = SQLAlchemyRepository(Classes, session)
        self.validator = StudentOrganizationValidators()
        self.service = ClassService(session)


    def create_class(self, new_class) -> Classes:
        """Create a new class.
        Args:
            new_class: class data containing name and description
        Returns:
            Classes: Created class record
        """
        class_data = Classes(
            id = uuid4(),
            level_id = new_class.level_id,
            code = new_class.code,
            created_by=SYSTEM_USER_ID,
            last_modified_by=SYSTEM_USER_ID,
            order = new_class.order
        )
        if not class_data.order:
            class_data.order = self.service.create_order(new_class.level_id)
        try:
            return self.repository.create(class_data)
        except UniqueViolationError as e:  # Could either be code or order
            error_message = str(e)
            if "uq_class_level_code" in error_message.lower():
                raise DuplicateClassError(
                    input_value=class_data.code, field="None", detail=error_message)#None is a filler attr hare
            elif "classes_order_key" in error_message.lower():
                raise DuplicateClassError(
                    input_value=str(class_data.order), field="order", detail=error_message)
            else:
                raise DuplicateClassError(
                    input_value="unknown field", field="unknown", detail=error_message)
        except RelationshipError:
            raise LevelNotFoundError(id = new_class.level_id) #Edge case: the possibility of another relationship error, not related to level_id

    def get_class(self, class_id: UUID) -> Classes:
        """Get a specific class by ID.
        Args:
            class_id (UUID): ID of class to retrieve
        Returns:
            Classes: Retrieved class record
        """
        try:
            return self.repository.get_by_id(class_id)
        except EntityNotFoundError:
            raise ClassNotFoundError(id=class_id)


    def get_all_classes(self, filters) -> List[Classes]:
        """Get all active student_organization with filtering.
        Returns:
            List[Classes]: List of active student_organization
        """
        fields = ['level_id', 'code']
        return self.repository.execute_query(fields, filters)

    def update_class(self, class_id: UUID, data: dict) -> Classes:
        """Update a class's information.
        Args:
            class_id (UUID): ID of class to update
            data (dict): Dictionary containing fields to update
        Returns:
            Classes: Updated class record
        """
        try:
            existing = self.get_class(class_id)
            if 'level_id' in data:
                existing.level_id = data['level_id']
            if 'code' in data:
                existing.code = data['code']
            existing.last_modified_by = SYSTEM_USER_ID
            return self.repository.update(class_id, existing)
        except EntityNotFoundError:
            raise ClassNotFoundError(id=class_id)
        except UniqueViolationError as e:
            error_message= str(e)
            if "classes_order_key" in error_message.lower():
                raise DuplicateClassError(
                    input_value=str(data['order']), field="order", detail=error_message)
            else:
                raise DuplicateClassError(
                    input_value="unknown field", field="unknown", detail=error_message)


    def archive_class(self, class_id: UUID, reason: ArchiveReason) -> Classes:
        """Archive a class.
        Args:
            class_id (UUID): ID of class to archive
            reason (ArchiveReason): Reason for archiving
        Returns:
            Classes: Archived class record
        """
        try:
            return self.repository.archive(class_id, SYSTEM_USER_ID, reason)
        except EntityNotFoundError:
            raise ClassNotFoundError(id=class_id)


    def delete_class(self, class_id: UUID) -> None:
        """Permanently delete a class.
        Args:
            class_id (UUID): ID of class to delete
        """
        try:
            self.repository.delete(class_id)
        except EntityNotFoundError:
            raise ClassNotFoundError(id=class_id)


    def get_all_archived_classes(self, filters) -> List[Classes]:
        """Get all archived student_organization with filtering.
        Returns:
            List[Classes]: List of archived class records
        """
        fields = ['level_id', 'code']
        return self.repository.execute_archive_query(fields, filters)


    def get_archived_class(self, class_id: UUID) -> Classes:
        """Get an archived class by ID.
        Args:
            class_id: ID of class to retrieve
        Returns:
            Classes: Retrieved class record
        """
        try:
            return self.repository.get_archive_by_id(class_id)
        except EntityNotFoundError:
            raise ClassNotFoundError(id=class_id)

    def restore_class(self, class_id: UUID) -> Classes:
        """Restore an archived class.
        Args:
            class_id: ID of class to restore
        Returns:
            Classes: Restored class record
        """
        try:
            archived = self.get_archived_class(class_id)
            archived.last_modified_by = SYSTEM_USER_ID
            return self.repository.restore(class_id)
        except EntityNotFoundError:
            raise ClassNotFoundError(id=class_id)


    def delete_archived_class(self, class_id: UUID) -> None:
        """Permanently delete an archived class.
        Args:
            class_id: ID of class to delete
        """
        try:
            self.repository.delete_archive(class_id)
        except EntityNotFoundError:
            raise ClassNotFoundError(id=class_id)

