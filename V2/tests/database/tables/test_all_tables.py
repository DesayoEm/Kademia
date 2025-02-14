from .common_test_imports import *

def test_model_structure(db_inspector):
    """Confirm the presence of all tables"""
    expected_tables = [
        "students", "parents", "staff", "educators", "operations", "support", "system", "student_documents", "staff_departments",
        "staff_roles", "departments", "access_level_changes", "classes","subjects", "grades", "total_grades",
        "student_subjects", "repetitions", "student_transfers", 'educator_qualifications' ]
    for table in expected_tables:
        assert db_inspector.has_table(table), f"Table '{table}' not found"
