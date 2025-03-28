from typing import List
from uuid import uuid4, UUID
from sqlalchemy.orm import Session
from ....core.errors.database_errors import RelationshipError
from ....core.errors.user_profile_errors import RelatedEducatorNotFoundError, RelatedStudentNotFoundError
from ....core.errors.student_organisation_errors import  RelatedLevelNotFoundError
from ....core.errors.student_organisation_errors import (
    DuplicateClassError, ClassNotFoundError
)
from ....core.errors.database_errors import EntityNotFoundError, UniqueViolationError
from ....database.db_repositories.sqlalchemy_repos.base_repo import SQLAlchemyRepository
from ....database.models.enums import ArchiveReason
from ....core.services.student_organization.classes import ClassService
from ....core.validators.student_organization import StudentOrganizationValidator
from ....database.models.student_organization import Classes



SYSTEM_USER_ID = UUID('00000000-0000-0000-0000-000000000000')

class ClassFactory:
    """Factory class for managing class operations."""
    def __init__(self, session: Session):
        self.repository = SQLAlchemyRepository(Classes, session)
        self.validator = StudentOrganizationValidator()
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
            supervisor_id = new_class.supervisor_id,
            student_rep_id =  new_class.student_rep_id,
            assistant_rep_id = new_class.assistant_rep_id,
            created_by=SYSTEM_USER_ID,
            last_modified_by=SYSTEM_USER_ID,

        )
        class_data.order = self.service.create_order(new_class.level_id)
        try:
            return self.repository.create(class_data)
        except UniqueViolationError as e:  # Could either be code or order
            error_message = str(e)
            if "uq_class_level_code" in error_message.lower():
                raise DuplicateClassError(
                    input_value=class_data.code.value, field="", detail=error_message)#None is a filler attr hare
            elif "classes_order_key" in error_message.lower():
                raise DuplicateClassError(
                    input_value=str(class_data.order), field="order", detail=error_message)
            else:
                raise DuplicateClassError(
                    input_value="unknown field", field="unknown", detail=error_message)

        except RelationshipError as e:
            error_message = str(e)
            fk_error_mapping = {
                'fk_classes_academic_levels_level_id': ('level_id', RelatedLevelNotFoundError),
                'fk_classes_educators_supervisor_id': ('supervisor_id', RelatedEducatorNotFoundError),
                'fk_classes_students_student_rep': ('student_rep_id', RelatedStudentNotFoundError),
                'fk_classes_students_assistant_rep': ('assistant_rep_id', RelatedStudentNotFoundError),
            }
            for fk_constraint, (attr_name, error_class) in fk_error_mapping.items():
                if fk_constraint in error_message:
                    entity_id = getattr(new_class, attr_name, None)
                    if entity_id:
                        raise error_class(id=entity_id, detail=error_message, action='create')

            raise RelationshipError(error=error_message, operation='create', entity='unknown_entity')

    def get_class(self, class_id: UUID) -> Classes:
        """Get a specific class by ID.
        Args:
            class_id (UUID): ID of class to retrieve
        Returns:
            Classes: Retrieved class record
        """
        try:
            return self.repository.get_by_id(class_id)
        except EntityNotFoundError as e:
            raise ClassNotFoundError(id=class_id, detail = str(e))


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
        original = data.copy()
        try:
            existing = self.get_class(class_id)
            for key, value in data.items():
                if hasattr(existing, key):
                    setattr(existing, key, value)
            existing.last_modified_by = SYSTEM_USER_ID

            return self.repository.update(class_id, existing)
        except EntityNotFoundError as e:
            raise ClassNotFoundError(id=class_id, detail = str(e))
        except UniqueViolationError as e:
            error_message= str(e)
            if "classes_order_key" in error_message.lower():
                raise DuplicateClassError(
                    input_value=str(original.get('order', 'unknown')), field="order", detail=error_message)
            else:
                raise DuplicateClassError(
                    input_value="unknown field", field="unknown", detail=error_message)
        except RelationshipError as e:
            error_message = str(e)
            fk_error_mapping = {
                'fk_classes_academic_levels_level_id': ('level_id', RelatedLevelNotFoundError),
                'fk_classes_educators_supervisor_id': ('supervisor_id', RelatedEducatorNotFoundError),
                'fk_classes_students_student_rep': ('student_rep_id', RelatedStudentNotFoundError),
                'fk_classes_students_assistant_rep': ('assistant_rep_id', RelatedStudentNotFoundError),
            }
            for fk_constraint, (attr_name, error_class) in fk_error_mapping.items():
                if fk_constraint in error_message:
                    entity_id = data.get(attr_name, None)
                    if entity_id:
                        raise error_class(id=entity_id, detail=error_message, action='update')

            raise RelationshipError(error=error_message, operation='update', entity='unknown_entity')

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
        except EntityNotFoundError as e:
            raise ClassNotFoundError(id=class_id, detail = str(e))


    def delete_class(self, class_id: UUID) -> None:
        """Permanently delete a class.
        Args:
            class_id (UUID): ID of class to delete
        """
        try:
            self.repository.delete(class_id)
        except EntityNotFoundError as e:
            raise ClassNotFoundError(id=class_id, detail = str(e))


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
        except EntityNotFoundError as e:
            raise ClassNotFoundError(id=class_id, detail = str(e))

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
        except EntityNotFoundError as e:
            raise ClassNotFoundError(id=class_id, detail = str(e))


    def delete_archived_class(self, class_id: UUID) -> None:
        """Permanently delete an archived class.
        Args:
            class_id: ID of class to delete
        """
        try:
            self.repository.delete_archive(class_id)
        except EntityNotFoundError as e:
            raise ClassNotFoundError(id=class_id, detail = str(e))

