from .common_test_imports import *


def test_model_structure_column_data_types(db_inspector):
    """Ensure all required columns are present and have the correct data type"""
    table = "student_class_transfers"
    columns = {col["name"]: col for col in db_inspector.get_columns(table)}
    expected_types = {
        "id": UUID,
        "student_id": UUID,
        "academic_year": Integer,
        "previous_class_id": UUID,
        "new_class_id": UUID,
        "reason": String,
        "status": Enum,
        "status_updated_by": UUID,
        "status_updated_at": DateTime,
        "rejection_reason": String,
        "created_at": DateTime,
        "last_modified_at": DateTime,
        "is_archived": Boolean,
        "archived_at": DateTime,
        "archive_reason": Enum,
        "created_by": UUID,
        "last_modified_by": UUID,
    }
    for column, expected_type in expected_types.items():
        assert isinstance(
            columns[column]["type"], expected_type
        ), f"{column} has incorrect type"

    enum_checks = {
        "archive_reason": ArchiveReason,
        "status": ApprovalStatus,
    }
    for column, enum_class in enum_checks.items():
        col_type = columns[column]["type"]
        assert col_type.enum_class is enum_class or col_type.enums == [
            e.value for e in enum_class
        ], f"{column} Enum mismatch"


def test_model_structure_nullable_constraints(db_inspector):
    """Ensure correctness of  nullable and not nullable fields"""
    table = "student_class_transfers"
    columns = db_inspector.get_columns(table)

    expected_nullable = {
        "id": False,
        "student_id": False,
        "academic_year": False,
        "previous_class_id": False,
        "new_class_id": False,
        "reason": False,
        "status": False,
        "status_updated_by": True,
        "status_updated_at": True,
        "rejection_reason": True,
        "created_at": False,
        "document_type": False,
        "file_url": False,
        "last_modified_at": False,
        "is_archived": False,
        "archived_at": True,
        "archived_by": True,
        "archive_reason": True,
        "created_by": False,
        "last_modified_by": False,
    }
    for column in columns:
        column["name"] = column["name"]
        assert column["nullable"] == expected_nullable.get(
            column["name"]
        ), f"column {column['name']} is not nullable as expected"


def test_model_structure_default_values(db_inspector):
    """Ensure no default values are set at db level since they're handled
    at the application level"""
    table = "student_class_transfers"
    columns = {col["name"]: col for col in db_inspector.get_columns(table)}

    fields_without_defaults = [
        "id",
        "student_id",
        "academic_year",
        "previous_class_id",
        "new_class_id",
        "reason",
        "status",
        "status_updated_by",
        "status_updated_at",
        "rejection_reason",
        "created_at",
        "last_modified_at",
        "is_archived",
        "archived_at",
        "archived_by",
        "archive_reason",
        "created_by",
        "last_modified_by",
    ]

    for field in fields_without_defaults:
        assert (
            columns[field]["default"] is None
        ), f"{field} should not have a default value"


def test_model_structure_string_column_length(db_inspector):
    """Ensure columns with String type have the correct max lengths"""
    table = "student_class_transfers"
    columns = {col["name"]: col for col in db_inspector.get_columns(table)}

    assert columns["reason"]["type"].length == 500
    assert columns["rejection_reason"]["type"].length == 500


def test_model_structure_foreign_keys(db_inspector):
    """Ensure that column foreign keys are correctly defined"""
    table = "student_class_transfers"
    foreign_keys = db_inspector.get_foreign_keys(table)
    student_fk = next(
        (fk for fk in foreign_keys if fk["constrained_columns"] == ["student_id"]), None
    )
    previous_class_fk = next(
        (
            fk
            for fk in foreign_keys
            if fk["constrained_columns"] == ["previous_class_id"]
        ),
        None,
    )
    new_class_fk = next(
        (fk for fk in foreign_keys if fk["constrained_columns"] == ["new_class_id"]),
        None,
    )
    status_updated_by_fk = next(
        (
            fk
            for fk in foreign_keys
            if fk["constrained_columns"] == ["status_updated_by"]
        ),
        None,
    )

    assert student_fk is not None, "Missing foreign key for student_id"
    assert (
        student_fk["options"]["ondelete"].upper() == "CASCADE"
    ), "student_id should CASCADE on delete"

    assert previous_class_fk is not None, "Missing foreign key for previous_class_id"
    assert (
        previous_class_fk["options"]["ondelete"].upper() == "RESTRICT"
    ), "previous_class_id should RESTRICT on delete"

    assert new_class_fk is not None, "Missing foreign key for new_class_id"
    assert (
        new_class_fk["options"]["ondelete"].upper() == "RESTRICT"
    ), "new_class_id should RESTRICT on delete"

    assert status_updated_by_fk is not None, "Missing foreign key for status_updated_by"
    assert (
        status_updated_by_fk["options"]["ondelete"].upper() == "RESTRICT"
    ), "status_updated_by should RESTRICT on delete"
