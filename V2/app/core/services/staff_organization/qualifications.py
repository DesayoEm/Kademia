from sqlalchemy.orm import Session

from ...errors.input_validation_errors import DateFormatError
from ...errors.staff_organisation_errors import LifetimeValidityConflictError
from ...validators.staff_organization import StaffOrganizationValidator
from datetime import date


class QualificationsService:
    def __init__(self, session: Session):
        self.validator = StaffOrganizationValidator()
        self.domain = "EDUCATOR QUALIFICATIONS"


    def create_valid_until(self, validity_type: str, value:date) -> date | str:
        """Create a valid until date depending on input"""
        if validity_type.lower() == 'lifetime':
            if isinstance(value, date):
                raise LifetimeValidityConflictError(entry=value)
            return 'Lifetime'

        if validity_type.lower() == 'temporary':
            if isinstance(value, str):
                raise DateFormatError(entry=value, domain = self.domain)

            if isinstance(value, date):
                return self.validator.validate_valid_until_date(value)
