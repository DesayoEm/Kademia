from pathlib import Path
from dotenv import load_dotenv
current_dir = Path(__file__).resolve().parent
env_path = current_dir / ".env"
load_dotenv(dotenv_path=env_path)

from fastapi import FastAPI
app = FastAPI()

from V2.app.routers.curriculum import subject, subject_archive
from V2.app.routers.staff_management import staff_departments_archive, staff_roles_archive
from V2.app.routers.staff_management import qualifications, staff_departments, staff_roles, qualifications_archive
from V2.app.routers.academic_structure import (
    academic_levels, academic_levels_archive, student_departments, student_departments_archive, classes, classes_archive
)
from V2.app.routers.curriculum import (
    level_subject, level_subject_archive, student_subject, student_subject_archive, subject, subject_archive,
    subject_educator, subject_educator_archive
)
from V2.app.routers.identity import guardian, guardian_archive, student, student_archive, staff_archive, staff
from V2.app.routers.auth import password, auth
from V2.app.infra.middleware.exception_handler import ExceptionMiddleware
from V2.app.infra.log_service.logger import logger

version = "v1"

app = FastAPI(
    version = version,
    title = "Kademia"
)

app.add_middleware(ExceptionMiddleware)

# auth
app.include_router(auth.router, prefix=f"/api/{version}/auth",
                   tags=["Auth"])

app.include_router(password.router, prefix=f"/api/{version}/auth",
                   tags=["Auth", "Password"])
# Subject
app.include_router(subject.router, prefix=f"/api/{version}/admin/subjects",
                   tags=["Subjects", "Admin"])
app.include_router(subject_archive.router, prefix=f"/api/{version}/admin/archive/subjects",
                   tags=["Archived","Subjects", "Admin"])
# Level Subject
app.include_router(level_subject.router, prefix=f"/api/{version}/admin/curriculum/levelsubjects",
                   tags=["Level Subjects", "Admin"])
app.include_router(level_subject_archive.router, prefix=f"/api/{version}/admin/archive/curriculum/levelsubjects",
                   tags=["Archived","Level Subjects", "Admin"])
# Student Subject
app.include_router(student_subject.router, prefix=f"/api/{version}/admin/curriculum/studentsubject",
                   tags=["Student Subjects", "Admin"])
app.include_router(student_subject_archive.router, prefix=f"/api/{version}/admin/archive/curriculum/studentsubject",
                   tags=["Archived","Student Subjects", "Admin"])
# Subject Educator
app.include_router(subject_educator.router, prefix=f"/api/{version}/admin/curriculum/subjecteducator",
                   tags=["Subject Educators", "Admin"])
app.include_router(subject_educator.router, prefix=f"/api/{version}/admin/archive/curriculum/subjecteducator",
                   tags=["Archived","Subject Educators", "Admin"])
# Staff
app.include_router(staff.router, prefix=f"/api/{version}/admin/staff",
                   tags=["Staff", "Admin"])
app.include_router(staff_archive.router, prefix=f"/api/{version}/admin/archive/staff",
                   tags=["Archived","Staff", "Admin"])
# Students
app.include_router(student.router, prefix=f"/api/{version}/admin/students",
                   tags=["Students", "Admin"])
app.include_router(student_archive.router, prefix=f"/api/{version}/admin/archive/students",
                   tags=["Archived","Students", "Admin"])
# Guardians
app.include_router(guardian.router, prefix=f"/api/{version}/admin/guardians",
                   tags=["Guardians", "Admin"])
app.include_router(guardian_archive.router, prefix=f"/api/{version}/admin/archive/guardians",
                   tags=["Archived","Guardians", "Admin"])
# Staff Departments
app.include_router(staff_departments.router, prefix=f"/api/{version}/admin/staff/departments",
                   tags=["Staff Departments", "Admin"])
app.include_router(staff_departments_archive.router, prefix=f"/api/{version}/admin/archive/staff/departments",
                   tags=["Archived", "Staff Departments", "Admin"])
# Roles
app.include_router(staff_roles.router, prefix=f"/api/{version}/admin/staff/roles",
                   tags=["Staff Roles", "Admin"])
app.include_router(staff_roles_archive.router, prefix=f"/api/{version}/admin/archive/staff/roles",
                   tags=["Archived","Staff Roles", "Admin"])
# Qualifications
app.include_router(qualifications.router, prefix=f"/api/{version}/admin/staff/qualifications",
                   tags=["Qualifications", "Admin"])
app.include_router(qualifications_archive.router, prefix=f"/api/{version}/admin/archive/staff/qualifications",
                   tags=["Archived","Qualifications", "Admin"])
# Student Departments
app.include_router(student_departments.router, prefix=f"/api/{version}/admin/students/departments",
                   tags=["Student Departments", "Admin"])
app.include_router(student_departments_archive.router, prefix=f"/api/{version}/admin/archive/students/departments",
                   tags=["Archived","Student Departments", "Admin"])
# Academic Levels
app.include_router(academic_levels.router, prefix=f"/api/{version}/admin/students/academic_levels",
                   tags=["Academic levels", "Admin"])
app.include_router(academic_levels_archive.router, prefix=f"/api/{version}/admin/archive/students/academic_levels",
                   tags=["Archived","Academic levels", "Admin"])
# Classes
app.include_router(classes.router, prefix=f"/api/{version}/admin/students/student_organization",
                   tags=["Classes", "Admin"])
app.include_router(classes_archive.router, prefix=f"/api/{version}/admin/archive/students/student_organization",
                   tags=["Archived","Classes", "Admin"])





@app.get("/")
async def root():
    return {"message": "Welcome to Kademia!"}

logger.info("Application started")