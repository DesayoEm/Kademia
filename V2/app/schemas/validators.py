from datetime import date

def validate_name(value: str) -> str:
    """Validate that a name is at least 2 characters long and return a formatted name."""
    if len(value.strip()) < 2:
        raise ValueError('Name must be greater than two characters')
    return value.title().strip()


def validate_phone(value: str) -> str:
    """Validate that a phone number contains exactly 11 digits and is numeric."""
    if len(value.strip()) != 11:
        raise ValueError('Phone number must be exactly 11 digits')
    if any(not char.isnumeric() for char in value):
        raise ValueError('Phone number can only contain digits')
    return value.strip()


def validate_admission_date(value: date) -> date:
    """Validate that admission date is not in the future."""
    if value > date.today():
        raise ValueError('Admission date cannot be in the future')
    return value