from common_test_imports import *


def test_column_data_types_in_access_level_changes(db_inspector):
    """Confirm all required columns are present and have the correct data type"""
    table ='access_level_changes'
    columns = {col['name']: col for col in db_inspector.get_columns(table)}
    expected_types = {
        "id": UUID,
        "staff_id": UUID,
        "previous_level": Enum,
        "new_level": Enum,
        "reason": String,
        "changed_at": DateTime,
        "changed_by": UUID
    }
    for column, expected_type in expected_types.items():
        assert isinstance(columns[column]['type'], expected_type), f"{column} has incorrect type"

    enum_checks = {
        'previous_level': AccessLevel,
        'new_level': AccessLevel
    }
    for column, enum_class in enum_checks.items():
        col_type = columns[column]['type']
        assert col_type.enum_class is enum_class or col_type.enums == [e.value for e in enum_class], f"{column} Enum mismatch"
