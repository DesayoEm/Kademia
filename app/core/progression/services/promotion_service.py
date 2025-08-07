from datetime import datetime

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select
from uuid import UUID

from app.core.progression.factories.promotion import PromotionFactory
from app.core.progression.models.progression import Repetition, Promotion
from app.core.shared.exceptions import StudentToGraduateError, EmptyFieldError, ProgressionStatusAlreadySetError, \
    LevelNotFinalError, EntityNotFoundError, NoResultError
from app.core.shared.services.audit_export_service.export import ExportService




class PromotionService:
    def __init__(self, session: Session, current_user):
        self.session = session
        self.current_user = current_user
        self.factory = PromotionFactory(self.session, Promotion, self.current_user)
        self.export_service = ExportService(session)
        self.domain = "PROGRESSION"


    def generate_promotion_level(self, previous_level_id: UUID):
    
        from app.core.academic_structure.factories.academic_level import AcademicLevelFactory
        from app.core.academic_structure.models import AcademicLevel
        academic_factory = AcademicLevelFactory(self.session, AcademicLevel, self.current_user)

        previous_level = academic_factory.get_academic_level(previous_level_id)

        if previous_level.is_final:
            raise StudentToGraduateError(previous_level_id)

        stmt = select(AcademicLevel).where(
            AcademicLevel.promotion_rank == previous_level.promotion_rank + 1
        )

        promoted_level = self.session.scalar(stmt)

        if not promoted_level:
            raise NoResultError(
                str(stmt), "greater than the student's current one", "academic level",
            )

        return promoted_level.id



    def graduate_student(self, student_id: UUID, academic_session: str):
        from app.core.identity.models.student import Student
        from app.core.shared.exceptions import LevelNotFinalError

        student = (
            self.session.query(Student)
            .options(joinedload(Student.level))
            .filter(Student.id == student_id)
            .one_or_none()
        )

        if not student:
            raise EntityNotFoundError(
            entity_model=Student,
            identifier=student_id,
            error="Student not found",
            display_name="student"
        )

        if not student.level.is_final:
            raise LevelNotFinalError(student.level.id)

        student.graduation_year = academic_session
        student.is_graduated = True

        self.session.commit()
        return student



    def action_promotion_record(self, promotion_id: UUID, data: dict):
        """
        Approve or reject a student promotion request.

        Args:
           promotion_id: ID of promotion to process
           data: Decision payload with status and optional decision_reason

        Raises:
           RepetitionStatusAlreadySetError: If status already set
           EmptyFieldError: If rejection missing decision_reason
        """

        from app.core.identity.factories.student import StudentFactory
        from app.core.identity.models.student import Student

        student_factory = StudentFactory(self.session, Student, self.current_user)
        promotion = self.factory.get_promotion(promotion_id)

        if promotion.status == "REJECTED" and data["status"].value == "REJECTED":
            raise ProgressionStatusAlreadySetError(
                "promotion", promotion.status, data["status"].value, promotion_id
            )

        if promotion.status == "APPROVED" and data["status"].value == "APPROVED":
            raise ProgressionStatusAlreadySetError(
                "promotion", promotion.status, data["status"].value, promotion_id
            )

        #if rejected, state reason for rejection
        if data["status"].value == "REJECTED":
            if not data["decision_reason"]: #if rejected, state reason for rejection
                raise EmptyFieldError(entry = data["decision_reason"])

            #persist student's promotion record
            student_factory.update_student(
             promotion.student_id, {"level_id": promotion.previous_level_id}
            )

            return self.factory.update_promotion(
                promotion_id,
                {"status": data["status"].value,
                 "decision_reason": data["decision_reason"],
                 "status_completed_by": self.current_user.id,
                 "status_completed_at": datetime.now()}
            )

        #if approved, persist student's new academic level, and promotion record
        if data["status"].value == "APPROVED":

            student_factory.update_student(
                promotion.student_id, {"level_id":promotion.promoted_level_id}
            )

            return self.factory.update_promotion(
                promotion_id,
                {"status":data["status"].value,
                 "decision_reason": data["decision_reason"],
                 "status_completed_by":self.current_user.id ,
                 "status_completed_at":datetime.now()}
            )



    def export_promotion_audit(self, promotion_id: UUID, export_format: str) -> str:
        """Export promotion object and its associated data
        Args:
            promotion_id: Promotion UUID
            export_format: Preferred export format
        """
        return self.export_service.export_entity(
            Repetition, promotion_id, export_format
        )