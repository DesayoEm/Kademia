from uuid import uuid4, UUID
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from .validators import staff_organisation_validators
from ..base_crud import CrudService
from ...database.models.staff_organization import StaffDepartments
from ...database.models.data_enums import ArchiveReason
from V2.app.services.errors.staff_organisation_errors import DepartmentNotFoundError, DuplicateDepartmentError
from ...schemas.staff_organization.staff_departments import (
    StaffDepartmentCreate,
    StaffDepartmentResponse,
    StaffDepartmentUpdate
)

SYSTEM_USER_ID = UUID('00000000-0000-0000-0000-000000000000')

class StaffDepartmentsService(CrudService):
    """Service class for managing staff department operations."""

    def __init__(self, db: Session):
        super().__init__(db, StaffDepartments)
        self.validator = staff_organisation_validators

    def create_staff_department(self, new_department: StaffDepartmentCreate) -> StaffDepartmentResponse:
        """Create a new staff department."""
        department = StaffDepartments(
            id=uuid4(),
            created_by=SYSTEM_USER_ID,
            last_modified_by=SYSTEM_USER_ID,
            name=self.validator.validate_name(new_department.name),
            description=self.validator.validate_name(new_department.description)
        )

        try:
            self.db.add(department)
            self.db.commit()
            return StaffDepartmentResponse.model_validate(department)
        except IntegrityError:
            self.db.rollback()
            raise DuplicateDepartmentError(department.name)


    def get_staff_departments(self) -> list[StaffDepartmentResponse]:
        """Get all active staff departments."""
        departments = (self.base_query()
                       .order_by(StaffDepartments.name).all())
        return [StaffDepartmentResponse.model_validate(department)
                for department in departments]


    def get_staff_department(self, department_id: UUID) -> StaffDepartmentResponse:
        """Get a specific staff department by ID."""
        department = (self.base_query()
                      .filter(StaffDepartments.id == department_id)
                      .first())
        if not department:
            raise DepartmentNotFoundError
        return StaffDepartmentResponse.model_validate(department)


    def update_staff_department(self, department_id: UUID,
                                data: StaffDepartmentUpdate) -> StaffDepartmentResponse:
        """Update a staff department's information."""
        data_update = data.model_dump(exclude_unset=True)
        if 'name' in data_update:
            data.name = self.validator.validate_name(data.name)
        if 'description' in data_update:
            data.description = self.validator.validate_name(data.description)

        department = self.get_staff_department(department_id)
        try:
            for key, value in data_update.items():
                setattr(department, key, value)
            department.last_modified_by = SYSTEM_USER_ID #placeholder

            self.db.commit()
            self.db.refresh(department)
            return StaffDepartmentResponse.model_validate(department)
        except IntegrityError:
            self.db.rollback()
            raise DuplicateDepartmentError(data.get('name'))


    def archive_department(self, department_id: UUID,
                           reason: ArchiveReason) -> StaffDepartmentResponse:
        """Archive a staff department."""
        department = self.get_staff_department(department_id)
        #use system id as placeholder until authentication is implemented
        department.archive(SYSTEM_USER_ID, reason)

        self.db.commit()
        self.db.refresh(department)
        return StaffDepartmentResponse.model_validate(department)


    def delete_department(self, department_id: UUID) -> None:
        """Permanently delete a staff department."""
        department = self.get_staff_department(department_id)
        self.db.delete(department)
        self.db.commit()