from ...database.models.data_enums import ArchiveReason
from ...schemas.staff_organization.staff_departments import (
    StaffDepartmentCreate, StaffDepartmentUpdate, StaffDepartmentResponse
)
from ...database.models.staff_organization import StaffDepartments
from sqlalchemy.orm import Session
from ...services.staff_organization.staff_departments import staff_department_factory

class StaffDepartmentCrud:
    pass
