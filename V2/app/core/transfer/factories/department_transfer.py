
from typing import List
from uuid import UUID, uuid4
from sqlalchemy.orm import Session

from V2.app.core.shared.factory.base_factory import BaseFactory
from V2.app.core.shared.services.lifecycle_service.archive_service import ArchiveService
from V2.app.core.shared.services.lifecycle_service.delete_service import DeleteService
from V2.app.infra.db.repositories.sqlalchemy_repos.base_repo import SQLAlchemyRepository
from V2.app.core.shared.exceptions.decorators.resolve_fk_violation import resolve_fk_on_create, resolve_fk_on_delete
from V2.app.core.shared.exceptions import EntityNotFoundError, ArchiveDependencyError
from V2.app.core.shared.exceptions.maps.error_map import error_map
from V2.app.core.transfer.models.transfer import DepartmentTransfer



class DepartmentTransferFactory(BaseFactory):
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
        self.repository = SQLAlchemyRepository(self.model, session)
        self.delete_service = DeleteService(self.model, session)
        self.archive_service = ArchiveService(session)
        self.error_details = error_map.get(self.model)
        self.entity_model, self.display_name = self.error_details
        self.actor_id: UUID = self.get_actor_id()
        self.domain = "StudentDepartmentTransfer"

    def raise_not_found(self, identifier, error):
        raise EntityNotFoundError(
            entity_model=self.entity_model,
            identifier=identifier,
            error=str(error),
            display_name=self.display_name
        )

    @resolve_fk_on_create()
    def create_transfer(self, student_id: UUID, data) -> DepartmentTransfer:
        new_transfer = DepartmentTransfer(
            id=uuid4(),
            student_id=student_id,
            academic_session=data.academic_session,
            previous_department_id=data.previous_department_id,
            new_department_id=data.new_department_id,
            reason=data.reason,
            status=data.status,
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
        return self.repository.execute_query(['academic_session', 'status'], filters)


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
        return self.repository.execute_archive_query(['academic_session', 'status'], filters)


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
