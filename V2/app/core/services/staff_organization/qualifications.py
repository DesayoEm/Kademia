from sqlalchemy.orm import Session

from ...errors.entry_validation_errors import DateFormatError
from ...errors.staff_organisation_errors import LifetimeValidityConflictError, TemporaryValidityConflictError
from ...validators.staff_organization import StaffOrganizationValidator
from datetime import date
from dateutil.parser import parse


class QualificationsService:
    def __init__(self, session: Session):
        self.validator = StaffOrganizationValidator()
        self.domain = "EDUCATOR QUALIFICATION"


    def parse_validity_date(self, value: str) -> date:
        """convert date string to a date object"""
        try:
            return parse(value).date()

        except ValueError:
                raise TemporaryValidityConflictError(entry = value, domain = self.domain)


    def validate_valid_until(self, validity_type: str, value:str) -> str:
        """Create a valid until date depending on input"""

        if validity_type.lower() == 'lifetime':
            if value.lower().strip() != 'lifetime':
                raise LifetimeValidityConflictError(entry = value)
            return value.title()


        elif validity_type.lower() == 'temporary':
            converted_str = self.parse_validity_date(value)
            return str(self.validator.validate_valid_until_date(converted_str))
