from .common_test_imports import *


def test_model_structure_column_data_types(db_inspector):
    """Ensure all required columns are present and have the correct data type"""
    table = 'students'
    columns = {col['name']: col for col in db_inspector.get_columns(table)}
    expected_types = {
        "id": UUID,
        "password_hash": String,
        "first_name": String,
        "last_name": String,
        "gender": Enum,
        "last_login": DateTime,
        "student_id": String,
        "user_type": Enum,
        "access_level": Enum,
        "status": Enum,
        "date_of_birth": Date,
        "image_url": String,
        "class_id": UUID,
        "level_id": UUID,
        "department_id": UUID,
        "guardian_id": UUID,
        "is_repeating": Boolean,
        "admission_date": Date,
        "date_left": Date,
        "graduation_date": Date,
        "created_at": DateTime,
        "last_modified_at": DateTime,
        "is_archived": Boolean,
        "archived_at": DateTime,
        "archive_reason": Enum,
        "created_by": UUID,
        "last_modified_by": UUID,
    }

    for column, expected_type in expected_types.items():
        assert isinstance(columns[column]['type'], expected_type), f"{column} has incorrect type"

    enum_checks = {
        "gender": Gender,
        "archive_reason": ArchiveReason,
        "access_level": AccessLevel,
        "user_type": UserType,
        "status": StudentStatus
    }

    for column, enum_class in enum_checks.items():
        col_type = columns[column]['type']
        assert isinstance(col_type, Enum), f"{column} should be Enum"
        assert col_type.enum_class is enum_class or col_type.enums == [e.value for e in enum_class], f"{column} Enum mismatch"


def test_model_structure_nullable_constraints(db_inspector):
    """Ensure correctness of  nullable and not nullable fields"""
    table = 'students'
    columns = db_inspector.get_columns(table)

    expected_nullable = {
        "id": False,
        "password_hash": False,
        "first_name": False,
        "last_name": False,
        "gender": False,
        "status": False,
        "last_login": True,
        "deletion_eligible":False,
        "created_at": False,
        "last_modified_at": False,
        "is_archived": False,
        "archived_at": True,
        "archived_by": True,
        "archive_reason": True,
        "created_by": False,
        "last_modified_by": False,
        "student_id": False,
        "date_of_birth": False,
        "access_level": False,
        "user_type": False,
        "image_url": True,
        "class_id": False,
        "level_id": False,
        "department_id": True,
        "guardian_id": False,
        "is_repeating": False,
        "admission_date":False,
        "date_left":True,
        "graduation_date":True,

    }
    for column in columns:
        column['name'] = column['name']
        assert column['nullable'] == expected_nullable.get(column['name']), \
            f"column {column['name']} is not nullable as expected"


def test_model_structure_default_values(db_inspector):
    """Ensure no default values are set at db level since they're handled
    at the application level"""
    table = 'students'
    columns = {col['name']: col for col in db_inspector.get_columns(table)}

    fields_without_defaults = [
        'id', "password_hash", "first_name", "last_name", "gender", "status",'level_id',
        "last_login","created_at","last_modified_at","is_archived", "archived_at",
        "archived_by", "archive_reason", "created_by","last_modified_by", "access_level","user_type",
        "student_id","image_url","date_of_birth","class_id","department_id","deletion_eligible", "guardian_id",
        "is_repeating", "admission_date", "date_left",  "graduation_date",
    ]

    for field in fields_without_defaults:
        assert columns[field]['default'] is None, f"{field} should not have a default value"


def test_model_structure_string_column_length(db_inspector):
    """Ensure columns with String type have the correct max lengths"""
    table = 'students'
    columns = {col['name']: col for col in db_inspector.get_columns(table)}


    assert columns['password_hash']['type'].length == 300
    assert columns['first_name']['type'].length == 30
    assert columns['last_name']['type'].length == 30
    assert columns['student_id']['type'].length == 14
    assert columns['image_url']['type'].length == 200


def test_model_structure_unique_constraints(db_inspector):
    """"Ensure unique constraints are correctly defined"""
    table = 'students'
    unique_constraints = db_inspector.get_unique_constraints(table)

    constraints_map = {
        constraint['name']: constraint['column_names']
        for constraint in unique_constraints
    }
    assert any(columns == ['student_id'] for columns in constraints_map.values()
               ), "student_id should have a unique constraint"



def test_model_structure_foreign_keys(db_inspector):
    """Ensure that column foreign keys are correctly defined"""
    table = 'students'
    foreign_keys = db_inspector.get_foreign_keys(table)
    class_fk = next(
        (fk for fk in foreign_keys if fk['constrained_columns'] == ['class_id']),
        None
    )
    level_fk = next(
        (fk for fk in foreign_keys if fk['constrained_columns'] == ['level_id']),
        None
    )
    department_fk = next(
        (fk for fk in foreign_keys if fk['constrained_columns'] == ['department_id']),
        None
    )
    guardian_fk = next(
        (fk for fk in foreign_keys if fk['constrained_columns'] == ['guardian_id']),
        None
    )
    assert class_fk is not None, "Missing foreign key for class_id"
    assert class_fk['options']['ondelete'].upper() == 'RESTRICT', \
        "class_id should RESTRICT on delete"

    assert level_fk is not None, "Missing foreign key for level_id"
    assert level_fk['options']['ondelete'].upper() == 'RESTRICT', \
        "level_id should RESTRICT on delete"

    assert department_fk is not None, "Missing foreign key for department_id"
    assert department_fk['options']['ondelete'].upper() == 'RESTRICT', \
        "department_id should RESTRICT on delete"

    assert guardian_fk is not None, "Missing foreign key for guardian_id"
    assert guardian_fk['options']['ondelete'].upper() == 'RESTRICT', \
        "guardian_id should RESTRICT on delete"



