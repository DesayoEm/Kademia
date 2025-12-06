import pytest
from unittest.mock import patch, MagicMock
from uuid import uuid4

from app.core import StaffDepartmentsFactory
from app.core.staff_management.schemas.department import (
    StaffDepartmentCreate,
    DepartmentFilterParams,
)
from app import ArchiveReason
from app.core import EntityNotFoundError
from app.core import DepartmentNotFoundError, DuplicateDepartmentError


@pytest.fixture
def mock_repository():
    with patch(
        "V2.app.core.factories.staff_management.department.SQLAlchemyRepository"
    ) as mock:
        mock_instance = MagicMock()
        mock.return_value = mock_instance

        test_uuid = uuid4()
        department_model = MagicMock()
        department_model.id = test_uuid
        department_model.name = "Test Department"
        department_model.description = "Test Description"
        department_model.manager_id = None

        mock_instance.create.return_value = department_model
        mock_instance.get_by_id.return_value = department_model
        mock_instance.execute_query.return_value = [department_model]
        mock_instance.update.return_value = department_model
        mock_instance.archive.return_value = department_model
        mock_instance.delete.return_value = None
        mock_instance.execute_archive_query.return_value = [department_model]
        mock_instance.get_archive_by_id.return_value = department_model
        mock_instance.restore.return_value = department_model
        mock_instance.delete_archive.return_value = None

        yield mock_instance, test_uuid, department_model


def test_create_staff_department(mock_repository):
    """Test the factory create_staff_department method"""
    mock_instance, _, _ = mock_repository
    session_mock = MagicMock()

    with patch(
        "V2.app.core.factories.staff_management.department.StaffOrganizationValidators"
    ) as validator_mock:
        validator_instance = MagicMock()
        validator_mock.return_value = validator_instance

        validator_instance.validate_name = lambda x: x

        factory = StaffDepartmentsFactory(session_mock)

        create_data = StaffDepartmentCreate(
            name="New Department", description="New Description"
        )

        result = factory.create_staff_department(create_data)
        assert mock_instance.create.called
        assert result.name == "Test Department"


def test_create_staff_department_duplicate_error(mock_repository):
    """Test duplicate department error handling"""
    mock_instance, _, _ = mock_repository

    unique_error = DuplicateDepartmentError(
        input_value="New department", detail="None", field="name"
    )
    mock_instance.create.side_effect = unique_error

    session_mock = MagicMock()

    with patch(
        "V2.app.core.factories.staff_management.department.StaffOrganizationValidators"
    ) as validator_mock:
        validator_instance = MagicMock()
        validator_mock.return_value = validator_instance
        validator_instance.validate_name = lambda x: x

        factory = StaffDepartmentsFactory(session_mock)
        create_data = StaffDepartmentCreate(
            name="New Department", description="New Description"
        )

        # Test that the correct exception is raised
        with pytest.raises(DuplicateDepartmentError):
            factory.create_staff_department(create_data)


def test_get_all_departments(mock_repository):
    """Test getting all departments"""
    mock_instance, _, department_model = mock_repository

    session_mock = MagicMock()
    with patch(
        "V2.app.core.factories.staff_management.department.StaffOrganizationValidators"
    ):
        factory = StaffDepartmentsFactory(session_mock)

        filters = DepartmentFilterParams()
        results = factory.get_all_departments(filters)

        mock_instance.execute_query.assert_called_once()
        call_args = mock_instance.execute_query.call_args[0]
        assert call_args[0] == ["name", "description"]
        assert call_args[1] == filters

        assert len(results) == 1
        assert results[0].name == "Test Department"


def test_get_staff_department(mock_repository):
    """Test getting a specific department"""
    mock_instance, test_uuid, _ = mock_repository

    session_mock = MagicMock()
    with patch(
        "V2.app.core.factories.staff_management.department.StaffOrganizationValidators"
    ):
        factory = StaffDepartmentsFactory(session_mock)

        result = factory.get_staff_department(test_uuid)

        mock_instance.get_by_id.assert_called_once_with(test_uuid)
        assert result.name == "Test Department"


def test_get_staff_department_not_found(mock_repository):
    """Test getting a non-existent department"""
    mock_instance, test_uuid, _ = mock_repository
    mock_instance.get_by_id.side_effect = EntityNotFoundError(
        entity_type="StaffDepartments"
    )

    session_mock = MagicMock()
    with patch(
        "V2.app.core.factories.staff_management.department.StaffOrganizationValidators"
    ):
        factory = StaffDepartmentsFactory(session_mock)

        with pytest.raises(DepartmentNotFoundError):
            factory.get_staff_department(test_uuid)


