from .common_test_imports import *

def test_model_structure_column_data_types(db_inspector):
    """Confirm all required columns  are present and have the correct data type"""
    table = 'guardians'
    columns = {col['name']: col for col in db_inspector.get_columns(table)}
    expected_types = {
        "id": UUID,
        "password_hash": String,
        "first_name": String,
        "last_name": String,
        "gender": Enum,
        "last_login": DateTime,
        "created_at": DateTime,
        "last_modified_at": DateTime,
        "is_archived": Boolean,
        "archived_at": DateTime,
        "archive_reason": Enum,
        "created_by": UUID,
        "last_modified_by": UUID,
        "access_level": Enum,
        "user_type": Enum,
        "image_url": String,
        "email_address": String,
        "address": String,
        "phone": String,

    }

    for column, expected_type in expected_types.items():
        assert isinstance(columns[column]['type'], expected_type), f"{column} has incorrect type"

    enum_checks = {
        "gender": Gender,
        "archive_reason": ArchiveReason,
        "access_level": AccessLevel,
        "user_type": UserType,

    }

    for column, enum_class in enum_checks.items():
        col_type = columns[column]['type']
        assert isinstance(col_type, Enum), f"{column} should be Enum"
        assert col_type.enum_class is enum_class or col_type.enums == [e.value for e in enum_class], f"{column} Enum mismatch"


def test_model_structure_nullable_constraints(db_inspector):
    """verify nullable and not nullable fields"""
    table = 'guardians'
    columns = db_inspector.get_columns(table)

    expected_nullable = {
        "id": False,
        "password_hash": False,
        "first_name": False,
        "last_name": False,
        "gender": False,
        "is_active": False,
        "last_login": True,
        "created_at": False,
        "last_modified_at": False,
        "is_archived": False,
        "archived_at": True,
        "archived_by": True,
        "archive_reason": True,
        "created_by": False,
        "last_modified_by": False,
        "access_level": False,
        "user_type": False,
        "image_url": True,
        "email_address": False,
        "address": False,
        "phone": False,
        "deletion_eligible":False
    }
    for column in columns:
        column['name'] = column['name']
        assert column['nullable'] == expected_nullable.get(column['name']), \
            f"column {column['name']} is not nullable as expected"

def test_model_structure_default_values(db_inspector):
    """Test that no default values are set at database level since they're handled
    at the application level"""
    table = 'guardians'
    columns = {col['name']: col for col in db_inspector.get_columns(table)}

    fields_without_defaults = [
        'id', "password_hash", "first_name", "last_name", "gender",
        "last_login","created_at","last_modified_at","is_archived", "archived_at",
        "archived_by", "archive_reason", "created_by","last_modified_by", "access_level","user_type",
        "image_url","email_address","address","phone","deletion_eligible"
    ]

    for field in fields_without_defaults:
        assert columns[field]['default'] is None, f"{field} should not have a default value"


def test_model_structure_string_column_length(db_inspector):
    """Test that columns with String type have the correct max lengths"""
    table = 'guardians'
    columns = {col['name']: col for col in db_inspector.get_columns(table)}

    assert columns['password_hash']['type'].length == 300
    assert columns['first_name']['type'].length == 30
    assert columns['last_name']['type'].length == 30
    assert columns['image_url']['type'].length == 225
    assert columns['email_address']['type'].length == 255
    assert columns['address']['type'].length == 500
    assert columns['phone']['type'].length == 14


def test_model_structure_unique_constraints(db_inspector):
    """Test unique constraint"""
    table = 'guardians'
    unique_constraints = db_inspector.get_unique_constraints(table)

    constraints_map = {
        constraint['name']: constraint['column_names']
        for constraint in unique_constraints
    }

    assert any(columns == ['email_address'] for columns in constraints_map.values()
               ), "email_service address should have a unique constraint"
    assert any(columns == ['phone'] for columns in constraints_map.values()
               ), "phone should have a unique constraint"




