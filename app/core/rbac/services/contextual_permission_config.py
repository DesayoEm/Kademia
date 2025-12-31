"""
Configuration mapping resources to their SQLAlchemy model classes.

Provides the RESOURCE_TO_MODEL dictionary used by PermissionService to
resolve Resource enum values to their corresponding database models for
contextual access checks.

When checking if a user can access a specific resource instance (e.g.,
"can this student view grade X?"), the service uses this mapping to:
1. Look up the model class for the resource type.
2. Query for the specific record by ID.
3. Check ownership via the record's student_id field.

Usage:
    from app.core.rbac.services.contextual_permission_config import RESOURCE_TO_MODEL

    model_class = RESOURCE_TO_MODEL.get(Resource.GRADE)
    record = session.query(model_class).filter_by(id=grade_id).first()

Extending:
    To add contextual access support for a new resource:
    1. Add the Resource enum value to shared/models/enums.py.
    2. Import the model class here.
    3. Add the mapping: Resource.NEW_RESOURCE: NewResourceModel
    4. Ensure the model has a student_id field for ownership checks,
       or add custom handling in PermissionService.

Note:
    Only resources requiring contextual (instance-level) access checks
    need to be mapped here. Resources that only need role-based permission
    checks don't require an entry.

Models mapped:
    - STUDENT -> Student
    - DOCUMENT -> StudentDocument
    - AWARD -> StudentAward
    - GRADE -> Grade
    - TOTAL_GRADE -> TotalGrade
    - PROMOTION -> Promotion
    - REPETITION -> Repetition
    - TRANSFER -> DepartmentTransfer
    - STUDENT_SUBJECT -> StudentSubject
"""


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
