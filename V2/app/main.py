from pathlib import Path
from dotenv import load_dotenv
current_dir = Path(__file__).resolve().parent
env_path = current_dir / ".env"
load_dotenv(dotenv_path=env_path)

from fastapi import FastAPI

app = FastAPI()

from .routers.staff_organization import (
    qualifications, staff_departments, staff_roles, archived_qualifications,
    archived_staff_departments, staff_roles_archive
)
from .routers.student_organization import (
    student_departments, archived_student_departments, academic_levels, archived_academic_levels,
    classes, archived_classes
)
from .routers.users.staff import staff, archived_staff
from .routers.users.student import student, archived_student
from .routers.users.guardian import guardian, archived_guardian
from .routers.auth import auth, password
from .middleware.error_handler import ExceptionMiddleware
from .log_service.logger import logger

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



# Staff
app.include_router(staff.router, prefix=f"/api/{version}/admin/staff",
                   tags=["Staff", "Admin"])
app.include_router(archived_staff.router, prefix=f"/api/{version}/admin/archive/staff",
                   tags=["Archived","Staff", "Admin"])

# /api/educators/
# /api/support-staff/
# /api/administrative-staff


# Students
app.include_router(student.router, prefix=f"/api/{version}/admin/students",
                   tags=["Students", "Admin"])
app.include_router(archived_student.router, prefix=f"/api/{version}/admin/archive/students",
                   tags=["Archived","Students", "Admin"])

# Guardians
app.include_router(guardian.router, prefix=f"/api/{version}/admin/guardians",
                   tags=["Guardians", "Admin"])
app.include_router(archived_guardian.router, prefix=f"/api/{version}/admin/archive/guardians",
                   tags=["Archived","Guardians", "Admin"])



# Staff Departments
app.include_router(staff_departments.router, prefix=f"/api/{version}/admin/staff/departments",
                   tags=["Staff Departments", "Admin"])
app.include_router(archived_staff_departments.router, prefix=f"/api/{version}/admin/archive/staff/departments",
                   tags=["Archived", "Staff Departments", "Admin"])

# Roles
app.include_router(staff_roles.router, prefix=f"/api/{version}/admin/staff/roles",
                   tags=["Staff Roles", "Admin"])
app.include_router(staff_roles_archive.router, prefix=f"/api/{version}/admin/archive/staff/roles",
                   tags=["Archived","Staff Roles", "Admin"])

# Qualifications
app.include_router(qualifications.router, prefix=f"/api/{version}/admin/staff/qualifications",
                   tags=["Qualifications", "Admin"])
app.include_router(archived_qualifications.router, prefix=f"/api/{version}/admin/archive/staff/qualifications",
                   tags=["Archived","Qualifications", "Admin"])

# Student Departments
app.include_router(student_departments.router, prefix=f"/api/{version}/admin/students/departments",
                   tags=["Student Departments", "Admin"])
app.include_router(archived_student_departments.router, prefix=f"/api/{version}/admin/archive/students/departments",
                   tags=["Archived","Student Departments", "Admin"])

# Academic Levels
app.include_router(academic_levels.router, prefix=f"/api/{version}/admin/students/academic_levels",
                   tags=["Academic levels", "Admin"])
app.include_router(archived_academic_levels.router, prefix=f"/api/{version}/admin/archive/students/academic_levels",
                   tags=["Archived","Academic levels", "Admin"])

# Classes
app.include_router(classes.router, prefix=f"/api/{version}/admin/students/student_organization",
                   tags=["Classes", "Admin"])
app.include_router(archived_classes.router, prefix=f"/api/{version}/admin/archive/students/student_organization",
                   tags=["Archived","Classes", "Admin"])





@app.get("/")
async def root():
    return {"message": "Welcome to Kademia!"}

logger.info("Application started")