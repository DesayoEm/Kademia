from datetime import datetime

from sqlalchemy.orm import Session
from uuid import UUID

from app.core.shared.exceptions import TransferStatusAlreadySetError, EmptyFieldError, DepartmentNotSetError
from app.core.transfer.factories.transfer import TransferFactory
from app.core.transfer.models.transfer import DepartmentTransfer
from app.core.shared.services.audit_export_service.export import ExportService


class TransferService:
    def __init__(self, session: Session, current_user):
        self.session = session
        self.current_user = current_user
        self.factory = TransferFactory(self.session, DepartmentTransfer, self.current_user)
        self.export_service = ExportService(session)
        self.domain = "TRANSFER"


    def check_student_has_department(self, student_id: UUID):
        """Check if a student is assigned to a department before attempting transfer."""
        from app.core.identity.factories.student import StudentFactory
        from app.core.identity.models.student import Student

        student_factory = StudentFactory(self.session, Student, self.current_user)
        student = student_factory.get_student(student_id)

        if not student.department_id:
            raise DepartmentNotSetError(student_id)
        return student.department_id


    def action_transfer_record(self, transfer_id: UUID, data: dict):
        """
        Approve or reject a student transfer request.

        Args:
           transfer_id: ID of transfer to process
           data: Decision payload with status and optional decision_reason
        """

        from app.core.identity.factories.student import StudentFactory
        from app.core.identity.models.student import Student

        student_factory = StudentFactory(self.session, Student, self.current_user)
        transfer = self.factory.get_transfer(transfer_id)

        if transfer.status == "REJECTED" and data["status"].value == "REJECTED":
            raise TransferStatusAlreadySetError(
                transfer.status, data["status"].value, transfer_id
            )

        if transfer.status == "APPROVED" and data["status"].value == "APPROVED":
            raise TransferStatusAlreadySetError(
                transfer.status, data["status"].value, transfer_id
            )

        # if rejected, state reason for rejection
        if data["status"].value == "REJECTED":
            if not data["decision_reason"]:  # if rejected, state reason for rejection
                raise EmptyFieldError(entry=data["decision_reason"])

            return self.factory.update_transfer(
                transfer_id,
                {"status": data["status"].value,
                 "decision_reason": data["decision_reason"],
                 "status_completed_by": self.current_user.id,
                 "status_completed_at": datetime.now()}
            )

        # if approved, persist student's new department, and transfer record
        if data["status"].value == "APPROVED":
            student_factory.update_student(
                transfer.student_id, {"department_id": transfer.new_department_id}
            )

            return self.factory.update_transfer(
                transfer_id,
                {"status": data["status"].value,
                 "decision_reason": data["decision_reason"],
                 "status_completed_by": self.current_user.id,
                 "status_completed_at": datetime.now()}
            )
        
        

    def export_transfer_audit(self, transfer_id: UUID, export_format: str) -> str:
        """Export transfer object and its associated data
        Args:
            transfer_id: transfer UUID
            export_format: Preferred export format
        """
        return self.export_service.export_entity(
            TransferFactory, transfer_id, export_format
        )