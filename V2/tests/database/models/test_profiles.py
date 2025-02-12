from V2.app.database.models import AccessLevelChanges
from V2.app.database.models.common_imports import Base
from V2.app.database.models.data_enums import *
from V2.app.database.models.profiles import Students
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, Enum, Integer, Boolean, DateTime, Date

def test_model_structure(db_inspector):
    """Confirm the presence of all required tables"""
    expected_tables = [
        "students", "parents", "staff", "educator", "operations", "support", "system", "student_documents", "staff_departments",
        "staff_roles", "departments", "access_level_changes", "classes","subjects", "grades", "total_grades",
        "student_subjects", "repetitions", "student_transfers", 'educator_qualifications' ]
    for table in expected_tables:
        assert db_inspector.has_table(table), f"Table '{table}' not found"


def test_column_data_types(db_inspector):
    """Confirm the presence of all required columns and  in students table are present
    and have the correct data type"""
    table = 'students'
    columns = {col['name']: col for col in db_inspector.get_columns(table)}

    assert isinstance (columns['id']['type'],UUID)
    assert isinstance(columns['password_hash']['type'],String)
    assert isinstance(columns['first_name']['type'],String)
    assert isinstance(columns['last_name']['type'],String)
    assert isinstance(columns['gender']['type'],Enum)
    assert isinstance(columns['gender']['type'], Enum) and columns['gender']['type'].enum_class is Gender
    assert isinstance(columns['is_active']['type'],Boolean)
    assert isinstance(columns['last_login']['type'],DateTime)
    assert isinstance(columns['created_at']['type'],DateTime)
    assert isinstance(columns['last_modified_at']['type'],DateTime)
    assert isinstance(columns['is_archived']['type'],Boolean)
    assert isinstance(columns['archived_at']['type'],DateTime)
    assert isinstance(columns['archive_reason']['type'], Enum) and columns['archive_reason']['type'].enum_class is ArchiveReason
    assert isinstance (columns['created_by']['type'],UUID)
    assert isinstance (columns['last_modified_by']['type'],UUID)
    assert isinstance(columns['date_of_birth']['type'],Date)
    assert isinstance(columns['access_level']['type'], Enum) and columns['access_level']['type'].enum_class is AccessLevel
    assert isinstance(columns['user_type']['type'], Enum) and columns['user_type']['type'].enum_class is UserType
    assert isinstance(columns['student_id']['type'],String)
    assert isinstance(columns['image_url']['type'],String)
    assert isinstance (columns['class_id']['type'],UUID)
    assert isinstance (columns['department_id']['type'],UUID)
    assert isinstance (columns['parent_id']['type'],UUID)
    assert isinstance(columns['is_repeating']['type'],Boolean)
    assert isinstance(columns['admission_date']['type'],Date)
    assert isinstance(columns['leaving_date']['type'],Date)
    assert isinstance(columns['is_graduated']['type'],Boolean)
    assert isinstance(columns['graduation_date']['type'],Date)
    assert isinstance(columns['is_enrolled']['type'],Boolean)






