
from typing import List
from uuid import UUID, uuid4
from sqlalchemy.orm import Session
from V2.app.core.shared.services.lifecycle_service.archive_service import ArchiveService
from V2.app.core.shared.services.lifecycle_service.delete_service import DeleteService
from V2.app.infra.db.repositories.sqlalchemy_repos.base_repo import SQLAlchemyRepository
from V2.app.core.shared.exceptions.decorators.resolve_fk_violation import resolve_fk_on_create, resolve_fk_on_update, resolve_fk_on_delete
from V2.app.core.shared.exceptions import EntityNotFoundError, ArchiveDependencyError
from V2.app.core.shared.exceptions.maps.error_map import error_map
from V2.app.core.transfer.models.transfer import StudentDepartmentTransfer


SYSTEM_USER_ID = UUID('00000000-0000-0000-0000-000000000000')



class DepartmentTransferFactory:
    """Factory class for managing department transfer operations."""

    def __init__(self, session: Session, model=StudentDepartmentTransfer):
        self.model = model
        self.repository = SQLAlchemyRepository(self.model, session)
        self.delete_service = DeleteService(self.model, session)
        self.archive_service = ArchiveService(session)
        self.error_details = error_map.get(self.model)
        self.entity_model, self.display_name = self.error_details
        self.domain = "StudentDepartmentTransfer"

    def raise_not_found(self, identifier, error):
        raise EntityNotFoundError(
            entity_model=self.entity_model,
            identifier=identifier,
            error=str(error),
            display_name=self.display_name
        )

    @resolve_fk_on_create()
    def create_transfer(self, student_id: UUID, data) -> StudentDepartmentTransfer:
        new_transfer = StudentDepartmentTransfer(
            id=uuid4(),
            student_id=student_id,
            academic_session=int(data.academic_session.split("/")[0]),
            previous_level_id=data.previous_level_id,
            new_level_id=data.new_level_id,
            previous_class_id=data.previous_class_id,
            new_class_id=data.new_class_id,
            previous_department_id=data.previous_department_id,
            new_department_id=data.new_department_id,
            reason=data.reason,
            status=data.status,
            status_updated_by=data.status_updated_by,
            status_updated_at=data.status_updated_at,
            rejection_reason=data.rejection_reason,
            created_by=SYSTEM_USER_ID,
            last_modified_by=SYSTEM_USER_ID
        )
        return self.repository.create(new_transfer)

    def get_transfer(self, transfer_id: UUID) -> StudentDepartmentTransfer:
        try:
            return self.repository.get_by_id(transfer_id)
        except EntityNotFoundError as e:
            self.raise_not_found(transfer_id, e)

    def get_all_transfers(self, filters) -> List[StudentDepartmentTransfer]:
        return self.repository.execute_query(['academic_session', 'status'], filters)

    @resolve_fk_on_update()
    def update_transfer(self, transfer_id: UUID, data: dict) -> StudentDepartmentTransfer:
        copied_data = data.copy()
        try:
            existing = self.get_transfer(transfer_id)
            for key, value in copied_data.items():
                if hasattr(existing, key):
                    setattr(existing, key, value)
            existing.last_modified_by = SYSTEM_USER_ID
            return self.repository.update(transfer_id, existing)
        except EntityNotFoundError as e:
            self.raise_not_found(transfer_id, e)

    def archive_transfer(self, transfer_id: UUID, reason) -> StudentDepartmentTransfer:
        try:
            failed_dependencies = self.archive_service.check_active_dependencies_exists(
                entity_model=self.model, target_id=transfer_id
            )
            if failed_dependencies:
                raise ArchiveDependencyError(
                    entity_model=self.entity_model, identifier=transfer_id,
                    display_name=self.display_name, related_entities=", ".join(failed_dependencies)
                )
            return self.repository.archive(transfer_id, SYSTEM_USER_ID, reason)
        except EntityNotFoundError as e:
            self.raise_not_found(transfer_id, e)

    @resolve_fk_on_delete()
    def delete_transfer(self, transfer_id: UUID, is_archived=False):
        try:
            self.delete_service.check_safe_delete(self.model, transfer_id, is_archived)
            return self.repository.delete(transfer_id)
        except EntityNotFoundError as e:
            self.raise_not_found(transfer_id, e)

    def get_all_archived_transfers(self, filters) -> List[StudentDepartmentTransfer]:
        return self.repository.execute_archive_query(['academic_session', 'status'], filters)

    def get_archived_transfer(self, transfer_id: UUID) -> StudentDepartmentTransfer:
        try:
            return self.repository.get_archive_by_id(transfer_id)
        except EntityNotFoundError as e:
            self.raise_not_found(transfer_id, e)

    def restore_transfer(self, transfer_id: UUID) -> StudentDepartmentTransfer:
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
