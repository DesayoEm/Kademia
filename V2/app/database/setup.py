from config import engine
from .models.common_imports import Base
from V2.app.security.auth_models import (AccessLevelChanges)
from models.profiles import ProfileBase,Students, Parents, Staff, System, Educator, Operations, Support
from models.academic import Subjects, Grades, TotalGrades, StudentSubjects,Repetitions, StudentTransfers
from models.documents import StudentDocuments
from models.organization import Departments, Classes, StaffDepartments, StaffRoles

def create_tables():
    print('create_tables')
    Base.metadata.create_all(engine)