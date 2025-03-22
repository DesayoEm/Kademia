from db_config import engine
from V2.app.database.models.common_imports import Base
from V2.app.database.models.users import Student, Guardian, Staff, Educator, SupportStaff, System
from V2.app.database.models.academic import Subject, Grade, TotalGrade, StudentSubject,Repetition, SubjectEducator, AcademicLevelSubject, StudentAward
from V2.app.database.models.documents import StudentDocument
from V2.app.database.models.auth_models import AccessLevelChange
from V2.app.database.models.student_organization import (
    StudentDepartment, Classes, AcademicLevel, ClassTransfer, StudentDepartmentTransfer
)
from V2.app.database.models.staff_organization import EducatorQualification, StaffDepartment, StaffRole


def create_tables():
    print('create_tables')
    Base.metadata.create_all(engine)

create_tables()