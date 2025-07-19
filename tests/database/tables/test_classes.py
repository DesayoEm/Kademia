from .common_test_imports import *

def test_model_structure_column_data_types(db_inspector):
    """Ensure all required columns are present and have the correct data type"""
    table = 'classes'
    columns = {col['name']: col for col in db_inspector.get_columns(table)}
    expected_types = {
        "id": UUID,
        "level_id": UUID,
        "code": Enum,
        "order": Integer,
        "mentor_id": UUID,
        "student_rep_id": UUID,
        "assistant_rep_id": UUID,
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
        "code": ClassCode,
        "archive_reason": ArchiveReason
    }
    for column, enum_class in enum_checks.items():
        col_type = columns[column]['type']
        assert col_type.enum_class is enum_class or col_type.enums == [e.value for e in enum_class], f"{column} Enum mismatch"



def test_model_structure_nullable_constraints(db_inspector):
    """Ensure correctness of  nullable and not nullable fields"""
    table = 'classes'
    columns = db_inspector.get_columns(table)

    expected_nullable = {
        "id": False,
        "level_id": False,
        "code": False,
        "order": True,
        "mentor_id": True,
        "student_rep_id": True,
        "assistant_rep_id": True,
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
        column['name'] = column['name']
        assert column['nullable'] == expected_nullable.get(column['name']), \
            f"column {column['name']} is not nullable as expected"


def test_model_structure_default_values(db_inspector):
    """Ensure no default values are set at db level since they're handled
   at the application level"""
    table = 'classes'
    columns = {col['name']: col for col in db_inspector.get_columns(table)}

    fields_without_defaults = [
        'id', 'created_at', 'created_by',
        'last_modified_at', 'last_modified_by',
        'is_archived', 'archived_at', 'archive_reason',
        'code', 'level_id', 'mentor_id',
        'student_rep_id', 'assistant_rep_id'
    ]

    for field in fields_without_defaults:
        assert columns[field]['default'] is None, f"{field} should not have a default value"


def test_model_structure_unique_constraints(db_inspector):
    """Ensure unique constraints are correctly defined"""
    table = 'classes'
    unique_constraints = db_inspector.get_unique_constraints(table)

    has_staff_dept_constraint = any(
        sorted(constraint['column_names']) == sorted(['level_id', 'code'])
        for constraint in unique_constraints
    )
    assert has_staff_dept_constraint, (
        "classes should have a unique constraint on "
        "level and code"
    )

def test_model_structure_foreign_keys(db_inspector):
    """Ensure that column foreign keys are correctly defined"""
    table = 'classes'
    foreign_keys = db_inspector.get_foreign_keys(table)
    level_fk = next(
        (fk for fk in foreign_keys if fk['constrained_columns'] == ['level_id']),
        None
    )
    mentor_fk = next(
        (fk for fk in foreign_keys if fk['constrained_columns'] == ['mentor_id']),
        None
    )
    student_rep_fk = next(
        (fk for fk in foreign_keys if fk['constrained_columns'] == ['student_rep_id']),
        None
    )
    assistant_rep_fk = next(
        (fk for fk in foreign_keys if fk['constrained_columns'] == ['assistant_rep_id']),
        None
    )
    assert level_fk is not None, "Missing foreign key for level_id"
    assert level_fk['options']['ondelete'].upper() == 'RESTRICT', \
        "level_id should RESTRICT on delete"

    assert mentor_fk is not None, "Missing foreign key for mentor_id"
    assert mentor_fk['options']['ondelete'].upper() == 'RESTRICT', \
        "mentor_id should RESTRICT on delete"

    assert student_rep_fk is not None, "Missing foreign key for student_rep_id"
    assert student_rep_fk['options']['ondelete'].upper() == 'SET NULL', \
        "student_rep_id should SET NULL on delete"

    assert assistant_rep_fk is not None, "Missing foreign key for assistant_rep_id"
    assert assistant_rep_fk['options']['ondelete'].upper() == 'SET NULL', \
        "assistant_rep_id should SET NULL on delete"




