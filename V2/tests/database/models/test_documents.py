from common_test_imports import *


def test_column_data_types_in_student_documents(db_inspector):
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
