from app.core.shared.schemas.common_imports import *
from app.core.shared.schemas.enums import ApprovalStatus
from app.core.shared.schemas.shared_models import *


class DepartmentTransferFilterParams(BaseFilterParams):
    academic_session: str | None = None
    status: str | None = None
    order_by: Literal["academic_session", "created_at"] = "academic_session"
    
class StudentDepartmentTransferBase(BaseModel):
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
                "reason": "Specialized track",
                "status": "PENDING",

            }
        }
    )


class StudentDepartmentTransferCreate(StudentDepartmentTransferBase):
    """Used for creating a new department transfer"""
    pass


class StudentDepartmentTransferResponse(StudentDepartmentTransferBase):
    """Response model for student department transfers"""
    status_updated_by: UUID | None = None
    status_updated_at: datetime | None = None
    rejection_reason: str | None = None
    previous_department_id: UUID