def test_update_staff_department(mock_repository):
    """Test updating a department"""
    mock_instance, test_uuid, department_model = mock_repository

    # Make the update method return a modified department
    updated_department = MagicMock()
    updated_department.name = "Updated Department"
    updated_department.description = "Updated Description"
    mock_instance.update.return_value = updated_department

    session_mock = MagicMock()
    with patch(
        "V2.app.core.factories.staff_management.department.StaffOrganizationValidators"
    ) as validator_mock:
        validator_instance = MagicMock()
        validator_mock.return_value = validator_instance
        validator_instance.validate_name = lambda x: x

        factory = StaffDepartmentsFactory(session_mock)

        # Create update data
        update_data = {
            "name": "Updated Department",
            "description": "Updated Description",
        }

        result = factory.update_staff_department(test_uuid, update_data)

        # Verify repository was called correctly
        mock_instance.update.assert_called_once()

        # Verify result
        assert result.name == "Updated Department"


def test_update_staff_department_not_found(mock_repository):
    """Test updating a non-existent department"""
    mock_instance, test_uuid, _ = mock_repository

    # Create a simple EntityNotFoundError without extra parameters
    mock_instance.get_by_id.side_effect = EntityNotFoundError(
        entity_type="StaffDepartments"
    )

    session_mock = MagicMock()
    with patch(
        "V2.app.core.factories.staff_management.department.StaffOrganizationValidators"
    ):
        factory = StaffDepartmentsFactory(session_mock)

        update_data = {
            "name": "Updated Department",
            "description": "Updated Description",
        }

        # Test that the correct exception is raised
        with pytest.raises(DepartmentNotFoundError):
            factory.update_staff_department(test_uuid, update_data)


def test_update_staff_department_duplicate(mock_repository):
    """Test updating a department with a duplicate name"""
    mock_instance, test_uuid, _ = mock_repository

    # Create a UniqueViolationError with correct parameters
    unique_error = DuplicateDepartmentError(
        input_value="New department", detail="None", field="name"
    )
    mock_instance.update.side_effect = unique_error

    session_mock = MagicMock()
    with patch(
        "V2.app.core.factories.staff_management.department.StaffOrganizationValidators"
    ) as validator_mock:
        validator_instance = MagicMock()
        validator_mock.return_value = validator_instance
        validator_instance.validate_name = lambda x: x

        factory = StaffDepartmentsFactory(session_mock)

        update_data = {
            "name": "Updated Department",
            "description": "Updated Description",
        }

        # Test that the correct exception is raised
        with pytest.raises(DuplicateDepartmentError):
            factory.update_staff_department(test_uuid, update_data)


def test_archive_department(mock_repository):
    """Test archiving a department"""
    mock_instance, test_uuid, _ = mock_repository

    session_mock = MagicMock()
    with patch(
        "V2.app.core.factories.staff_management.department.StaffOrganizationValidators"
    ):
        factory = StaffDepartmentsFactory(session_mock)

        reason = ArchiveReason.ADMINISTRATIVE
        result = factory.archive_department(test_uuid, reason)

        # Verify repository was called correctly
        mock_instance.archive.assert_called_once()

        # Verify result
        assert result.name == "Test Department"


def test_archive_department_not_found(mock_repository):
    """Test archiving a non-existent department"""
    mock_instance, test_uuid, _ = mock_repository

    # Create EntityNotFoundError with required entity_type parameter
    mock_instance.archive.side_effect = EntityNotFoundError(
        entity_type="StaffDepartments"
    )

    session_mock = MagicMock()
    with patch(
        "V2.app.core.factories.staff_management.department.StaffOrganizationValidators"
    ):
        factory = StaffDepartmentsFactory(session_mock)

        reason = ArchiveReason.ADMINISTRATIVE

        # Test that the correct exception is raised
        with pytest.raises(DepartmentNotFoundError):
            factory.archive_department(test_uuid, reason)


def test_delete_department(mock_repository):
    """Test deleting a department"""
    mock_instance, test_uuid, _ = mock_repository

    session_mock = MagicMock()
    with patch(
        "V2.app.core.factories.staff_management.department.StaffOrganizationValidators"
    ):
        factory = StaffDepartmentsFactory(session_mock)

        factory.delete_department(test_uuid)

        # Verify repository was called correctly
        mock_instance.delete.assert_called_once_with(test_uuid)


