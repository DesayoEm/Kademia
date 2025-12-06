from app.core.shared.schemas.common_imports import *
from app.core.shared.schemas.shared_models import *
from app.core.shared.schemas.enums import Term


class CourseListRequest(BaseModel):
    """Request model for enrollments"""

    academic_session: str
    term: Term

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra={
            "example": {"academic_session": "2025/2026", "term": "FIRST"}
        },
    )


from app.core.shared.schemas.common_imports import *
from app.core.shared.schemas.shared_models import *
from app.core.shared.schemas.enums import Term
from datetime import date
from typing import List, Tuple


class CourseItem(BaseModel):
    """Individual course item in the course list"""

    course_code: str
    course_title: str
    educator_name: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "course_code": "MATH101",
                "course_title": "Algebra I",
                "educator_name": "Mrs. Johnson",
            }
        },
    )


class CourseListResponse(BaseModel):
    """Response model for student course list"""

    student_name: str
    term: Term
    academic_session: str
    date_generated: str
    enrollment_list: List[CourseItem]

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "student_name": "Johnny Smith",
                "term": "FIRST",
                "academic_session": "2025/2026",
                "date_generated": "2025-07-09",
                "enrollment_list": [
                    {
                        "course_code": "MATH101",
                        "course_title": "Algebra I",
                        "educator_name": "Mrs. Johnson",
                    }
                ],
            }
        },
    )
