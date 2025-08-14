from db_config import engine
from app.core.shared.models.common_imports import Base
from app.core.rbac.models import Permission, Role, RolePermission, RoleHistory, StudentRole, StaffRole, GuardianRole
from app.core.progression.models.progression import Promotion, Repetition
from app.core.documents.models.documents import StudentDocument, StudentAward
from app.core.curriculum.models.curriculum import Subject, SubjectEducator, StudentSubject, AcademicLevelSubject
from app.core.staff_management.models import StaffDepartment, StaffTitle, EducatorQualification
from app.core.academic_structure.models import StudentDepartment, Classes, AcademicLevel
from app.core.transfer.models.transfer import DepartmentTransfer
from app.core.assessment.models.assessment import Grade, TotalGrade
from app.core.identity.models.student import Student
from app.core.identity.models.guardian import Guardian

def create_tables():
    print('create_tables')
    Base.metadata.create_all(engine)

if __name__ =='__main__':
    create_tables()