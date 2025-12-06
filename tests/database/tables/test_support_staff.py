from .common_test_imports import *


def test_model_structure_column_data_types(db_inspector):
    """Ensure all required columns are present and have the correct data type"""
    table = "support_staff"
    columns = {col["name"]: col for col in db_inspector.get_columns(table)}
    expected_types = {"id": UUID}
    for column, expected_type in expected_types.items():
        assert isinstance(
            columns[column]["type"], expected_type
        ), f"{column} has incorrect type"


def test_model_structure_nullable_constraints(db_inspector):
    """Ensure correctness of  nullable and not nullable fields"""
    table = "support_staff"
    columns = db_inspector.get_columns(table)

    expected_nullable = {
        "id": False,
    }
    for column in columns:
        column["name"] = column["name"]
        assert column["nullable"] == expected_nullable.get(
            column["name"]
        ), f"column {column['name']} is not nullable as expected"


def test_model_structure_default_values(db_inspector):
    """Ensure no default values are set at db level since they're handled
    at the application level"""
    table = "support_staff"
    columns = {col["name"]: col for col in db_inspector.get_columns(table)}

    fields_without_defaults = ["id"]

    for field in fields_without_defaults:
        assert (
            columns[field]["default"] is None
        ), f"{field} should not have a default value"


def test_model_structure_foreign_keys(db_inspector):
    """Ensure that column foreign keys are correctly defined"""
    table = "support_staff"
    foreign_keys = db_inspector.get_foreign_keys(table)
    id_fk = next(
        (fk for fk in foreign_keys if fk["constrained_columns"] == ["id"]), None
    )
    assert id_fk is not None, "Missing foreign key for id"
