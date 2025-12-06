from .common_test_imports import *


def test_model_structure_table_exists(db_inspector):
    """Confirm the presence of all tables"""
    expected_tables = [
        "students",
        "guardians",
        "staff",
        "educators",
        "admin_staff",
        "support_staff",
        "system",
        "student_documents",
        "staff_departments",
        "staff_roles",
        "student_departments",
        "access_level_changes",
        "classes",
        "subjects",
        "grades",
        "total_grades",
        "student_subjects",
        "repetitions",
        "student_department_transfers",
        "educator_qualifications",
        "academic_level_subjects",
        "academic_levels",
        "subject_educators",
        "student_class_transfers",
        "student_awards",
    ]

    for table in expected_tables:
        assert db_inspector.has_table(table), f"Table '{table}' not found"
