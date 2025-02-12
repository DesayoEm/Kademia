from V2.app.database.models import AccessLevelChanges
from V2.app.database.models.common_imports import Base
from V2.app.database.models.data_enums import *
from V2.app.database.models.profiles import Students
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, Enum, Integer, Boolean, DateTime, Date, Float


def test_model_structure(db_inspector):
    """Confirm the presence of all required tables"""
    expected_tables = [
        "students", "parents", "staff", "educator", "operations", "support", "system", "student_documents", "staff_departments",
        "staff_roles", "departments", "access_level_changes", "classes","subjects", "grades", "total_grades",
        "student_subjects", "repetitions", "student_transfers", 'educator_qualifications' ]
    for table in expected_tables:
        assert db_inspector.has_table(table), f"Table '{table}' not found"

