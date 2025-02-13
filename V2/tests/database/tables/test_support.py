from .common_test_imports import *

def test_column_data_types_in_support(db_inspector):
    """Confirm all required columns  are present and have the correct data type"""
    table = 'support'
    columns = {col['name']: col for col in db_inspector.get_columns(table)}
    expected_types = {
        "id": UUID
    }
    for column, expected_type in expected_types.items():
        assert isinstance(columns[column]['type'], expected_type), f"{column} has incorrect type"



def test_support_nullable_constraints(db_inspector):
    """verify nullable and not nullable fields"""
    table = 'support'
    columns = db_inspector.get_columns(table)

    expected_nullable = {
        "id": False,
    }
    for column in columns:
        column['name'] = column['name']
        assert column['nullable'] == expected_nullable.get(column['name']), \
            f"column {column['name']} is not nullable as expected"

