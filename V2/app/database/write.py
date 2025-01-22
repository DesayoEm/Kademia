from config import engine
from uuid import uuid4, UUID
from datetime import datetime
from sqlalchemy.orm import Session
from models.common_imports import Base
from V2.app.security.auth_models import (Users, AccessLevelChanges)
from models.profiles import ProfileBase,Students, Parents, Staff, System, Educator, Operations, Support
from models.academic import Subjects, Grades, TotalGrades, StudentSubjects, EducatorSubjects,Repetitions, StudentTransfers
from models.documents import StudentDocuments
from models.organization import Departments, Classes, StaffDepartments, StaffRoles
from models.data_enums import UserType, AccessLevel, Gender, StaffType

TRAKADEMIK_ID = uuid4()

try:
    with Session(engine) as session:
        system_user = Users(
            profile_id=TRAKADEMIK_ID,
            user_type="System",  # Exact match with database enum
            password_hash="trakademik_system",
            access_level="System",  # Exact match with database enum
            is_active=True,
            is_verified=True
        )
        system_department = StaffDepartments(
            id = UUID('00000000-0000-0000-0000-000000000000'),
            name = 'System',
            description= 'System'
        )

        system_role = StaffRoles (
            id = UUID('00000000-0000-0000-0000-000000000000'),
            name = 'System',
            description= 'System'
        )

        system_staff = Staff(
            id=TRAKADEMIK_ID,
            image_url = "path-to-img",
            profile_id=TRAKADEMIK_ID,
            first_name="TraKademik",
            last_name="System",
            gender="S",
            email_address="system@trakademik.com",
            phone="00000000000",
            department_id = system_department.id,
            role_id = system_role.id,
            address="System",
            staff_type="System",
            is_active=True,
            date_joined=datetime.now().date()
        )

        session.add(system_user)
        session.add(system_department)
        session.add(system_role)
        session.flush()
        session.add(system_staff)
        session.commit()
        print("System user and staff created successfully with shared ID.")
except Exception as e:
    print(f"Error: {e}")