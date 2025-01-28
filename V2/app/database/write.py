from config import engine
from uuid import uuid4, UUID
from datetime import datetime
from sqlalchemy.orm import Session
from models.common_imports import Base
from V2.app.security.auth_models import AccessLevelChanges
from models.profiles import ProfileBase,Students, Parents, Staff, System, Educator, Operations, Support
from models.academic import Subjects, Grades, TotalGrades, StudentSubjects, EducatorSubjects,Repetitions, StudentTransfers
from models.documents import StudentDocuments
from models.organization import Departments, Classes, StaffDepartments, StaffRoles
from models.data_enums import UserType, AccessLevel, Gender, StaffType

TRAKADEMIK_ID = UUID('00000000-0000-0000-0000-000000000000')
with Session(engine) as session:
    prs = session.query(StaffDepartments).filter_by(
        id = TRAKADEMIK_ID).first()
    print(prs.name)

# try:
#     with Session(engine) as session:
#
#         system_department = StaffDepartments(
#             id = UUID('00000000-0000-0000-0000-000000000000'),
#             name = 'System',
#             description= 'System'
#         )
#         session.add(system_department)
#         session.flush()
#
#         system_role = StaffRoles (
#             id = UUID('00000000-0000-0000-0000-000000000000'),
#             name = 'System',
#             description= 'System'
#         )
#         session.add(system_role)
#         session.flush()
#
#         system_user = System(
#             user_id = TRAKADEMIK_ID,
#             id=TRAKADEMIK_ID,
#             image_url = "path-to-img",
#             password_hash="trakademik_system",
#             access_level="System",
#             first_name="TraKademik",
#             last_name="System",
#             gender="S",
#             is_verified=True,
#             email_address="system@trakademik.com",
#             phone="00000000000",
#             department_id = system_department.id,
#             role_id = system_role.id,
#             address="System",
#             staff_type="System",
#             date_joined=datetime.now().date()
#         )
#         session.add(system_user)
#         session.commit()
#         print("System user and staff created successfully with shared ID.")
# except Exception as e:
#     print(f"Error: {e}")