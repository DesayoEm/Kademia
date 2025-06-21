from datetime import datetime

from sqlalchemy.orm import Session
from uuid import UUID

from V2.app.core.progression.factories.promotion import PromotionFactory
from V2.app.core.progression.models.progression import Repetition, Promotion
from V2.app.core.shared.exceptions import InvalidPromotionLevelError, EmptyFieldError, ProgressionStatusAlreadySetError
from V2.app.core.shared.services.export_service.export import ExportService




class PromotionService:
    def __init__(self, session: Session, current_user):
        self.session = session
        self.current_user = current_user
        self.factory = PromotionFactory(self.session, Promotion, self.current_user)
        self.export_service = ExportService(session)
        self.domain = "PROGRESSION"


    def validate_promotion_level(self, previous_level_id: UUID, promoted_level_id: UUID):
    
        from V2.app.core.academic_structure.factories.academic_level import AcademicLevelFactory
        from V2.app.core.academic_structure.models import AcademicLevel
       
        academic_factory = AcademicLevelFactory(self.session, AcademicLevel, self.current_user)
        
        previous_level = academic_factory.get_academic_level(previous_level_id)
        promoted_level = academic_factory.get_academic_level(promoted_level_id)
        
        if promoted_level.promotion_rank != previous_level.promotion_rank + 1:
            raise InvalidPromotionLevelError(
                next_level_id=promoted_level_id,
                previous_level_id=previous_level_id
            )

        return promoted_level_id


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

        from V2.app.core.identity.factories.student import StudentFactory
        from V2.app.core.identity.models.student import Student

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