
from typing import List
from uuid import UUID, uuid4
from sqlalchemy.orm import Session

from app.core.shared.factory.base_factory import BaseFactory
from app.core.shared.services.lifecycle_service.archive_service import ArchiveService
from app.core.shared.services.lifecycle_service.delete_service import DeleteService
from app.infra.db.repositories.sqlalchemy_repos.base_repo import SQLAlchemyRepository
from app.core.shared.exceptions.decorators.resolve_fk_violation import resolve_fk_on_create, resolve_fk_on_delete, \
    resolve_fk_on_update
from app.core.shared.exceptions import EntityNotFoundError, ArchiveDependencyError
from app.core.shared.exceptions.maps.error_map import error_map
from app.core.transfer.models.transfer import DepartmentTransfer



class TransferFactory(BaseFactory):
    """Factory class for managing department transfer operations."""

    def __init__(self, session: Session, model=DepartmentTransfer, current_user = None):
        super().__init__(current_user)
        """Initialize factory with db session, model and current user.
        Args:
            session: SQLAlchemy db session
            model: Model class, defaults to StudentDepartmentTransfer
            current_user: The authenticated user performing the operation, if any.
        """

        self.model = model
        self.session = session
        self.repository = SQLAlchemyRepository(self.model, session)
        self.delete_service = DeleteService(self.model, session)
        self.archive_service = ArchiveService(session)
        self.error_details = error_map.get(self.model)
        self.entity_model, self.display_name = self.error_details
        self.actor_id: UUID = self.get_actor_id()
        self.domain = "DepartmentTransfer"

    def raise_not_found(self, identifier, error):
        raise EntityNotFoundError(
            entity_model=self.entity_model,
            identifier=identifier,
            error=str(error),
            display_name=self.display_name
        )

    @resolve_fk_on_create()
    def create_transfer(self, student_id: UUID, data) -> DepartmentTransfer:

        from app.core.identity.models.student import Student
        from app.core.identity.factories.student import StudentFactory
        student_factory = StudentFactory(self.session, Student, self.current_user)
        student = student_factory.get_student(student_id)

        new_transfer = DepartmentTransfer(
            id=uuid4(),
            student_id=student_id,
            academic_session=data.academic_session,
            previous_department_id=student.department_id,
            new_department_id=data.new_department_id,
            reason=data.reason,
            created_by=self.actor_id,
            last_modified_by=self.actor_id
        )
        return self.repository.create(new_transfer)


    def get_transfer(self, transfer_id: UUID) -> DepartmentTransfer:
        try:
            return self.repository.get_by_id(transfer_id)
        except EntityNotFoundError as e:
            self.raise_not_found(transfer_id, e)


    def get_all_transfers(self, filters) -> List[DepartmentTransfer]:
        fields = [
            'student_id','previous_department_id', 'new_department_id','academic_session', 'status',
            'status_completed_by'
        ]
        return self.repository.execute_archive_query(fields, filters)


    @resolve_fk_on_update()
    def update_transfer(self, transfer_id: UUID, data: dict) -> DepartmentTransfer:
        """Update a transfer record information."""
        from app.core.transfer.services.transfer_service import TransferService
        service = TransferService(self.session, self.current_user)

        try:
            existing = self.get_transfer(transfer_id)
            if "reason" in data:
                existing.transfer_reason = data["reason"]

            for key, value in data.items():
                if hasattr(existing, key):
                    setattr(existing, key, value)

            return self.repository.update(transfer_id, existing, modified_by=self.actor_id)

        except EntityNotFoundError as e:
            self.raise_not_found(transfer_id, e)
            
    def archive_transfer(self, transfer_id: UUID, reason) -> None:
        """Archive a transfer record."""
        try:
            failed_dependencies = self.archive_service.check_active_dependencies_exists(
                entity_model=self.model,
                target_id=transfer_id
            )
            if failed_dependencies:
                raise ArchiveDependencyError(
                    entity_model=self.entity_model, identifier=transfer_id,
                    display_name=self.display_name, related_entities=", ".join(failed_dependencies)
                )
            return self.repository.archive(transfer_id, self.actor_id, reason)

        except EntityNotFoundError as e:
            self.raise_not_found(transfer_id, e)


    @resolve_fk_on_delete()
    def delete_transfer(self, transfer_id: UUID, is_archived=False):
        try:
            self.delete_service.check_safe_delete(self.model, transfer_id, is_archived)
            return self.repository.delete(transfer_id)
        except EntityNotFoundError as e:
            self.raise_not_found(transfer_id, e)


    def get_all_archived_transfers(self, filters) -> List[DepartmentTransfer]:
        fields = [
            'student_id', 'previous_department_id', 'new_department_id', 'academic_session', 'status',
            'status_completed_by'
        ]
        return self.repository.execute_archive_query(fields, filters)


    def get_archived_transfer(self, transfer_id: UUID) -> DepartmentTransfer:
        try:
            return self.repository.get_archive_by_id(transfer_id)
        except EntityNotFoundError as e:
            self.raise_not_found(transfer_id, e)


    def restore_transfer(self, transfer_id: UUID) -> DepartmentTransfer:
        try:
            return self.repository.restore(transfer_id)
        except EntityNotFoundError as e:
            self.raise_not_found(transfer_id, e)


    @resolve_fk_on_delete()
    def delete_archived_transfer(self, transfer_id: UUID, is_archived=True):
        try:
            self.delete_service.check_safe_delete(self.model, transfer_id, is_archived)
            self.repository.delete_archive(transfer_id)
        except EntityNotFoundError as e:
            self.raise_not_found(transfer_id, e)
