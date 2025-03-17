from typing import List
from uuid import uuid4, UUID
from sqlalchemy.orm import Session
from ...errors.database_errors import RelationshipError
from ....security.utils import SecurityUtils
from ....services.errors.staff_profile_errors import (
    DuplicateStaffError, StaffNotFoundError
)
from ....services.errors.staff_organisation_errors import DepartmentNotFoundError, RoleNotFoundError
from ...errors.staff_profile_errors import *
from ....database.db_repositories.sqlalchemy_repos.main_repo import SQLAlchemyRepository
from ....database.models.data_enums import ArchiveReason
from ....services.profiles.validators import ProfileValidators
from .service import StaffFactoryService
from ....database.models.profiles import Staff



SYSTEM_USER_ID = UUID('00000000-0000-0000-0000-000000000000')


class StaffFactory:
    """Factory class for managing staff operations."""

    def __init__(self, session: Session):
        self.repository = SQLAlchemyRepository(Staff, session)
        self.validator = ProfileValidators()
        self.service =StaffFactoryService()
        self.secure = SecurityUtils()

    def create_staff(self, staff_data) -> Staff:
        """Create a new staff.
        Args:
            staff_data: staff data
        Returns:
            Staff: Created staff record
        """
        password = self.service.generate_random_password(10)
        new_staff = Staff(
            id = uuid4(),
            first_name = self.validator.validate_name(staff_data.first_name),
            last_name = self.validator.validate_name(staff_data.last_name),
            password_hash = self.secure.hash_password(password),
            gender = staff_data.gender,
            access_level = staff_data.access_level,
            status = staff_data.status,
            availability =  staff_data.availability,
            staff_type = staff_data.staff_type,
            email_address =  self.validator.validate_staff_email(staff_data.email_address),
            address =  self.validator.validate_address(staff_data.address),
            phone =  self.validator.validate_phone(staff_data.phone),
            department_id =  staff_data.department_id,
            role_id = staff_data.role_id,
            date_joined =  self.validator.validate_date(staff_data.date_joined),
            created_by=SYSTEM_USER_ID,
            last_modified_by=SYSTEM_USER_ID,
        )
        try:
            return self.repository.create(new_staff)
        except UniqueViolationError as e:  # Could either be email or phone
            error_message = str(e)
            if "staff_phone_key" in error_message.lower():
                raise DuplicateStaffError(
                    input_value=staff_data.phone, field="phone", detail=error_message)
            elif "staff_email_address_key" in error_message.lower():
                raise DuplicateStaffError(
                    input_value = str(staff_data.email_address), field="email address", detail=error_message)
            else:
                raise DuplicateStaffError(
                    input_value="unknown field", field="unknown", detail=error_message)
        # Could be role or department. Could there be OTHER reasons for a relationship error during creation
        except RelationshipError as e:
            error_message = str(e)
            if "role_id" in error_message.lower():
                raise RoleNotFoundError(id=staff_data.role_id)
            elif "department_id" in error_message.lower():
                raise DepartmentNotFoundError(id=staff_data.department_id)
            else:#edge case
                raise EntityNotFoundError(
                    identifier="unknown field", entity_type="unknown")



