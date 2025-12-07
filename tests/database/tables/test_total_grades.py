from .common_test_imports import *


def test_model_structure_column_data_types(db_inspector):
    """Confirm all required columns are present and have the correct data type"""
    table = "total_grades"
    columns = {col["name"]: col for col in db_inspector.get_columns(table)}
    expected_types = {
        "id": UUID,
        "student_id": UUID,
        "subject_id": UUID,
        "academic_year": String,
        "semester": Enum,
        "total_score": Integer,
        "rank": Integer,
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

    enum_checks = {"archive_reason": ArchiveReason, "semester": Semester}
    for column, enum_class in enum_checks.items():
        col_type = columns[column]["type"]
        assert col_type.enum_class is enum_class or col_type.enums == [
            e.value for e in enum_class
        ], f"{column} Enum mismatch"


def test_model_structure_nullable_constraints(db_inspector):
    """verify nullable and not nullable fields"""
    table = "total_grades"
    columns = db_inspector.get_columns(table)

    expected_nullable = {
        "id": False,
        "student_id": False,
        "subject_id": False,
        "academic_year": False,
        "semester": False,
        "total_score": False,
        "rank": True,
        "created_at": False,
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
    """Test that no default values are set at db level since they're handled
    at the application level"""
    table = "total_grades"
    columns = {col["name"]: col for col in db_inspector.get_columns(table)}

    fields_without_defaults = [
        "id",
        "created_at",
        "created_by",
        "last_modified_at",
        "last_modified_by",
        "is_archived",
        "archived_at",
        "archive_reason",
        "student_id",
        "subject_id",
        "academic_year",
        "semester",
        "total_score",
        "rank",
    ]

    for field in fields_without_defaults:
        assert (
            columns[field]["default"] is None
        ), f"{field} should not have a default value"


def test_model_structure_string_column_length(db_inspector):
    """Test that string columns have correct max lengths"""
    table = "total_grades"
    columns = {col["name"]: col for col in db_inspector.get_columns(table)}

    assert columns["academic_year"]["type"].length == 9


def test_model_structure_foreign_keys(db_inspector):
    """Ensure that column foreign keys are correctly defined"""
    table = "grades"
    foreign_keys = db_inspector.get_foreign_keys(table)
    student_fk = next(
        (fk for fk in foreign_keys if fk["constrained_columns"] == ["student_id"]), None
    )
    subject_fk = next(
        (fk for fk in foreign_keys if fk["constrained_columns"] == ["subject_id"]), None
    )

    assert student_fk is not None, "Missing foreign key for student_id"
    assert (
        student_fk["options"]["ondelete"].upper() == "CASCADE"
    ), "student_id should CASCADE on delete"

    assert subject_fk is not None, "Missing foreign key for subject_id"
    assert (
        subject_fk["options"]["ondelete"].upper() == "RESTRICT"
    ), "subject_id should RESTRICT on delete"
