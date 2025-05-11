from sqlalchemy.orm import Session
from sqlalchemy import select, func
from V2.app.core.assessment.models.assessment import Grade

class GradeCalculator:
    def __init__(self, session: Session):
        self.session = session


    def calculate_total_grade(self, student_subject_id, academic_session, term):
        total_weight_stmt  = select(func.sum(Grade.weight).where(
            Grade.student_subject_id == student_subject_id,
            Grade.academic_session == academic_session,
            Grade.term == term,
        ))
        total_weight = self.session.scalar(total_weight_stmt )

        weighted_score_stmt = select(func.sum(
            (Grade.score/Grade.max_score)*Grade.weight
            )).where(
                Grade.student_subject_id == student_subject_id,
                Grade.academic_session == academic_session,
                Grade.term == term,
    )
        weighted_score = self.session.scalar(weighted_score_stmt)

        total_grade = (weighted_score / total_weight) * 100
        return round(total_grade, 2)
