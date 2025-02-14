from uuid import uuid4

from .common_test_imports import *


def test_column_data_types_in_access_level_changes(db_inspector):
    """Confirm all required columns are present and have the correct data type"""
    table ='access_level_changes'
    columns = {col['name']: col for col in db_inspector.get_columns(table)}
    expected_types = {
        "id": UUID,
        "staff_id": UUID,
        "previous_level": Enum,
        "new_level": Enum,
        "reason": String,
        "changed_at": DateTime,
        "changed_by": UUID
    }
    for column, expected_type in expected_types.items():
        assert isinstance(columns[column]['type'], expected_type), f"{column} has incorrect type"

    enum_checks = {
        'previous_level': AccessLevel,
        'new_level': AccessLevel
    }
    for column, enum_class in enum_checks.items():
        col_type = columns[column]['type']
        assert col_type.enum_class is enum_class or col_type.enums == [e.value for e in enum_class], f"{column} Enum mismatch"


def test_access_level_changes_nullable_constraints(db_inspector):
    table = 'access_level_changes'
    columns = db_inspector.get_columns(table)

    expected_nullable = {
        "id": False,
        "staff_id": False,
        "previous_level": False,
        "new_level": False,
        "reason": False,
        "changed_at": False,
        "changed_by": False,
    }
    for column in columns:
        column_name = column['name']
        assert column['nullable'] == expected_nullable.get(column_name), \
            f"column {column['name']} is not nullable as expected"


def test_access_level_changes_default_values(db_inspector):
    """Test that no default values are set at database level since they're handled
     at the application level"""
    table = 'access_level_changes'
    columns = {col['name']: col for col in db_inspector.get_columns(table)}

    fields_without_defaults = ['staff_id', 'previous_level', 'new_level', 'reason', 'changed_by']
    for field in fields_without_defaults:
        assert columns[field]['default'] is None, f"{field} should not have a default value"


def test_string_column_length_in_access_level_changes(db_inspector):
    """Test that string columns have correct max lengths"""
    table = 'access_level_changes'
    columns = {col['name']: col for col in db_inspector.get_columns(table)}

    assert columns['reason']['type'].length == 500


def test_unique_constraints_in_staff_departments(db_inspector):
    """Test unique constraint"""
    table = 'staff_departments'
    unique_constraints = db_inspector.get_unique_constraints(table)

    constraints_map = {
        constraint['name']: constraint['column_names']
        for constraint in unique_constraints
    }

    assert any(columns == ['name'] for columns in constraints_map.values()
               ), "name should have a unique constraint"
