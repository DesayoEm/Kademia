from datetime import date
import re

class ProfileService:
    def __init__(self):
        pass

    def validate_student_id(value: str) -> str:
        """
        Validate that a student's id matches the format `STU/10/11/0000` and the first integer
        group is one less than the second, representing the academic year of student's admission
        """
        pattern = r'^(?i)STU/(\d{2})/(\d{2})/([0-9]{4})$'
        match = re.match(value, pattern)
        if not match:
            raise Exception

        first_num = int(match.group(1))
        second_num = int(match.group(2))

        if second_num != first_num + 1:
            raise Exception
        return value.upper()


    def validate_admission_date(value: date) -> date:
        """Validate that admission date is not in the future."""
        if value > date.today():
            raise ValueError('Admission date cannot be in the future')
        return value

profile_service = ProfileService()