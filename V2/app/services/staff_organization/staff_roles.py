from uuid import uuid4, UUID
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from .validators import staff_organisation_validators
from ..base_crud import CrudService
from ...database.models.staff_organization import StaffRoles
from ...database.models.data_enums import ArchiveReason
from V2.app.services.errors.staff_organisation_errors import RoleNotFoundError, DuplicateRoleError
from ...schemas.staff_organization.staff_roles import (
    StaffRoleCreate,
    StaffRoleResponse,
    StaffRoleUpdate
)

SYSTEM_USER_ID = UUID('00000000-0000-0000-0000-000000000000')

class StaffRolesService(CrudService):
    """Service class for managing staff role operations."""

    def __init__(self, db: Session):
        super().__init__(db, StaffRoles)
        self.validator = staff_organisation_validators

    def create_staff_role(self, new_role: StaffRoleCreate) -> StaffRoleResponse:
        """Create a new staff role."""
        role = StaffRoles(
            id=uuid4(),
            created_by=SYSTEM_USER_ID,
            last_modified_by=SYSTEM_USER_ID,
            name=self.validator.validate_name(new_role.name),
            description=self.validator.validate_name(new_role.description)
        )

        try:
            self.db.add(role)
            self.db.commit()
            return StaffRoleResponse.model_validate(role)
        except IntegrityError:
            self.db.rollback()
            raise DuplicateRoleError(role.name)


    def get_staff_roles(self) -> list[StaffRoleResponse]:
        """Get all active staff roles."""
        roles = (self.base_query()
                       .order_by(StaffRoles.name).all())
        return [StaffRoleResponse.model_validate(role)
                for role in roles]


    def get_staff_role(self, role_id: UUID) -> StaffRoleResponse:
        """Get a specific staff role by ID."""
        role = (self.base_query()
                      .filter(StaffRoles.id == role_id)
                      .first())
        if not role:
            raise RoleNotFoundError
        return StaffRoleResponse.model_validate(role)


    def update_staff_role(self, role_id: UUID,
                                data: StaffRoleUpdate) -> StaffRoleResponse:
        """Update a staff role's information."""
        data_update = data.model_dump(exclude_unset=True)
        if 'name' in data_update:
            data.name = self.validator.validate_name(data.name)
        if 'description' in data_update:
            data.description = self.validator.validate_name(data.description)

        role = self.get_staff_role(role_id)
        try:
            for key, value in data_update.items():
                setattr(role, key, value)
            role.last_modified_by = SYSTEM_USER_ID #placeholder

            self.db.commit()
            self.db.refresh(role)
            return StaffRoleResponse.model_validate(role)
        except IntegrityError:
            self.db.rollback()
            raise DuplicateRoleError(data.get('name'))


    def archive_role(self, role_id: UUID,
                           reason: ArchiveReason) -> StaffRoleResponse:
        """Archive a staff role."""
        role = self.get_staff_role(role_id)
        #use system id as placeholder until authentication is implemented
        role.archive(SYSTEM_USER_ID, reason)

        self.db.commit()
        self.db.refresh(role)
        return StaffRoleResponse.model_validate(role)

    def delete_role(self, role_id: UUID) -> None:
        """Permanently delete a staff role."""
        role = self.get_staff_role(role_id)
        self.db.delete(role)
        self.db.commit()