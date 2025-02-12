from config import engine
from V2.app.database.models.common_imports import Base
from V2.app.database.models.profiles import ProfileBase,Students, Parents, Staff, Educator, Support, System
from V2.app.database.models.academic import Subjects, Grades, TotalGrades, StudentSubjects,Repetitions, StudentTransfers, EducatorQualifications
from V2.app.database.models.documents import StudentDocuments
from V2.app.database.models.auth_models import AccessLevelChanges
from V2.app.database.models.organization import Departments, Classes, StaffDepartments, StaffRoles


def create_tables():
    print('create_tables')
    Base.metadata.create_all(engine)

create_tables()