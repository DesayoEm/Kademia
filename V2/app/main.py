from pathlib import Path
from dotenv import load_dotenv
current_dir = Path(__file__).resolve().parent
env_path = current_dir / ".env"
load_dotenv(dotenv_path=env_path)

from fastapi import FastAPI
app = FastAPI()

from V2.app.routers.staff_management import staff_departments_archive, staff_roles_archive
from V2.app.routers.staff_management import qualifications, staff_departments, staff_roles, qualifications_archive
from V2.app.routers.academic_structure import (
    academic_levels, academic_levels_archive, student_departments, student_departments_archive,
    classes, classes_archive
)
from V2.app.routers.curriculum import (
    level_subject, level_subject_archive, student_subject, student_subject_archive, subject,subject_archive,
    subject_educator, subject_educator_archive
)
from V2.app.routers.documents import award, award_archive, document_archive, document
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

# Authentication
app.include_router(auth.router, prefix=f"/api/{version}/auth",
                   tags=["Auth"])
app.include_router(password.router, prefix=f"/api/{version}/auth/password",
                   tags=["Auth"])


# Curriculum
app.include_router(subject.router, prefix=f"/api/{version}/curriculum/subjects",
                   tags=["Subjects", "Admin"])
app.include_router(subject_archive.router, prefix=f"/api/{version}/curriculum/subjects/archived",
                   tags=["Subjects", "Admin"])

app.include_router(level_subject.router, prefix=f"/api/{version}/curriculum/level-subjects",
                   tags=["Curriculum", "Admin"])
app.include_router(level_subject_archive.router, prefix=f"/api/{version}/curriculum/level-subjects/archived",
                   tags=["Curriculum", "Admin"])
app.include_router(student_subject.router, prefix=f"/api/{version}/curriculum/student-subjects",
                   tags=["Curriculum", "Admin"])
app.include_router(student_subject_archive.router, prefix=f"/api/{version}/curriculum/student-subjects/archived",
                   tags=["Curriculum", "Admin"])
app.include_router(subject_educator.router, prefix=f"/api/{version}/curriculum/subject-educators",
                   tags=["Curriculum", "Admin"])
app.include_router(subject_educator_archive.router, prefix=f"/api/{version}/curriculum/subject-educators/archived",
                   tags=["Curriculum", "Admin"])

# Staff
app.include_router(staff.router, prefix=f"/api/{version}/staff",
                   tags=["Staff", "Admin"])
app.include_router(staff_archive.router, prefix=f"/api/{version}/staff/archived",
                   tags=["Staff", "Admin"])
app.include_router(staff_departments.router, prefix=f"/api/{version}/staff/departments",
                   tags=["Staff", "Admin"])
app.include_router(staff_departments_archive.router, prefix=f"/api/{version}/staff/departments/archived",
                   tags=["Staff", "Admin"])
app.include_router(staff_roles.router, prefix=f"/api/{version}/staff/roles",
                   tags=["Staff", "Admin"])
app.include_router(staff_roles_archive.router, prefix=f"/api/{version}/staff/roles/archived",
                   tags=["Staff", "Admin"])
app.include_router(qualifications.router, prefix=f"/api/{version}/staff/qualifications",
                   tags=["Staff", "Admin"])
app.include_router(qualifications_archive.router, prefix=f"/api/{version}/staff/qualifications/archived",
                   tags=["Staff", "Admin"])

# Students
app.include_router(student.router, prefix=f"/api/{version}/students",
                   tags=["Students", "Admin"])
app.include_router(student_archive.router, prefix=f"/api/{version}/students/archived",
                   tags=["Students", "Admin"])
app.include_router(award.router, prefix=f"/api/{version}/students/awards",
                   tags=["Students", "Admin"])
app.include_router(award_archive.router, prefix=f"/api/{version}/students/awards/archived",
                   tags=["Students", "Admin"])
app.include_router(document.router, prefix=f"/api/{version}/students/documents",
                   tags=["Students", "Admin"])
app.include_router(document_archive.router, prefix=f"/api/{version}/students/documents/archived",
                   tags=["Students", "Admin"])
app.include_router(student_departments.router, prefix=f"/api/{version}/students/departments",
                   tags=["Students", "Admin"])
app.include_router(student_departments_archive.router, prefix=f"/api/{version}/students/departments/archived",
                   tags=["Students", "Admin"])
app.include_router(academic_levels.router, prefix=f"/api/{version}/students/academic-levels",
                   tags=["Students", "Admin"])
app.include_router(academic_levels_archive.router, prefix=f"/api/{version}/students/academic-levels/archived",
                   tags=["Students", "Admin"])

app.include_router(classes.router, prefix=f"/api/{version}/students/classes",
                   tags=["Classes", "Admin"])
app.include_router(classes_archive.router, prefix=f"/api/{version}/students/classes/archived",
                   tags=["Classes", "Admin"])


# Guardians
app.include_router(guardian.router, prefix=f"/api/{version}/guardians",
                   tags=["Guardians", "Admin"])
app.include_router(guardian_archive.router, prefix=f"/api/{version}/guardians/archived",
                   tags=["Guardians", "Admin"])





@app.get("/")
async def root():
    return {"message": "Welcome to Kademia!"}

logger.info("Application started")