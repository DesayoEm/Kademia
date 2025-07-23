from app.core.shared.schemas.common_imports import *
from app.core.shared.schemas.enums import ApprovalStatus
from app.core.shared.schemas.shared_models import *


class DepartmentTransferFilterParams(BaseFilterParams):
    student_id: UUID | None = None
    previous_department_id: UUID | None = None
    new_department_id: UUID | None = None
    academic_session: str | None = None
    status: str | None = None
    order_by: Literal["academic_session", "created_at"] = "academic_session"
    
class DepartmentTransferBase(BaseModel):
    """Base model for student department transfers"""
    academic_session: str
    new_department_id: UUID
    reason: str


    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra={
            "example": {
                "academic_session": "2025/2026",
                "new_department_id": "00000000-0000-0000-0000-000000000031",
                "reason": "Specialized track"

            }
        }
    )


class DepartmentTransferCreate(DepartmentTransferBase):
    """Used for creating a new department transfer"""
    pass


class DepartmentTransferUpdate(BaseModel):
    """Used for updating a transfer"""
    reason: str

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra={
            "example": {
                "reason": "New request"

            }
        }
    )

class DepartmentTransferDecision(BaseModel):
    """Model for reviewing transfers"""
    status: ApprovalStatus
    decision_reason: str


    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra = {
                "example": {
                    "decision_reason": "Academic performance below promotion criteria",
                    "status": "APPROVED"
                }
            }

   )


class DepartmentTransferResponse(DepartmentTransferBase):
    """Response model for student department transfers"""
    status_completed_by: UUID | None = None
    status_completed_at: datetime | None = None
    decision_reason: str | None = None
    previous_department_id: UUID
    status: str | None = None
