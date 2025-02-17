from ..common_imports import *
from ..enums import ApprovalStatus, ArchiveReason


class StudentClassTransferBase(BaseModel):
    """Base model for student class transfers"""
    student_id: UUID
    academic_year: int
    previous_class_id: UUID
    new_class_id: UUID
    reason: str
    status: ApprovalStatus = ApprovalStatus.PENDING
    status_updated_by: UUID | None = None
    status_updated_at: datetime | None = None
    rejection_reason: str | None = None

    class Config:
        from_attributes = True

    json_schema_extra = {
        "example": {
            "student_id": "00000000-0000-0000-0000-000000000000",
            "academic_year": 2024,
            "previous_class_id": "00000000-0000-0000-0000-000000000001",
            "new_class_id": "00000000-0000-0000-0000-000000000002",
            "reason": "Better fit for student's academic needs",
            "status": "PENDING",
            "status_updated_by": None,
            "status_updated_at": None,
            "rejection_reason": None
        }
    }


class StudentClassTransferUpdate(StudentClassTransferBase):
    """Used for updating student class transfers"""
    pass


class StudentClassTransferCreate(StudentClassTransferBase):
    """Used for creating new student class transfers"""
    pass


class StudentClassTransferResponse(StudentClassTransferBase):
    """Response model for student class transfers"""
    pass


class StudentClassTransferInDB(StudentClassTransferBase):
    """Represents stored student class transfers"""
    id: UUID
    created_at: datetime
    created_by: UUID
    last_modified_at: datetime
    last_modified_by: UUID
    is_archived: bool
    archived_at: datetime | None = None
    archived_by: UUID | None = None
    archive_reason: ArchiveReason | None = None

    json_schema_extra = {
        "example": {
            "id": "00000000-0000-0000-0000-000000000000",
            "student_id": "00000000-0000-0000-0000-000000000000",
            "academic_year": 2024,
            "previous_class_id": "00000000-0000-0000-0000-000000000001",
            "new_class_id": "00000000-0000-0000-0000-000000000002",
            "reason": "Better fit for student's academic needs",
            "status": "PENDING",
            "status_updated_by": None,
            "status_updated_at": None,
            "rejection_reason": None,
            "created_at": "2024-02-17T12:00:00Z",
            "created_by": "00000000-0000-0000-0000-000000000000",
            "last_modified_at": "2024-02-17T12:00:00Z",
            "last_modified_by": "00000000-0000-0000-0000-000000000000",
            "is_archived": False,
            "archived_at": None,
            "archived_by": None,
            "archive_reason": None
        }
    }