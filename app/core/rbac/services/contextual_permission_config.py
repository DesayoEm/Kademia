
from app.core.identity.models.staff import Staff, Educator
from app.core.identity.models.student import Student
from app.core.identity.models.guardian import Guardian
from app.core.rbac.models import Permission, Role
from app.core.shared.models.enums import Resource, Action

from app.core.assessment.models.assessment import Grade, TotalGrade
from app.core.documents.models.documents import StudentDocument, StudentAward
from app.core.progression.models.progression import Promotion, Repetition
from app.core.transfer.models.transfer import DepartmentTransfer
from app.core.curriculum.models.curriculum import StudentSubject

RESOURCE_TO_MODEL = {
    Resource.STUDENT: Student,
    Resource.DOCUMENT: StudentDocument,
    Resource.AWARD: StudentAward,
    Resource.GRADE: Grade,
    Resource.TOTAL_GRADE: TotalGrade,
    Resource.PROMOTION: Promotion,
    Resource.REPETITION: Repetition,
    Resource.TRANSFER: DepartmentTransfer,
    Resource.STUDENT_SUBJECT: StudentSubject,
}
