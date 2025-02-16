from .common_test_imports import *
def test_model_structure_column_data_types(db_inspector):
    """Confirm all required columns are present and have the correct data type for departments table"""
    table = 'student_departments'
    columns = {col['name']: col for col in db_inspector.get_columns(table)}
    expected_types = {
        "id": UUID,
        "name": String,
        "description": String,
        "mentor_id": UUID,
        "student_rep": UUID,
        "assistant_rep": UUID,
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

        "archive_reason": ArchiveReason
    }
    for column, enum_class in enum_checks.items():
        col_type = columns[column]['type']
        assert col_type.enum_class is enum_class or col_type.enums == [e.value for e in enum_class], f"{column} Enum mismatch"


def test_model_structure_nullable_constraints(db_inspector):
    """verify nullable and not nullable fields"""
    table = 'student_departments'
    columns = db_inspector.get_columns(table)

    expected_nullable = {
        "id": False,
        "name": False,
        "code": False,
        "mentor_id": True,
        "student_rep": True,
        "assistant_rep": True,
        "description": False,
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
        column_name = column['name']
        assert column['nullable'] == expected_nullable.get(column_name), \
            f"column {column_name} is not nullable as expected"


def test_model_structure_default_values(db_inspector):
    """Test that no default values are set at database level since they're handled by SQLAlchemy"""
    table = 'student_departments'
    columns = {col['name']: col for col in db_inspector.get_columns(table)}

    fields_without_defaults = [
        'id', 'created_at', 'created_by', 'student_rep', 'assistant_rep',
        'last_modified_at', 'last_modified_by','is_archived', 'archived_at',
        'archive_reason','name', 'description', 'mentor_id'
    ]

    for field in fields_without_defaults:
        assert columns[field]['default'] is None, f"{field} should not have a default value"


def test_model_structure_string_column_length(db_inspector):
    """Test that string columns have correct max lengths"""
    table = 'student_departments'
    columns = {col['name']: col for col in db_inspector.get_columns(table)}

    assert columns['name']['type'].length == 30
    assert columns['description']['type'].length == 500


def test_model_structure_unique_constraints(db_inspector):
    """Test unique constraint"""
    table = 'student_departments'
    unique_constraints = db_inspector.get_unique_constraints(table)

    constraints_map = {
        constraint['name']: constraint['column_names']
        for constraint in unique_constraints
    }

    assert any(columns == ['name'] for columns in constraints_map.values()
               ), "name should have a unique constraint"

