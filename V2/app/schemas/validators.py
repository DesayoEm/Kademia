from datetime import date
import re

def validate_name(value: str) -> str:
    """Validate that a name is at least 2 characters long and return a formatted name."""
    if len(value.strip()) < 2:
        raise ValueError('Name must be greater than two characters')
    if value.isspace():
        raise ValueError("Name cannot be whitespace")
    if  any(char.isdigit() for char in value):
        raise ValueError("Name cannot contain a digit")
    return value.title().strip()


def validate_phone(value: str) -> str:
    """Validate that a phone number contains exactly 11 digits and is numeric."""
    phone_pattern = re.compile(r"^\+?(\d{1,3})?(\d{10,15})$")
    if not phone_pattern.match(value):
        raise ValueError("Invalid phone number format")
    if len(value) < 10 or len(value) > 15:
        raise ValueError("Phone number must be between 10 and 15 digits.")

    return value


def validate_admission_date(value: date) -> date:
    """Validate that admission date is not in the future."""
    if value > date.today():
        raise ValueError('Admission date cannot be in the future')
    return value