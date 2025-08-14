from pathlib import Path
from dotenv import load_dotenv
current_dir = Path(__file__).resolve().parent
env_path = current_dir / ".env"
load_dotenv(dotenv_path=env_path)

from fastapi import FastAPI
app = FastAPI()


from app.api.staff_management import staff_departments_archive
from app.api.staff_management import qualifications, staff_departments, staff_titles
from app.api.academic_structure import academic_levels, departments, classes
from app.api.curriculum import subject, level_subject, student_subject, subject_educator

from app.api.progression import repetition_archive,promotion, promotion_archive, repetition
from app.api.transfer import department_transfer
from app.api.assessment import total_grade, grade
from app.api.documents import award, document

from app.api.identity import student, guardian, staff, educator
from app.api.auth import password
from app.api.auth import auth, access_level_change

from app.infra.middleware.exception_handler import ExceptionMiddleware
from app.infra.log_service.logger import logger

version = "v1"

app = FastAPI(
    version = version,
    title = "Kademia"
)

app.add_middleware(ExceptionMiddleware)

# Authentication
app.include_router(auth.router, prefix=f"/api/{version}/auth",tags=["Auth"])
app.include_router(password.router, prefix=f"/api/{version}/auth/password",tags=["Auth"])

# Access level
app.include_router(access_level_change.router, prefix=f"/api/{version}",tags=["Auth", "Access Level"])

# Staff Org
app.include_router(staff_titles.router, prefix=f"/api/{version}/",tags=["Staff Titles", "Admin"])
app.include_router(staff_departments.router, prefix=f"/api/{version}/staff/departments",
                   tags=["Staff Departments", "Admin"])
app.include_router(staff_departments_archive.router, prefix=f"/api/{version}/staff/departments/archived",
                   tags=["Staff Departments", "Admin"])



app.include_router(qualifications.router, prefix=f"/api/{version}/staff/qualifications",
                   tags=["Educator Qualifications", "Admin"])

#Academic Structure
app.include_router(departments.router, prefix=f"/api/{version}/students/departments",tags=["Student Department", "Admin"])
app.include_router(academic_levels.router, prefix=f"/api/{version}/students/academic-levels",tags=["Level", "Admin"])
app.include_router(classes.router, prefix=f"/api/{version}/students/classes",tags=["Classes", "Admin"])

#Users
app.include_router(staff.router, prefix=f"/api/{version}", tags=["Staff", "Admin"])
app.include_router(educator.router, prefix=f"/api/{version}", tags=["Educators", "Admin"])
app.include_router(guardian.router, prefix=f"/api/{version}/guardians",tags=["Guardians", "Admin"])
app.include_router(student.router, prefix=f"/api/{version}",tags=["Students", "Admin"])

#Docs
app.include_router(award.router, prefix=f"/api/{version}/students/awards",tags=["Awards", "Admin"])
app.include_router(document.router, prefix=f"/api/{version}/students/documents",tags=["Documents", "Admin"])

# Curriculum
app.include_router(subject.router, prefix=f"/api/{version}/curriculum/subjects",tags=["Subjects", "Admin"])
app.include_router(level_subject.router, prefix=f"/api/{version}/curriculum/level-subjects",tags=["Level Subjects", "Admin"])
app.include_router(student_subject.router, prefix=f"/api/{version}/curriculum/student-subjects",tags=["Student Subjects", "Admin"])
app.include_router(subject_educator.router, prefix=f"/api/{version}/curriculum/subject-educators",tags=["Subject Educator", "Admin"])

# Assessment
app.include_router(grade.router, prefix=f"/api/{version}/students/assessment/grades",tags=["Assessment", "Admin"])
app.include_router(total_grade.router, prefix=f"/api/{version}/students/assessment/total-grades",
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