from sqlalchemy.orm import Session


class GradeCalculator:
    def __init__(self, session: Session):
        self.session = session


    def calculate_total_grade(self, student_id, subject_id, academic_session, term):
        pass
