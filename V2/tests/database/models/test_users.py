from V2.app.database.models.common_imports import Base

def test_model_structure(db_inspector):
    """Confirm the presence of all required tables"""
    expected_tables = [
        "students", "parents", "staff", "educator", "operations", "support", "system", "student_documents", "staff_departments",
        "staff_roles", "departments", "access_level_changes", "classes","subjects", "grades", "total_grades",
        "student_subjects", "repetitions", "student_transfers"  ]
    for table in expected_tables:
        assert db_inspector.has_table(table), f"Table '{table}' not found"

