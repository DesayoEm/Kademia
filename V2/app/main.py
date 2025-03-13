from fastapi import FastAPI
from .routers.staff_organization import (
    qualifications, staff_departments, staff_roles, archived_qualifications, archived_staff_departments,
    archived_staff_roles
)

from .routers.student_organization import (
    student_departments, archived_student_departments
)
from .middleware.error_handler import ExceptionMiddleware
from .logging.logger import logger

version = "v1"
app = FastAPI(
    version = version,
    title = "TraKademik"
)

app.add_middleware(ExceptionMiddleware)

# Qualifications
app.include_router(qualifications.router, prefix=f"/api/{version}/staff/qualifications",
                   tags=["Qualifications"])
app.include_router(archived_qualifications.router, prefix=f"/api/{version}/archive/staff/qualifications",
                   tags=["Archived","Qualifications"])

# Staff Departments
app.include_router(staff_departments.router, prefix=f"/api/{version}/staff/departments",
                   tags=["Staff Departments"])
app.include_router(archived_staff_departments.router, prefix=f"/api/{version}/archive/staff/departments",
                   tags=["Archived", "Staff Departments"])

# Roles
app.include_router(staff_roles.router, prefix=f"/api/{version}/staff/roles",
                   tags=["Staff Roles"])
app.include_router(archived_staff_roles.router, prefix=f"/api/{version}/archive/staff/roles",
                   tags=["Archived","Staff Roles"])

# Student Departments
app.include_router(student_departments.router, prefix=f"/api/{version}/students/departments",
                   tags=["Student Departments"])
app.include_router(archived_student_departments.router, prefix=f"/api/{version}/archive/students/departments",
                   tags=["Archived","Student Departments"])


@app.get("/")
async def root():
    return {"message": "Welcome to TraKademik!"}

logger.info("Application started")