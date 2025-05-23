from .common_test_imports import *

def test_model_structure_column_data_types(db_inspector):
    """Ensure all required columns are present and have the correct data type"""
    table ='educator_qualifications'
    columns = {col['name']: col for col in db_inspector.get_columns(table)}
    expected_types = {
        "id": UUID,
        "educator_id": UUID,
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
    table = 'educator_qualifications'
    columns = db_inspector.get_columns(table)

    expected_nullable = {
        "id": False,
        "educator_id": False,
        "created_at": False,
        "last_modified_at": False,
        "is_archived": False,
        "archived_at": True,
        "archived_by": True,
        "archive_reason": True,
        "created_by": False,
        "last_modified_by": False,
        "name": False,
        "description": True
    }
    for column in columns:
        column['name'] = column['name']
        assert column['nullable'] == expected_nullable.get(column['name']), \
            f"column {column['name']} is not nullable as expected"

def test_model_structure_default_values(db_inspector):
    """Ensure no default values are set at db level since they're handled
    at the application level"""
    table = 'educator_qualifications'
    columns = {col['name']: col for col in db_inspector.get_columns(table)}

    fields_without_defaults = [
        'id', 'created_at', 'created_by',
        'last_modified_at', 'last_modified_by',
        'is_archived', 'archived_at', 'archive_reason',
        'educator_id', 'name', 'description'
    ]

    for field in fields_without_defaults:
        assert columns[field]['default'] is None, f"{field} should not have a default value"


def test_model_structure_unique_constraints(db_inspector):
    """"Ensure unique constraints are correctly defined"""
    table = 'educator_qualifications'
    unique_constraints = db_inspector.get_unique_constraints(table)

    constraints_map = {
        constraint['name']: constraint['column_names']
        for constraint in unique_constraints
    }

    assert any(columns == ['name'] for columns in constraints_map.values()
               ), "name should have a unique constraint"


def test_model_structure_foreign_keys(db_inspector):
    """Ensure that column foreign keys are correctly defined"""
    table = 'educator_qualifications'
    foreign_keys = db_inspector.get_foreign_keys(table)
    educator_fk = next(
        (fk for fk in foreign_keys if fk['constrained_columns'] == ['educator_id']),
        None
        )

    assert educator_fk is not None, "Missing foreign key for educator_id"
    assert educator_fk['options']['ondelete'].upper() == 'CASCADE', \
        "educator_id should CASCADE on delete"


