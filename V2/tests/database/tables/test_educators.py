from .common_test_imports import *

def test_model_structure_column_data_types(db_inspector):
    """Confirm all required columns  are present and have the correct data type"""
    table = 'educators'
    columns = {col['name']: col for col in db_inspector.get_columns(table)}
    expected_types = {
        "id": UUID
    }
    for column, expected_type in expected_types.items():
        assert isinstance(columns[column]['type'], expected_type), f"{column} has incorrect type"


def test_model_structure_nullable_constraints(db_inspector):
    """verify nullable and not nullable fields"""
    table = 'educators'
    columns = db_inspector.get_columns(table)

    expected_nullable = {
        "id": False,
    }
    for column in columns:
        column['name'] = column['name']
        assert column['nullable'] == expected_nullable.get(column['name']), \
            f"column {column['name']} is not nullable as expected"


def test_model_structure_default_values(db_inspector):
    """Test that no default values are set at database level since they're handled
    at the application level"""
    table = 'educators'
    columns = {col['name']: col for col in db_inspector.get_columns(table)}

    fields_without_defaults = [
        'id'
    ]

    for field in fields_without_defaults:
        assert columns[field]['default'] is None, f"{field} should not have a default value"

