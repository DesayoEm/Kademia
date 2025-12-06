from .base_error import KademiaError
from uuid import UUID


class CurriculumError(KademiaError):
    """Base exception for all curriculum-related exceptions"""


class AcademicLevelMismatchError(CurriculumError):
    """Raised when attempting to assign a subject outside student's academic level"""

    def __init__(self, student_id: UUID, academic_level_id: UUID):
        super().__init__()
        self.user_message = "Cannot assign subject from different academic level"
        self.log_message = f"Academic level mismatch: Student {student_id} is not in level {academic_level_id}"
