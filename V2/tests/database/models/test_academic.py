from common_test_imports import *


def test_column_data_types_in_subject(db_inspector):
    """Confirm all required columns are present and have the correct data type"""
    table ='subjects'
    columns = {col['name']: col for col in db_inspector.get_columns(table)}
    expected_types = {
        "id": UUID,
        "name": String,
        "class_level": Enum,
        "group": Enum,
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

#
def test_column_data_types_in_student_subjects(db_inspector):
    """Confirm all required columns are present and have the correct data type"""
    table = 'student_subjects'
    columns = {col['name']: col for col in db_inspector.get_columns(table)}
    expected_types = {
        "id": UUID,
        "student_id": UUID,
        "subject_id": UUID,
        "academic_year": String,
        "term": Enum,
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
        'term': Term
        }
    for column, enum_class in enum_checks.items():
        col_type = columns[column]['type']
        assert col_type.enum_class is enum_class or col_type.enums == [e.value for e in enum_class], f"{column} Enum mismatch"


def test_column_data_types_in_grades(db_inspector):
    """Confirm all required columns are present and have the correct data type"""
    table ='grades'
    columns = {col['name']: col for col in db_inspector.get_columns(table)}
    expected_types = {
        "id": UUID,
        "student_id": UUID,
        "subject_id": UUID,
        "department_id": UUID,
        "academic_year": String,
        "term": Enum,
        "type": Enum,
        "marks": Integer,
        "file_url": String,
        "graded_by": UUID,
        "remarks": String,
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
        'type': GradeType,
        'term': Term
    }
    for column, enum_class in enum_checks.items():
        col_type = columns[column]['type']
        assert col_type.enum_class is enum_class or col_type.enums == [e.value for e in enum_class], f"{column} Enum mismatch"


def test_column_data_types_in_total_grades(db_inspector):
    """Confirm all required columns are present and have the correct data type"""
    table ='total_grades'
    columns = {col['name']: col for col in db_inspector.get_columns(table)}
    expected_types = {
        "id": UUID,
        "student_id": UUID,
        "subject_id": UUID,
        "academic_year": String,
        "term": Enum,
        "total_marks": Float,
        "rank": Integer,
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
        'term': Term
    }
    for column, enum_class in enum_checks.items():
        col_type = columns[column]['type']
        assert col_type.enum_class is enum_class or col_type.enums == [e.value for e in enum_class], f"{column} Enum mismatch"


def test_column_data_types_in_repetitions(db_inspector):
    """Confirm all required columns are present and have the correct data type"""
    table ='repetitions'
    columns = {col['name']: col for col in db_inspector.get_columns(table)}
    expected_types = {
        "id": UUID,
        "student_id": UUID,
        "academic_year": Integer,
        "from_class_level": Enum,
        "to_class_level": Enum,
        "from_class_id": UUID,
        "to_class_id": UUID,
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
        "last_modified_by": UUID
    }
    for column, expected_type in expected_types.items():
        assert isinstance(columns[column]['type'], expected_type), f"{column} has incorrect type"

    enum_checks = {
        "archive_reason": ArchiveReason,
        "status": ApprovalStatus,
        'from_class_level': ClassLevel,
        'to_class_level': ClassLevel
    }
    for column, enum_class in enum_checks.items():
        col_type = columns[column]['type']
        assert col_type.enum_class is enum_class or col_type.enums == [e.value for e in enum_class], f"{column} Enum mismatch"



def test_column_data_types_in_student_transfers(db_inspector):
    """Confirm all required columns are present and have the correct data type"""
    table ='student_transfers'
    columns = {col['name']: col for col in db_inspector.get_columns(table)}
    expected_types = {
        "id": UUID,
        "student_id": UUID,
        "academic_year": Integer,
        "from_class_level": Enum,
        "to_class_level": Enum,
        "from_class_id": UUID,
        "to_class_id": UUID,
        "from_department_id": UUID,
        "to_department_id": UUID,
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
        "last_modified_by": UUID
    }
    for column, expected_type in expected_types.items():
        assert isinstance(columns[column]['type'], expected_type), f"{column} has incorrect type"

    enum_checks = {
        "archive_reason": ArchiveReason,
        "status": ApprovalStatus,
        'from_class_level': ClassLevel,
        'to_class_level': ClassLevel
    }
    for column, enum_class in enum_checks.items():
        col_type = columns[column]['type']
        assert col_type.enum_class is enum_class or col_type.enums == [e.value for e in enum_class], f"{column} Enum mismatch"


def test_column_data_types_in_educator_qualifications(db_inspector):
    """Confirm all required columns are present and have the correct data type"""
    table ='educator_qualifications'
    columns = {col['name']: col for col in db_inspector.get_columns(table)}
    expected_types = {
        "id": UUID,
        "educator_id": UUID,
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
        "archive_reason": ArchiveReason

    }
    for column, enum_class in enum_checks.items():
        col_type = columns[column]['type']
        assert col_type.enum_class is enum_class or col_type.enums == [e.value for e in enum_class], f"{column} Enum mismatch"





