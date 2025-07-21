from uuid import UUID
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, func

from app.core.curriculum.models.curriculum import StudentSubject, AcademicLevelSubject, Subject
from app.core.shared.schemas.enums import Term
from app.core.assessment.factories.total_grade import TotalGradeFactory
from app.core.assessment.services.validators import AssessmentValidator
from app.core.assessment.factories.grade import GradeFactory
from app.core.assessment.models.assessment import TotalGrade
from app.core.identity.factories.student import StudentFactory
from app.core.identity.models.student import Student
from app.core.shared.services.audit_export_service.export import ExportService
from app.core.shared.exceptions.assessment_errors import WeightTooHighError, UnableToRecalculateError
from app.core.shared.exceptions import InvalidWeightError
from app.core.assessment.models.assessment import Grade
from app.core.shared.services.pdf_service.templates.results import ResultPDF
from app.infra.db.repositories.sqlalchemy_repos.base_repo import SQLAlchemyRepository


class AssessmentService:
    def __init__(self, session: Session, current_user=None):
        self.session = session
        self.current_user = current_user
        self.export_service = ExportService(session)
        self.validator = AssessmentValidator(session)
        self.grade_factory = GradeFactory(session , Grade, self.current_user)
        self.student_factory = StudentFactory(session, Student, self.current_user)
        self.total_grade_factory = TotalGradeFactory(session, TotalGrade, self.current_user)
        self.total_grade_repository = SQLAlchemyRepository(TotalGrade, session)
        self.pdf_service = ResultPDF()


    def validate_grade_weight(self, value: int, student_subject_id: UUID) -> int:

        """Ensure cumulative weight for a term doesn't exceed 10."""
        if value > 10:
            raise WeightTooHighError(entry=value)

        stmt = select(func.coalesce(func.sum(Grade.weight), 0)).where(
            Grade.student_subject_id == student_subject_id
        )
        cumulative = self.session.scalar(stmt)

        if value + cumulative > 10:
            raise InvalidWeightError(
                entry=value, cumulative_weight=cumulative
            )
        return value


    def validate_grade_weight_on_update(self, current_value: int, new_value: int, student_subject_id: UUID) -> int:

        """Ensure cumulative weight for a term doesn't exceed 10 on update."""
        if new_value > 10:
            raise WeightTooHighError(entry=new_value)

        stmt = select(func.coalesce(func.sum(Grade.weight), 0)).where(
            Grade.student_subject_id == student_subject_id
        )
        cumulative = self.session.scalar(stmt)


        if new_value + cumulative - current_value > 10:
            raise InvalidWeightError(
                entry=new_value, cumulative_weight=cumulative
            )
        return new_value


    def calculate_total_grade(self, student_subject_id):
        """Calculate total grade from all the grades for a student subject"""
        from sqlalchemy import cast, Float

        total_weight_stmt = select(func.sum(Grade.weight)).where(
            Grade.student_subject_id == student_subject_id,
        )
        total_weight = self.session.scalar(total_weight_stmt)

        weighted_score_stmt = select(
            func.sum(
                (cast(Grade.score, Float) / cast(Grade.max_score, Float)) * Grade.weight
            )
        ).where(
            Grade.student_subject_id == student_subject_id,
        )
        weighted_score = self.session.scalar(weighted_score_stmt)

        if not total_weight or total_weight == 0:
            return 0.0

        total_grade = (weighted_score / total_weight) * 100
        return round(total_grade, 2)


    def handle_grade_update(self, grade_id: UUID, update_data: dict):
        """
           Handle the update of an individual grade record. If the grade has a weight (existing or updated) and a total grade record exists,
            recalculate the total grade for the student subject. Finally, persist all validated and updated data to the database.
        """
        existing_grade = self.grade_factory.get_grade(grade_id)

        if "graded_on" in update_data:
            updated_graded_on = self.validator.validate_graded_date(update_data["graded_on"])
            update_data["graded_on"] = updated_graded_on

        if "weight" in update_data:
            current_weight = existing_grade.weight
            validated_weight = self.validate_grade_weight_on_update(
                current_weight,
                update_data["weight"],
                existing_grade.student_subject_id
            )
            update_data["weight"] = validated_weight

        if "score" in update_data:
            max_score = (
                self.validator.validate_max_score(update_data["max_score"])
                if "max_score" in update_data
                else existing_grade.max_score
            )
            validated_score = self.validator.validate_score(max_score, update_data["score"])
            update_data["score"] = validated_score

        #If the grade has or will have a weight > 0, recalculate total grade
        if (existing_grade.weight or "weight" in update_data) and self.check_if_total_exists(existing_grade):

            updated = self.grade_factory.update_grade(grade_id, update_data)
            try:
                existing_total_grade = self.total_grade_repository.get_by_id(
                existing_grade.student_subject.total_grade.id
                )
                total_grade_id = existing_total_grade.id
                new_total = self.calculate_total_grade(existing_grade.student_subject_id)
                self.total_grade_factory.update_total_grade(total_grade_id, {"total_score": new_total})
                return updated

            except Exception as e:
                failed = str(total_grade_id) if total_grade_id else "Unknown"
                raise UnableToRecalculateError(failed, str(e))

        return self.grade_factory.update_grade(grade_id, update_data)



    @staticmethod
    def check_if_total_exists(grade: Grade) -> bool:
        """Check if a total grade has been calculated from a grade"""
        return True if grade.student_subject.total_grade else False


    def recalculate_total_grade(self, total_grade_id: UUID):
        grade = self.total_grade_factory.get_total_grade(total_grade_id)
        self.calculate_total_grade(grade.student_subject_id)

        return self.total_grade_factory.get_total_grade(total_grade_id)


    def generate_student_results(self, student_id: UUID, academic_session: str, term: Term):
        student = self.student_factory.get_student(student_id)
        student_name = f"{student.first_name} {student.last_name}"

        results = self.session.query(StudentSubject).options(
            joinedload(StudentSubject.subject),
            joinedload(StudentSubject.total_grade),
        ).filter(
            StudentSubject.student_id == student_id,
            StudentSubject.academic_session == academic_session,
            StudentSubject.term == term
        ).all()

        result_list = []

        for result in results:
            subject = result.subject
            total_score = result.total_grade.total_score if result.total_grade else None

            result_list.append({
                "course_code": subject.code,
                "course_title": subject.name,
                "total_score": total_score,
                "grading": self.generate_grading(total_score) if total_score is not None else None
            })

        return {
            "student_name": student_name,
            "term": term.value,
            "academic_session": academic_session,
            "result_list": result_list
        }



    def generate_assessment_pdf(self, student_id: UUID, academic_session: str, term: Term):
        student = self.student_factory.get_student(student_id)
        student_name = f"{student.first_name} {student.last_name}"
        file_name = f"{student_name} {academic_session} {term} term results"

        data = self.generate_student_results(student_id, academic_session, term)

        return self.pdf_service.render_pdf(data, file_name)

    @staticmethod
    def generate_grading(self, score: int) -> str:
        if score >= 70:
            return "A"
        elif score >= 60:
            return "B"
        elif score >= 50:
            return "C"
        elif score >= 45:
            return "D"
        elif score >= 40:
            return "E"
        else:
            return "F"

    def export_grade_audit(self, grade_id: UUID, export_format: str) -> str:
        """Export grade and its associated data
        Args:
            grade_id: grade UUID
            export_format: Preferred export format
        """
        return self.export_service.export_entity(
            Grade, grade_id, export_format
        )


    def export_total_grade_audit(self, total_grade_id: UUID, export_format: str) -> str:
        """Export total grade and its associated data
        Args:
            total_grade_id: grade UUID
            export_format: Preferred export format
        """
        return self.export_service.export_entity(
            TotalGrade, total_grade_id, export_format
        )