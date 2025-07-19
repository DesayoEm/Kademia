from .common_test_imports import *

def test_model_structure_column_data_types(db_inspector):
    """Ensure all required columns are present and have the correct data type"""
    table = 'academic_levels'
    columns = {col['name']: col for col in db_inspector.get_columns(table)}
    expected_types = {
        "id": UUID,
        "name": String,
        "description": String,
        "order": Integer,
        "created_at": DateTime,
        "last_modified_at": DateTime,
        "is_archived": Boolean,
        "archived_at": DateTime,
        "archive_reason": Enum,
        "archived_by": UUID,
        "created_by": UUID,
        "last_modified_by": UUID
    }
    for column,expected_type in expected_types.items():
        assert isinstance(columns[column]['type'], expected_type), f"{column} has incorrect type"


def test_model_structure_nullable_constraints(db_inspector):
    """Ensure correctness of  nullable and not nullable fields"""
    table = 'academic_levels'
    columns = db_inspector.get_columns(table)
    expected_nullable = {
        "id": False,
        "name": False,
        "description": False,
        "order": False,
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
    """Ensure no default values are set at db level since they're handled
   at the application level"""
    table = 'academic_levels'
    columns = {col['name']: col for col in db_inspector.get_columns(table)}
    fields_without_defaults = [
        'id', 'created_at', 'created_by','last_modified_at', 'last_modified_by',
        'is_archived', 'archived_at','archive_reason','name', 'description',
        'order'
    ]
    for field in fields_without_defaults:
        assert columns[field]['default'] is None, f"{field} should not have a default value"


def test_model_structure_string_column_length(db_inspector):
    """Ensure columns with String type have the correct max lengths"""
    table = 'academic_levels'
    columns = {col['name']: col for col in db_inspector.get_columns(table)}

    assert columns['name']['type'].length == 30
    assert columns['description']['type'].length == 500



def test_model_structure_unique_constraints(db_inspector):
    """Ensure unique constraints are correctly defined"""
    table = 'academic_levels'
    unique_constraints = db_inspector.get_unique_constraints(table)

    constraints_map = {
        constraint['name']: constraint['column_names']
        for constraint in unique_constraints
    }

    assert any(columns == ['name'] for columns in constraints_map.values()
               ), "name should have a unique constraint"
    assert any(columns == ['order'] for columns in constraints_map.values()
               ), "name should have a unique constraint"




def test_model_structure_foreign_keys(db_inspector):
    """Ensure that column foreign keys are correctly defined"""
    table = 'academic_level_subjects'
    foreign_keys = db_inspector.get_foreign_keys(table)
    level_fk = next(
        (fk for fk in foreign_keys if fk['constrained_columns'] == ['level_id']),
        None
    )
    subject_fk = next(
        (fk for fk in foreign_keys if fk['constrained_columns'] == ['subject_id']),
        None
    )
    educator_fk = next(
        (fk for fk in foreign_keys if fk['constrained_columns'] == ['educator_id']),
        None
    )
    assert level_fk is not None, "Missing foreign key for level_id"

    assert level_fk['options']['ondelete'].upper() == 'RESTRICT', \
        "level_id should RESTRICT on delete"

    assert subject_fk is not None, "Missing foreign key for subject_id"
    assert subject_fk['options']['ondelete'].upper() == 'RESTRICT', \
        "subject_id should RESTRICT on delete"

    assert educator_fk is not None, "Missing foreign key for educator_id"
    assert subject_fk['options']['ondelete'].upper() == 'RESTRICT', \
        "educator_id should RESTRICT on delete"



