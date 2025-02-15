from .common_test_imports import *

def test_model_structure_column_data_types(db_inspector):
    """Confirm all required columns are present and have the correct data type"""
    table ='subjects'
    columns = {col['name']: col for col in db_inspector.get_columns(table)}
    expected_types = {
        "id": UUID,
        "name": String,
        "class_level": Enum,
        "group": Enum,
        "syllabus_url": String,
        "educator_id": UUID,
        "is_elective": Boolean,
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
        'class_level': ClassLevel,
        'group': SubjectGroup
    }
    for column, enum_class in enum_checks.items():
        col_type = columns[column]['type']
        assert col_type.enum_class is enum_class or col_type.enums == [e.value for e in enum_class], f"{column} Enum mismatch"

def test_model_structure_nullable_constraints(db_inspector):
    """verify nullable and not nullable fields"""
    table = 'subjects'
    columns = db_inspector.get_columns(table)

    expected_nullable = {
        "id": False,
        "name": False,
        "class_level": False,
        "group": False,
        "syllabus_url": True,
        "educator_id": False,
        "is_elective": False,
        "created_at": False,
        "last_modified_at": False,
        "is_archived": False,
        "archived_at": False,
        "archived_by": False,
        "archive_reason": False,
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
    table = 'subjects'
    columns = {col['name']: col for col in db_inspector.get_columns(table)}

    fields_without_defaults = [
        'id', "name","class_level","is_elective","educator_id", "syllabus_url",
        "is_archived", "archived_at","archived_by", "archive_reason", "created_by","last_modified_by"
    ]

    for field in fields_without_defaults:
        assert columns[field]['default'] is None, f"{field} should not have a default value"


def test_model_structure_string_column_length(db_inspector):
    """Test that string columns have correct max lengths"""
    table = 'subjects'
    columns = {col['name']: col for col in db_inspector.get_columns(table)}

    assert columns['name']['type'].length == 30
    assert columns['syllabus_url']['type'].length == 225


