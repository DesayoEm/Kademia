from .common_test_imports import *


def test_column_data_types_in_student_subjects(db_inspector):
    """Confirm all required columns are present and have the correct data type"""
    table = 'student_subjects'
    columns = {col['name']: col for col in db_inspector.get_columns(table)}
    expected_types = {
        "id": UUID,
        "student_id": UUID,
        "subject_id": UUID,
        "academic_year": String,
        "term": Enum,
        "created_at": DateTime,
        "last_modified_at": DateTime,
        "is_archived": Boolean,
        "archived_at": DateTime,
        "archive_reason": Enum,
        "created_by": UUID,
        "last_modified_by": UUID

    }
    for column, expected_type in expected_types.items():
        assert isinstance(columns[column]['type'], expected_type), f"{column} has incorrect type"

    enum_checks = {
        "archive_reason": ArchiveReason,
        'term': Term
    }
    for column, enum_class in enum_checks.items():
        col_type = columns[column]['type']
        assert col_type.enum_class is enum_class or col_type.enums == [e.value for e in enum_class], f"{column} Enum mismatch"

def student_subjects_nullable_constraints(db_inspector):
    """verify nullable and not nullable fields"""
    table = 'student_subjects'
    columns = db_inspector.get_columns(table)

    expected_nullable = {
        "id": False,
        "student_id": False,
        "subject_id": False,
        "academic_year": False,
        "term": False,
        "is_active": False,
        "created_at": False,
        "last_modified_at": False,
        "is_archived": False,
        "archived_at": False,
        "archived_by": False,
        "archive_reason": False,
        "created_by": False,
        "last_modified_by": False
    }
    for column in columns:
        column['name'] = column['name']
        assert column['nullable'] == expected_nullable.get(column['name']), \
            f"column {column['name']} is not nullable as expected"


def test_student_subjects_default_values(db_inspector):
    """Test that no default values are set at database level since they're handled
    at the application level"""
    table = 'student_subjects'
    columns = {col['name']: col for col in db_inspector.get_columns(table)}

    fields_without_defaults = [
        'id', "student_id","subject_id","academic_year", "term","is_active",
        "is_archived", "archived_at","archived_by", "archive_reason", "created_by","last_modified_by"
    ]

    for field in fields_without_defaults:
        assert columns[field]['default'] is None, f"{field} should not have a default value"


def test_string_column_length_in_student_subjects(db_inspector):
    """Test that string columns have correct max lengths"""
    table = 'student_subjects'
    columns = {col['name']: col for col in db_inspector.get_columns(table)}

    assert columns['academic_year']['type'].length == 9


