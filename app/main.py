from pathlib import Path
from dotenv import load_dotenv
current_dir = Path(__file__).resolve().parent
env_path = current_dir / ".env"
load_dotenv(dotenv_path=env_path)

from fastapi import FastAPI
app = FastAPI()

from app.api.staff_management import staff_departments_archive, staff_roles_archive
from app.api.staff_management import staff_roles
from app.api.staff_management import qualifications, staff_departments
from app.api.academic_structure import (
    academic_levels, academic_levels_archive, departments, departments_archive,
    classes_archive
)
from app.api.academic_structure import classes
from app.api.curriculum import (
    level_subject, student_subject, student_subject_archive, subject_educator_archive
)
from app.api.curriculum import subject, level_subject_archive, subject_educator, subject_archive
from app.api.progression import (
    repetition_archive,
    promotion, promotion_archive
)
from app.api.progression import repetition
from app.api.transfer import department_transfer
from app.api.assessment import total_grade
from app.api.assessment import grade_archive, grade, total_grade_archive
from app.api.documents import award
from app.api.documents import document, document_archive, award_archive
from app.api.identity import student, staff_archive, guardian, staff, student_archive, guardian_archive
from app.api.auth import password
from app.api.auth import access_level_change_archive, auth, access_level_change
from app.infra.middleware.exception_handler import ExceptionMiddleware
from app.infra.log_service.logger import logger

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


# Staff Org
app.include_router(staff_departments.router, prefix=f"/api/{version}/staff/departments",
                   tags=["Staff Departments", "Admin"])
app.include_router(staff_departments_archive.router, prefix=f"/api/{version}/staff/departments/archived",
                   tags=["Staff Departments", "Admin"])

app.include_router(staff_roles.router, prefix=f"/api/{version}/staff/roles",
                   tags=["Staff Roles", "Admin"])
app.include_router(staff_roles_archive.router, prefix=f"/api/{version}/staff/roles/archived",
                   tags=["Staff Roles", "Admin"])

app.include_router(qualifications.router, prefix=f"/api/{version}/staff/qualifications",
                   tags=["Educator Qualifications", "Admin"])

#Academic Structure
app.include_router(departments.router, prefix=f"/api/{version}/students/departments",
                   tags=["Student Department", "Admin"])
app.include_router(departments_archive.router, prefix=f"/api/{version}/students/departments/archived",
                   tags=["Student Department", "Admin"])

app.include_router(academic_levels.router, prefix=f"/api/{version}/students/academic-levels",
                   tags=["Level", "Admin"])
app.include_router(academic_levels_archive.router, prefix=f"/api/{version}/students/academic-levels/archived",
                   tags=["Level", "Admin"])

app.include_router(classes.router, prefix=f"/api/{version}/students/classes",
                   tags=["Classes", "Admin"])
app.include_router(classes_archive.router, prefix=f"/api/{version}/students/classes/archived",
                   tags=["Classes", "Admin"])


#Users
app.include_router(staff.router, prefix=f"/api/{version}/staff",
                   tags=["Staff", "Admin"])
app.include_router(staff_archive.router, prefix=f"/api/{version}/staff/archived",
                   tags=["Staff", "Admin"])

# Access level
app.include_router(access_level_change.router, prefix=f"/api/{version}",
                   tags=["Auth", "Access Level"])
app.include_router(access_level_change_archive.router, prefix=f"/api/{version}",
                   tags=["Auth", "Access Level"])


app.include_router(guardian.router, prefix=f"/api/{version}/guardians",
                   tags=["Guardians", "Admin"])
app.include_router(guardian_archive.router, prefix=f"/api/{version}/guardians/archived",
                   tags=["Guardians", "Admin"])


app.include_router(student.router, prefix=f"/api/{version}/students",
                   tags=["Students", "Admin"])
app.include_router(student_archive.router, prefix=f"/api/{version}/students/archived",
                   tags=["Students", "Admin"])


#Docs
app.include_router(award.router, prefix=f"/api/{version}/students/awards",
                   tags=["Awards", "Admin"])
app.include_router(award_archive.router, prefix=f"/api/{version}/students/awards/archived",
                   tags=["Awards", "Admin"])

app.include_router(document.router, prefix=f"/api/{version}/students/documents",
                   tags=["Documents", "Admin"])
app.include_router(document_archive.router, prefix=f"/api/{version}/students/documents/archived",
                   tags=["Documents", "Admin"])

# Curriculum
app.include_router(subject.router, prefix=f"/api/{version}/curriculum/subjects",
                   tags=["Subjects", "Admin"])
app.include_router(subject_archive.router, prefix=f"/api/{version}/curriculum/subjects/archived",
                   tags=["Subjects", "Admin"])

app.include_router(level_subject.router, prefix=f"/api/{version}/curriculum/level-subjects",
                   tags=["Level Subjects", "Admin"])
app.include_router(level_subject_archive.router, prefix=f"/api/{version}/curriculum/level-subjects/archived",
                   tags=["Level Subjects", "Admin"])

app.include_router(student_subject.router, prefix=f"/api/{version}/curriculum/student-subjects",
                   tags=["Student Subjects", "Admin"])
app.include_router(student_subject_archive.router, prefix=f"/api/{version}/curriculum/student-subjects/archived",
                   tags=["Student Subjects", "Admin"])

app.include_router(subject_educator.router, prefix=f"/api/{version}/curriculum/subject-educators",
                   tags=["Subject Educator", "Admin"])
app.include_router(subject_educator_archive.router, prefix=f"/api/{version}/curriculum/subject-educators/archived",
                   tags=["Subject Educator", "Admin"])




# Assessment
app.include_router(grade.router, prefix=f"/api/{version}/students/assessment/grades",
                   tags=["Assessment", "Admin"])
app.include_router(grade_archive.router, prefix=f"/api/{version}/students/assessment/archived/grade",
                   tags=["Assessment", "Admin"])

app.include_router(total_grade.router, prefix=f"/api/{version}/students/assessment/total-grades",
                   tags=["Assessment", "Admin"])
app.include_router(total_grade_archive.router, prefix=f"/api/{version}/students/assessment/archived/total-grade",
                   tags=["Assessment", "Admin"])

# Progression
app.include_router(repetition.router, prefix=f"/api/{version}/students/repetitions",
                   tags=["Progression", "Admin"])
app.include_router(repetition_archive.router, prefix=f"/api/{version}/students/repetitions/archived",
                   tags=["Progression", "Admin"])

app.include_router(promotion.router, prefix=f"/api/{version}/students/promotions",
                   tags=["Progression", "Admin"])
app.include_router(promotion_archive.router, prefix=f"/api/{version}/students/promotions/archived",
                   tags=["Progression", "Admin"])



app.include_router(department_transfer.router, prefix=f"/api/{version}/department-transfers",
                   tags=["Department Transfers", "Admin"])






@app.get("/")
async def root():
    return {"message": "Welcome to Kademia!"}

logger.info("Application started")