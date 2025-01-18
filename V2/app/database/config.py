from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from app.database.models.common_imports import Base
from app.security.auth_models import Users, AccessLevelChanges
from app.database.models.profiles import ProfileBase,Students, Parents, Staff, Admin, Educator, Commercial, Management, Support
from app.database.models.academic import Subjects, Grades, TotalGrades, StudentSubjects, EducatorSubjects,Repetitions, StudentTransfers
from app.database.models.documents import StudentDocuments
from app.database.models.organization import Departments, Classes, StaffDepartments, StaffRoles
import os

load_dotenv()
database_url = os.getenv("DATABASE_URL")
engine= create_engine(database_url, echo=True)


