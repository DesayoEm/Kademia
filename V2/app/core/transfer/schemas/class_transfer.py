from V2.app.core.shared.schemas.common_imports import *
from V2.app.core.shared.schemas.enums import ApprovalStatus
from V2.app.core.shared.schemas.shared_models import *


class ClassTransferFilterParams(BaseFilterParams):
    academic_session: str | None = None
    status: str | None = None
    order_by: Literal["academic_session", "created_at"] = "academic_session"

class StudentClassTransferBase(BaseModel):
    """Base model for student class transfers"""
    academic_session: str
    new_class_id: UUID
    reason: str
    status: ApprovalStatus = ApprovalStatus.PENDING
    status_updated_by: UUID | None = None
    status_updated_at: datetime | None = None
    rejection_reason: str | None = None

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra = {
        "example": {
            "academic_session": "2025/2026",
            "new_class_id": "00000000-0000-0000-0000-000000000002",
            "reason": "Better fit for student's academic needs",
            "status": "PENDING",
            "status_updated_by": None,
            "status_updated_at": None,
            "rejection_reason": None
        }
    }
    )


class StudentClassTransferUpdate(StudentClassTransferBase):
    """Used for updating student class transfers"""
    pass


class StudentClassTransferCreate(StudentClassTransferBase):
    """Used for creating new student class transfers"""
    pass


class StudentClassTransferResponse(StudentClassTransferBase):
    """Response model for student class transfers"""
    previous_class_id: UUID

