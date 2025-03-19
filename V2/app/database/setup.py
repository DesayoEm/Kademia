from db_config import engine
from V2.app.database.models.common_imports import Base
from V2.app.database.models.users import ProfileBase,Students, Guardians, Staff, Educator, Support, System
from V2.app.database.models.academic import Subjects, Grades, TotalGrades, StudentSubjects,StudentRepetitions, SubjectEducators, AcademicLevelSubjects, StudentAwards
from V2.app.database.models.documents import StudentDocuments
from V2.app.database.models.auth_models import AccessLevelChanges
from V2.app.database.models.student_organization import (
    StudentDepartments, Classes, AcademicLevel, StudentClassTransfers, StudentDepartmentTransfers
)
from V2.app.database.models.staff_organization import EducatorQualifications, StaffDepartments, StaffRoles


def create_tables():
    print('create_tables')
    Base.metadata.create_all(engine)

create_tables()