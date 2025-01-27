from datetime import date

class StudentService:
    def __init__(self):
        pass

    def validate_admission_date(value: date) -> date:
        """Validate that admission date is not in the future."""
        if value > date.today():
            raise ValueError('Admission date cannot be in the future')
        return value

student_service = StudentService()