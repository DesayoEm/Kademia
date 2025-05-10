import pytest
from unittest.mock import patch, MagicMock
from uuid import uuid4

from V2.app.core.staff_management.crud.department import StaffDepartmentCrud
from V2.app.core.staff_management.schemas.department import (
    StaffDepartmentCreate,
    StaffDepartmentUpdate,
    DepartmentFilterParams
)
from V2.app.database.models.enums import ArchiveReason

@pytest.fixture
def mock_factory():
    with patch("V2.app.crud.staff_management.staff_departments.StaffDepartmentsFactory") as mock:
        mock_instance = MagicMock()
        mock.return_value = mock_instance

        test_uuid = uuid4()
        factory_response = {
            "id": test_uuid,
            "name": "Test Department",
            "description": "Test Description",
            "manager_id": None,
        }

        mock_instance.create_staff_department.return_value = factory_response
        mock_instance.get_staff_department.return_value = factory_response
        mock_instance.get_all_departments.return_value = [factory_response]
        mock_instance.update_staff_department.return_value = {**factory_response, "name": "Updated Department"}
        mock_instance.archive_department.return_value = None
        mock_instance.delete_department.return_value = None
        mock_instance.get_archived_department.return_value = factory_response
        mock_instance.get_all_archived_departments.return_value = [factory_response]
        mock_instance.restore_department.return_value = factory_response
        mock_instance.delete_archived_department.return_value = None

        yield mock_instance, test_uuid

def test_create_department(mock_factory):
    """Test the CRUD service create_department method"""
    mock_instance, _ = mock_factory

    session_mock = MagicMock()
    crud = StaffDepartmentCrud(session_mock)

    create_data = StaffDepartmentCreate(
        name="New Department",
        description="New Description"
    )
    result = crud.create_department(create_data)
    mock_instance.create_staff_department.assert_called_once_with(create_data)

    assert result.model_dump()["name"] == "Test Department"

def test_get_department(mock_factory):
    """Test getting a specific department"""
    mock_instance, test_uuid = mock_factory

    session_mock = MagicMock()
    crud = StaffDepartmentCrud(session_mock)

    result = crud.get_department(test_uuid)
    mock_instance.get_staff_department.assert_called_once_with(test_uuid)
    assert result.model_dump()["name"] == "Test Department"

def test_get_all_departments(mock_factory):
    """Test getting all departments"""
    mock_instance, _ = mock_factory

    session_mock = MagicMock()
    crud = StaffDepartmentCrud(session_mock)

    # Create filter params
    filters = DepartmentFilterParams()

    result = crud.get_all_departments(filters)
    mock_instance.get_all_departments.assert_called_once_with(filters)
    assert len(result) == 1
    assert result[0].model_dump()["name"] == "Test Department"

def test_update_department(mock_factory):
    """Test updating a specific department"""
    mock_instance, test_uuid = mock_factory

    session_mock = MagicMock()
    crud = StaffDepartmentCrud(session_mock)

    update_data = StaffDepartmentUpdate(
        name="Updated Department",
        description="Human Resources"
    )

    result = crud.update_department(test_uuid, update_data)
    mock_instance.update_staff_department.assert_called_once_with(test_uuid, update_data.model_dump())
    assert result.model_dump()["name"] == "Updated Department"

def test_archive_department(mock_factory):
    """Test archiving a specific department"""
    mock_instance, test_uuid = mock_factory

    session_mock = MagicMock()
    crud = StaffDepartmentCrud(session_mock)

    reason = ArchiveReason.ADMINISTRATIVE
    crud.archive_department(test_uuid, reason)
    mock_instance.archive_department.assert_called_once_with(test_uuid, reason)

def test_delete_department(mock_factory):
    """Test deleting a specific department"""
    mock_instance, test_uuid = mock_factory

    session_mock = MagicMock()
    crud = StaffDepartmentCrud(session_mock)

    crud.delete_department(test_uuid)
    mock_instance.delete_department.assert_called_once_with(test_uuid)

def test_get_archived_department(mock_factory):
    """Test getting an archived department"""
    mock_instance, test_uuid = mock_factory

    session_mock = MagicMock()
    crud = StaffDepartmentCrud(session_mock)

    result = crud.get_archived_department(test_uuid)
    mock_instance.get_archived_department.assert_called_once_with(test_uuid)
    assert result.model_dump()["name"] == "Test Department"

def test_get_all_archived_departments(mock_factory):
    """Test getting all archived departments"""
    mock_instance, _ = mock_factory

    session_mock = MagicMock()
    crud = StaffDepartmentCrud(session_mock)

    # Create filter params
    filters = DepartmentFilterParams()

    result = crud.get_all_archived_departments(filters)
    mock_instance.get_all_archived_departments.assert_called_once_with(filters)
    assert len(result) == 1
    assert result[0].model_dump()["name"] == "Test Department"

def test_restore_department(mock_factory):
    """Test restoring an archived department"""
    mock_instance, test_uuid = mock_factory

    session_mock = MagicMock()
    crud = StaffDepartmentCrud(session_mock)

    result = crud.restore_department(test_uuid)
    mock_instance.restore_department.assert_called_once_with(test_uuid)
    assert result.model_dump()["name"] == "Test Department"

def test_delete_archived_department(mock_factory):
    """Test deleting an archived department"""
    mock_instance, test_uuid = mock_factory

    session_mock = MagicMock()
    crud = StaffDepartmentCrud(session_mock)

    crud.delete_archived_department(test_uuid)
    mock_instance.delete_archived_department.assert_called_once_with(test_uuid)