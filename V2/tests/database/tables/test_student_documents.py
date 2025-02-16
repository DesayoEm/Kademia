from .common_test_imports import *


def test_model_structure_column_data_types(db_inspector):
    """Confirm all required columns are present and have the correct data type"""
    table ='student_documents'
    columns = {col['name']: col for col in db_inspector.get_columns(table)}
    expected_types = {
        "id": UUID,
        "owner_id": UUID,
        "title": String,
        "academic_year": Integer,
        "document_type": Enum,
        "file_url": String,
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
        'document_type': DocumentType,
    }
    for column, enum_class in enum_checks.items():
        col_type = columns[column]['type']
        assert col_type.enum_class is enum_class or col_type.enums == [e.value for e in enum_class], f"{column} Enum mismatch"



def test_model_structure_nullable_constraints(db_inspector):
    """verify nullable and not nullable fields"""
    table = 'student_documents'
    columns = db_inspector.get_columns(table)

    expected_nullable = {
        "id": False,
        "owner_id": False,
        "title": False,
        "created_at": False,
        "academic_year": False,
        "document_type": False,
        "file_url": False,
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
    """Test that no default values are set at database level since they're handled
    at the application level"""
    table = 'student_documents'
    columns = {col['name']: col for col in db_inspector.get_columns(table)}

    fields_without_defaults = [
        'id', "owner_id","title","academic_year", "document_type","file_url",
        "is_archived", "archived_at","archived_by", "archive_reason", "created_by","last_modified_by"
    ]

    for field in fields_without_defaults:
        assert columns[field]['default'] is None, f"{field} should not have a default value"


def test_model_structure_string_column_length(db_inspector):
    """Test that string columns have correct max lengths"""
    table = 'student_documents'
    columns = {col['name']: col for col in db_inspector.get_columns(table)}

    assert columns['title']['type'].length == 50
    assert columns['file_url']['type'].length == 225

