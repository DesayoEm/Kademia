from V2.app.core.shared.schemas.common_imports import *
from V2.app.core.shared.schemas.shared_models import *


class AcademicLevelSubjectFilterParams(BaseFilterParams):
    is_elective: str | None = None
    academic_session: str | None = None


class AcademicLevelSubjectBase(BaseModel):
    """Base model for academic level subject assignments"""
    subject_id: UUID
    is_elective: bool = True
    educator_id: UUID | None = None
    academic_session: str | None = None


    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra={
            "example": {
                "subject_id": "00000000-0000-0000-0000-000000000002",
                "is_elective": True,
                "academic_session": "2025/2026",
            }
        }
    )

class AcademicLevelSubjectResponse(AcademicLevelSubjectBase):
    """Response model for academic level subject assignments"""
    pass


class AcademicLevelSubjectCreate(AcademicLevelSubjectBase):
     """For creating new academic level subject assignments"""


class AcademicLevelSubjectUpdate(AcademicLevelSubjectBase):
    """For updating academic level subject assignments"""
    is_elective: bool = True
    academic_session: str | None = None

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra={
            "example": {
                "is_elective": True,
                "academic_session": "2023-2024",
            }
        }
    )

