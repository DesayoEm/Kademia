from .common_test_imports import *

def test_model_structure_column_data_types(db_inspector):
    """Confirm all required columns are present and have the correct data type"""
    table ='student_repetitions'
    columns = {col['name']: col for col in db_inspector.get_columns(table)}
    expected_types = {
        "id": UUID,
        "student_id": UUID,
        "academic_year": Integer,
        "previous_level_id": UUID,
        "new_level_id": UUID,
        "previous_class_id": UUID,
        "new_class_id": UUID,
        "reason": String,
        "status": Enum,
        "status_updated_by": UUID,
        "status_updated_at": DateTime,
        "rejection_reason": String,
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
        "status": ApprovalStatus,

    }
    for column, enum_class in enum_checks.items():
        col_type = columns[column]['type']
        assert col_type.enum_class is enum_class or col_type.enums == [e.value for e in enum_class], f"{column} Enum mismatch"

def test_model_structure_nullable_constraints(db_inspector):
    """verify nullable and not nullable fields"""
    table = 'student_repetitions'
    columns = db_inspector.get_columns(table)

    expected_nullable = {
        "id": False,
        "student_id": False,
        "academic_year": False,
        "previous_level_id": False,
        "new_level_id": False,
        "previous_class_id": False,
        "new_class_id": False,
        "reason": False,
        "status": False,
        "status_updated_by": True,
        "status_updated_at": True,
        "rejection_reason": True,
        "created_at": False,
        "last_modified_at": False,
        "is_archived": False,
        "archived_at": True,
        "archived_by": True,
        "archive_reason": True,
        "created_by": False,
        "last_modified_by": False
    }
    for column in columns:
        column['name'] = column['name']
        assert column['nullable'] == expected_nullable.get(column['name']), \
            f"column {column['name']} is not nullable as expected"


def test_model_structure_default_values(db_inspector):
    """Test that no default values are set at database level since they're handled
    at the application level"""
    table = 'student_repetitions'
    columns = {col['name']: col for col in db_inspector.get_columns(table)}

    fields_without_defaults = [
        'id', "student_id", "academic_year", "previous_level_id", "new_level_id",
        "previous_class_id","new_class_id","reason","status","status_updated_by","status_updated_at",
        "rejection_reason","created_at","last_modified_at","is_archived", "archived_at",
        "archived_by", "archive_reason", "created_by","last_modified_by"
    ]

    for field in fields_without_defaults:
        assert columns[field]['default'] is None, f"{field} should not have a default value"


def test_model_structure_string_column_length(db_inspector):
    """Test that string columns have correct max lengths"""
    table = 'student_repetitions'
    columns = {col['name']: col for col in db_inspector.get_columns(table)}

    assert columns['reason']['type'].length == 500
    assert columns['rejection_reason']['type'].length == 500
