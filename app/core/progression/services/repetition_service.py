from datetime import datetime

from sqlalchemy.orm import Session
from uuid import UUID
from app.core.academic_structure.factories.academic_level import AcademicLevelFactory
from app.core.academic_structure.models import AcademicLevel
from app.core.progression.factories.repetition import RepetitionFactory
from app.core.progression.models.progression import Repetition
from app.core.shared.exceptions import InvalidRepetitionLevelError, EmptyFieldError, \
    ProgressionStatusAlreadySetError
from app.core.shared.services.audit_export_service.export import ExportService



class RepetitionService:
    def __init__(self, session: Session, current_user):
        self.session= session
        self.current_user = current_user
        self.export_service = ExportService(session)
        self.factory = RepetitionFactory(session, Repetition, self.current_user)
        self.domain = "REPETITION"

    def validate_repetition_level(self, failed_level_id: UUID, repeat_level_id: UUID):
        """
            Validate that repeat level is at or below the failed level.
            Args:
                failed_level_id: Academic level the student failed
                repeat_level_id: Proposed repetition level
            Returns:
                UUID: Validated repeat_level_id
            Raises:
                InvalidRepetitionLevelError: If repeat level ranks higher than failed level
            """

        academic_factory = AcademicLevelFactory(self.session, AcademicLevel, self.current_user)
        failed_level = academic_factory.get_academic_level(failed_level_id)
        repeat_level = academic_factory.get_academic_level(repeat_level_id)

        if not repeat_level.promotion_rank <= failed_level.promotion_rank:
            raise InvalidRepetitionLevelError(
                repeat_level_id=repeat_level_id, failed_level_id=failed_level_id
            )

        return repeat_level_id


    def action_repetition_record(self, repetition_id: UUID, data: dict):
        """
        Approve or reject a student repetition request.

        Args:
           repetition_id: ID of repetition to process
           data: Decision payload with status and optional decision_reason

        Raises:
           RepetitionStatusAlreadySetError: If status already set
           EmptyFieldError: If rejection missing decision_reason
        """

        from app.core.identity.factories.student import StudentFactory
        from app.core.identity.models.student import Student

        student_factory = StudentFactory(self.session, Student, self.current_user)
        repetition = self.factory.get_repetition(repetition_id)

        if repetition.status == "REJECTED" and data["status"].value == "REJECTED":
            raise ProgressionStatusAlreadySetError(
                "repetition", repetition.status, data["status"].value, repetition_id
            )

        if repetition.status == "APPROVED" and data["status"].value == "APPROVED":
            raise ProgressionStatusAlreadySetError(
                "repetition", repetition.status, data["status"].value, repetition_id
            )

        #if rejected, state reason for rejection
        if data["status"].value == "REJECTED":
            if not data["decision_reason"]: #if rejected, state reason for rejection
                raise EmptyFieldError(entry = data["decision_reason"])

            #persist student's repetition record

            student_factory.update_student(
                repetition.student_id, {"level_id": repetition.failed_level_id}
            )

            return self.factory.update_repetition(
                repetition_id,
                {"status": data["status"].value,
                 "decision_reason": data["decision_reason"],
                 "status_completed_by": self.current_user.id,
                 "status_completed_at": datetime.now()}
            )

        #if approved, persist student's new academic level, and repetition record
        if data["status"].value == "APPROVED":

            student_factory.update_student(
                repetition.student_id, {"level_id":repetition.repeat_level_id}
            )

            return self.factory.update_repetition(
                repetition_id,
                {"status":data["status"].value,
                 "decision_reason": data["decision_reason"],
                 "status_completed_by":self.current_user.id ,
                 "status_completed_at":datetime.now()}
            )




    def export_repetition_audit(self, repetition_id: UUID, export_format: str) -> str:
        """Export repetition object and its associated data
        Args:
            repetition_id: Repetition UUID
            export_format: Preferred export format
        """
        return self.export_service.export_entity(
            Repetition, repetition_id, export_format
        )