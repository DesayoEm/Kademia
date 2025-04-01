from sqlalchemy.orm import Session
from ...validators.staff_organization import StaffOrganizationValidator


class QualificationsService:
    def __init__(self, session: Session):
        self.validator = StaffOrganizationValidator()


    def create_valid_until(self, validity_type: str, value:str) -> str:
        """Create a valid until date depending on input"""
        if validity_type.lower() == 'lifetime':
            return 'Lifetime'
        return self.validator.validate_valid_until_year(value)
