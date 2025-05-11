from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from V2.app.core.shared.schemas.enums import ArchiveReason
from V2.app.core.academic_structure.models.academic_structure import Classes
from V2.app.core.academic_structure.factories.classes import ClassFactory
from V2.app.core.shared.services.export_service.export import ExportService
from V2.app.core.academic_structure.schemas.classes import (
    ClassCreate, ClassUpdate, ClassResponse, ClassFilterParams
)


class ClassCrud:
    """CRUD operations for classes."""

    def __init__(self, session: Session, current_user = None):
        """Initialize CRUD service.
        Args:
            session: SQLAlchemy db session
            current_user: The authenticated user performing the operation, if any.
        """
        self.session = session
        self.current_user = current_user
        self.factory = ClassFactory(session, current_user=current_user)
        self.export_service = ExportService(session)


    def create_class(self, data: ClassCreate) -> ClassResponse:
        """Create a new class.
        Args:
            data: Validated class creation data
        Returns:
            ClassResponse: Created class
        """
        new_class = self.factory.create_class(data)
        return ClassResponse.model_validate(new_class)


    def get_class(self, class_id: UUID) -> ClassResponse:
        """Get class by ID.
        Args:
            class_id: class UUID
        Returns:
            ClassResponse: Retrieved class
        """
        class_response = self.factory.get_class(class_id)
        return ClassResponse.model_validate(class_response)


    def get_all_classes(self, filters: ClassFilterParams) -> List[ClassResponse]:
        """Get all active class.
        Returns:
            List[ClassResponse]: List of active classes
        """
        classes = self.factory.get_all_classes(filters)
        return [ClassResponse.model_validate(a_class) for a_class in classes]


    def update_class(self, class_id: UUID, data: ClassUpdate) -> ClassResponse:
        """Update class information.
        Args:
            class_id: class UUID
            data: Validated update data
        Returns:
            ClassResponse: Updated class
        """
        data = data.model_dump(exclude_unset=True)
        updated_class = self.factory.update_class(class_id, data)
        return ClassResponse.model_validate(updated_class)

    def archive_class(self, class_id: UUID, reason: ArchiveReason) -> None:
        """Archive a class.
        Args:
            class_id: class UUID
            reason: Reason for archiving
        Returns:
            ClassResponse: Archived class
        """
        self.factory.archive_class(class_id, reason)

    def export_class(self, class_id: UUID, export_format: str) -> str:
        """Export class and its associated data
        Args:
            class_id: Class UUID
            export_format: Preferred export format
        """
        return self.export_service.export_entity(
            Classes, class_id, export_format
        )


    def delete_class(self, class_id: UUID) -> None:
        """Permanently delete a class.
        Args:
            class_id: class UUID
        """
        self.factory.delete_class(class_id)


    # Archived Class operations
    def get_archived_class(self, class_id: UUID) -> ClassResponse:
        """Get an archived class by ID.
        Args:
            class_id: class UUID
        Returns:
            ClassResponse: Retrieved archived class
        """
        class_response = self.factory.get_archived_class(class_id)
        return ClassResponse.model_validate(class_response)

    def get_all_archived_classes(self, filters: ClassFilterParams) -> List[ClassResponse]:
        """Get all archived classes.
        Args:
            filters: Filter parameters
        Returns:
            List[ClassResponse]: List of archived classes
        """
        classes = self.factory.get_all_archived_classes(filters)
        return [ClassResponse.model_validate(a_class) for a_class in classes]


    def restore_class(self, class_id: UUID) -> ClassResponse:
        """Restore an archived class.
        Args:
            class_id: class UUID
        Returns:
            ClassResponse: Restored class
        """
        restored_class = self.factory.restore_class(class_id)
        return ClassResponse.model_validate(restored_class)


    def delete_archived_class(self, class_id: UUID) -> None:
        """Permanently delete an archived class.
        Args:
            class_id: class UUID
        """
        self.factory.delete_archived_class(class_id)