def test_delete_department_not_found(mock_repository):
    """Test deleting a non-existent department"""
    mock_instance, test_uuid, _ = mock_repository

    # Create EntityNotFoundError with required entity_type parameter
    mock_instance.delete.side_effect = EntityNotFoundError(
        entity_type="StaffDepartments"
    )

    session_mock = MagicMock()
    with patch(
        "V2.app.core.factories.staff_management.department.StaffOrganizationValidators"
    ):
        factory = StaffDepartmentsFactory(session_mock)

        # Test that the correct exception is raised
        with pytest.raises(DepartmentNotFoundError):
            factory.delete_department(test_uuid)


def test_get_all_archived_departments(mock_repository):
    """Test getting all archived departments"""
    mock_instance, _, department_model = mock_repository

    session_mock = MagicMock()
    with patch(
        "V2.app.core.factories.staff_management.department.StaffOrganizationValidators"
    ):
        factory = StaffDepartmentsFactory(session_mock)

        filters = DepartmentFilterParams()
        results = factory.get_all_archived_departments(filters)

        # Verify repository was called correctly
        mock_instance.execute_archive_query.assert_called_once()
        call_args = mock_instance.execute_archive_query.call_args[0]
        assert call_args[0] == ["name", "description"]
        assert call_args[1] == filters

        # Verify results
        assert len(results) == 1
        assert results[0].name == "Test Department"


def test_get_archived_department(mock_repository):
    """Test getting a specific archived department"""
    mock_instance, test_uuid, _ = mock_repository

    session_mock = MagicMock()
    with patch(
        "V2.app.core.factories.staff_management.department.StaffOrganizationValidators"
    ):
        factory = StaffDepartmentsFactory(session_mock)

        result = factory.get_archived_department(test_uuid)

        # Verify repository was called correctly
        mock_instance.get_archive_by_id.assert_called_once_with(test_uuid)

        # Verify result
        assert result.name == "Test Department"


def test_get_archived_department_not_found(mock_repository):
    """Test getting a non-existent archived department"""
    mock_instance, test_uuid, _ = mock_repository

    # Create EntityNotFoundError with required entity_type parameter
    mock_instance.get_archive_by_id.side_effect = EntityNotFoundError(
        entity_type="StaffDepartments"
    )

    session_mock = MagicMock()
    with patch(
        "V2.app.core.factories.staff_management.department.StaffOrganizationValidators"
    ):
        factory = StaffDepartmentsFactory(session_mock)

        # Test that the correct exception is raised
        with pytest.raises(DepartmentNotFoundError):
            factory.get_archived_department(test_uuid)


def test_restore_department(mock_repository):
    """Test restoring an archived department"""
    mock_instance, test_uuid, _ = mock_repository

    session_mock = MagicMock()
    with patch(
        "V2.app.core.factories.staff_management.department.StaffOrganizationValidators"
    ):
        factory = StaffDepartmentsFactory(session_mock)

        result = factory.restore_department(test_uuid)

        # Verify repository was called correctly
        mock_instance.restore.assert_called_once_with(test_uuid)

        # Verify result
        assert result.name == "Test Department"


def test_restore_department_not_found(mock_repository):
    """Test restoring a non-existent archived department"""
    mock_instance, test_uuid, _ = mock_repository

    # Create a simple EntityNotFoundError without extra parameters
    mock_instance.get_archive_by_id.side_effect = EntityNotFoundError(
        entity_type="StaffDepartments"
    )

    session_mock = MagicMock()
    with patch(
        "V2.app.core.factories.staff_management.department.StaffOrganizationValidators"
    ):
        factory = StaffDepartmentsFactory(session_mock)

        # Test that the correct exception is raised
        with pytest.raises(DepartmentNotFoundError):
            factory.restore_department(test_uuid)


def test_delete_archived_department(mock_repository):
    """Test deleting an archived department"""
    mock_instance, test_uuid, _ = mock_repository

    session_mock = MagicMock()
    with patch(
        "V2.app.core.factories.staff_management.department.StaffOrganizationValidators"
    ):
        factory = StaffDepartmentsFactory(session_mock)

        factory.delete_archived_department(test_uuid)

        # Verify repository was called correctly
        mock_instance.delete_archive.assert_called_once_with(test_uuid)


def test_delete_archived_department_not_found(mock_repository):
    """Test deleting a non-existent archived department"""
    mock_instance, test_uuid, _ = mock_repository

    # Create EntityNotFoundError with required entity_type parameter
    mock_instance.delete_archive.side_effect = EntityNotFoundError(
        entity_type="StaffDepartments"
    )

    session_mock = MagicMock()
    with patch(
        "V2.app.core.factories.staff_management.department.StaffOrganizationValidators"
    ):
        factory = StaffDepartmentsFactory(session_mock)

        # Test that the correct exception is raised
        with pytest.raises(DepartmentNotFoundError):
            factory.delete_archived_department(test_uuid)
