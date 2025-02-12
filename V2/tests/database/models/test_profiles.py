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


def test_column_data_types_in_students(db_inspector):
    """Confirm the presence of all required columns and  in students table are present
    and have the correct data type"""
    table = 'students'
    columns = {col['name']: col for col in db_inspector.get_columns(table)}
    expected_types = {
        "id": UUID,
        "password_hash": String,
        "first_name": String,
        "last_name": String,
        "gender": Enum,
        "is_active": Boolean,
        "last_login": DateTime,
        "created_at": DateTime,
        "last_modified_at": DateTime,
        "is_archived": Boolean,
        "archived_at": DateTime,
        "archive_reason": Enum,
        "created_by": UUID,
        "last_modified_by": UUID,
        "student_id": String,
        "date_of_birth": Date,
        "access_level": Enum,
        "user_type": Enum,
        "image_url": String,
        "class_id": UUID,
        "department_id": UUID,
        "parent_id": UUID,
        "is_repeating": Boolean,
        "admission_date": Date,
        "leaving_date": Date,
        "is_graduated": Boolean,
        "graduation_date": Date,
        "is_enrolled": Boolean,
    }

    for column, expected_type in expected_types.items():
        assert isinstance(columns[column]['type'], expected_type), f"{column} has incorrect type"

    enum_checks = {
        "gender": Gender,
        "archive_reason": ArchiveReason,
        "access_level": AccessLevel,
        "user_type": UserType
    }

    for column, enum_class in enum_checks.items():
        col_type = columns[column]['type']
        assert isinstance(col_type, Enum), f"{column} should be Enum"
        assert col_type.enum_class is enum_class or col_type.enums == [e.value for e in enum_class], f"{column} Enum mismatch"



def test_column_data_types_in_parents(db_inspector):
    """Confirm the presence of all required columns and  in parents table are present
    and have the correct data type"""
    table = 'parents'
    columns = {col['name']: col for col in db_inspector.get_columns(table)}
    expected_types = {
        "id": UUID,
        "password_hash": String,
        "first_name": String,
        "last_name": String,
        "gender": Enum,
        "is_active": Boolean,
        "last_login": DateTime,
        "created_at": DateTime,
        "last_modified_at": DateTime,
        "is_archived": Boolean,
        "archived_at": DateTime,
        "archive_reason": Enum,
        "created_by": UUID,
        "last_modified_by": UUID,
        "access_level": Enum,
        "user_type": Enum,
        "image_url": String,
        "email_address": String,
        "address": String,
        "phone": String,
    }

    for column, expected_type in expected_types.items():
        assert isinstance(columns[column]['type'], expected_type), f"{column} has incorrect type"

    enum_checks = {
        "gender": Gender,
        "archive_reason": ArchiveReason,
        "access_level": AccessLevel,
        "user_type": UserType
    }

    for column, enum_class in enum_checks.items():
        col_type = columns[column]['type']
        assert isinstance(col_type, Enum), f"{column} should be Enum"
        assert col_type.enum_class is enum_class or col_type.enums == [e.value for e in enum_class], f"{column} Enum mismatch"



def test_column_data_types_in_staff(db_inspector):
    """Confirm the presence of all required columns and  in parents table are present
    and have the correct data type"""
    table = 'staff'
    columns = {col['name']: col for col in db_inspector.get_columns(table)}
    expected_types = {
        "id": UUID,
        "password_hash": String,
        "first_name": String,
        "last_name": String,
        "gender": Enum,
        "is_active": Boolean,
        "last_login": DateTime,
        "created_at": DateTime,
        "last_modified_at": DateTime,
        "is_archived": Boolean,
        "archived_at": DateTime,
        "archive_reason": Enum,
        "created_by": UUID,
        "last_modified_by": UUID,
        "access_level": Enum,
        "user_type": Enum,
        "staff_type": Enum,
        "image_url": String,
        "email_address": String,
        "address": String,
        "phone": String,
        "department_id": UUID,
        "role_id": UUID,
        "date_joined": Date,
        "date_left": Date,
    }

    for column, expected_type in expected_types.items():
        assert isinstance(columns[column]['type'], expected_type), f"{column} has incorrect type"

    enum_checks = {
        "gender": Gender,
        "archive_reason": ArchiveReason,
        "access_level": AccessLevel,
        "user_type": UserType,
        "staff_type": StaffType
    }

    for column, enum_class in enum_checks.items():
        col_type = columns[column]['type']
        assert isinstance(col_type, Enum), f"{column} should be Enum"
        assert col_type.enum_class is enum_class or col_type.enums == [e.value for e in enum_class], f"{column} Enum mismatch"


def test_column_data_types_in_educator(db_inspector):
    """Confirm the presence of all required columns and  in parents table are present
    and have the correct data type"""
    table = 'educator'
    columns = {col['name']: col for col in db_inspector.get_columns(table)}
    expected_types = {
        "id": UUID
    }
    for column, expected_type in expected_types.items():
        assert isinstance(columns[column]['type'], expected_type), f"{column} has incorrect type"

def test_column_data_types_in_operations(db_inspector):
    """Confirm the presence of all required columns and  in parents table are present
    and have the correct data type"""
    table = 'operations'
    columns = {col['name']: col for col in db_inspector.get_columns(table)}
    expected_types = {
        "id": UUID
    }
    for column, expected_type in expected_types.items():
        assert isinstance(columns[column]['type'], expected_type), f"{column} has incorrect type"


def test_column_data_types_in_support(db_inspector):
    """Confirm the presence of all required columns and  in parents table are present
    and have the correct data type"""
    table = 'support'
    columns = {col['name']: col for col in db_inspector.get_columns(table)}
    expected_types = {
        "id": UUID
    }
    for column, expected_type in expected_types.items():
        assert isinstance(columns[column]['type'], expected_type), f"{column} has incorrect type"


def test_column_data_types_in_system(db_inspector):
    """Confirm the presence of all required columns and  in parents table are present
    and have the correct data type"""
    table = 'system'
    columns = {col['name']: col for col in db_inspector.get_columns(table)}
    expected_types = {
        "id": UUID
    }
    for column, expected_type in expected_types.items():
        assert isinstance(columns[column]['type'], expected_type), f"{column} has incorrect type"