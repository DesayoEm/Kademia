from .common_test_imports import *


def test_model_structure_column_data_types(db_inspector):
    """Ensure all required columns are present and have the correct data type"""
    table = 'staff_roles'
    columns = {col['name']: col for col in db_inspector.get_columns(table)}
    expected_types = {
        "id": UUID,
        "name": String,
        "description": String,
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
    """Ensure correctness of  nullable and not nullable fields"""
    table = 'staff_roles'
    columns = db_inspector.get_columns(table)

    expected_nullable = {
        "id": False,
        "name": False,
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
        column['name'] = column['name']
        assert column['nullable'] == expected_nullable.get(column['name']), \
            f"column {column['name']} is not nullable as expected"


def test_model_structure_default_values(db_inspector):
    """Ensure no default values are set at db level since they're handled
    at the application level"""
    table = 'staff_roles'
    columns = {col['name']: col for col in db_inspector.get_columns(table)}

    fields_without_defaults = [
        'id', "name", "description","created_at","last_modified_at",
        "is_archived", "archived_at","archived_by", "archive_reason", "created_by","last_modified_by"
    ]

    for field in fields_without_defaults:
        assert columns[field]['default'] is None, f"{field} should not have a default value"


def test_model_structure_string_column_length(db_inspector):
    """Ensure columns with String type have the correct max lengths"""
    table = 'staff_roles'
    columns = {col['name']: col for col in db_inspector.get_columns(table)}

    assert columns['name']['type'].length == 100
    assert columns['description']['type'].length == 500


def test_model_structure_unique_constraints(db_inspector):
    """Ensure unique constraints are correctly defined"""
    table = 'staff_roles'
    unique_constraints = db_inspector.get_unique_constraints(table)

    constraints_map = {
        constraint['name']: constraint['column_names']
        for constraint in unique_constraints
    }
    assert any(columns == ['name'] for columns in constraints_map.values()
               ), "name should have a unique constraint"


