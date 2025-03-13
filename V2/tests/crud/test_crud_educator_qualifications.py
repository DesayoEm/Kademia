import pytest
from unittest.mock import patch, MagicMock
from uuid import uuid4

from V2.app.crud.staff_organization.staff_roles import StaffRoleCrud
from V2.app.schemas.staff_organization.staff_roles import (
    StaffRoleCreate, StaffRoleUpdate, RolesFilterParams, StaffRoleResponse
)
from V2.app.database.models.data_enums import ArchiveReason

@pytest.fixture
def mock_factory():
    with patch("V2.app.crud.staff_organization.staff_roles.StaffRolesFactory") as mock:
        mock_instance = MagicMock()
        mock.return_value = mock_instance

        test_uuid = uuid4()

        # Create mock objects with proper attributes instead of Pydantic models
        class MockRole:
            def __init__(self, name="Test role", description="Test Description"):
                self.name = name
                self.description = description

        class MockUpdatedRole(MockRole):
            def __init__(self):
                super().__init__(name="Updated role", description="Test Description")

        # Setup return values using the mock objects
        mock_instance.create_role.return_value = MockRole()
        mock_instance.get_role.return_value = MockRole()
        mock_instance.get_all_roles.return_value = [MockRole()]
        mock_instance.update_role.return_value = MockUpdatedRole()
        mock_instance.archive_role.return_value = MockRole()
        mock_instance.delete_role.return_value = None
        mock_instance.get_archived_role.return_value = MockRole()
        mock_instance.get_all_archived_roles.return_value = [MockRole()]
        mock_instance.restore_role.return_value = MockRole()
        mock_instance.delete_archived_role.return_value = None

        yield mock_instance, test_uuid

def test_create_role(mock_factory):
    """Test the CRUD service create_role method"""
    mock_instance, _ = mock_factory

    session_mock = MagicMock()
    crud = StaffRoleCrud(session_mock)

    create_data = StaffRoleCreate(
        name="New role",
        description="New Description"
    )
    result = crud.create_role(create_data)
    mock_instance.create_role.assert_called_once_with(create_data)

    assert result.name == "Test role"
    assert result.description == "Test Description"

def test_get_role(mock_factory):
    """Test getting a specific role"""
    mock_instance, test_uuid = mock_factory

    session_mock = MagicMock()
    crud = StaffRoleCrud(session_mock)

    result = crud.get_role(test_uuid)
    mock_instance.get_role.assert_called_once_with(test_uuid)
    assert result.name == "Test role"
    assert result.description == "Test Description"

def test_get_all_roles(mock_factory):
    """Test getting all roles"""
    mock_instance, _ = mock_factory

    session_mock = MagicMock()
    crud = StaffRoleCrud(session_mock)
    filters = RolesFilterParams()

    result = crud.get_all_roles(filters)
    mock_instance.get_all_roles.assert_called_once_with(filters)
    assert len(result) == 1
    assert result[0].name == "Test role"
    assert result[0].description == "Test Description"

def test_update_role(mock_factory):
    """Test updating a specific role"""
    mock_instance, test_uuid = mock_factory

    session_mock = MagicMock()
    crud = StaffRoleCrud(session_mock)

    update_data = StaffRoleUpdate(
        name="Updated role",
        description="Human Resources"
    )

    result = crud.update_role(test_uuid, update_data)
    mock_instance.update_role.assert_called_once_with(test_uuid, update_data.model_dump())
    assert result.name == "Updated role"
    assert result.description == "Test Description"

def test_archive_role(mock_factory):
    """Test archiving a specific role"""
    mock_instance, test_uuid = mock_factory

    session_mock = MagicMock()
    crud = StaffRoleCrud(session_mock)

    reason = ArchiveReason.ADMINISTRATIVE
    result = crud.archive_role(test_uuid, reason)
    mock_instance.archive_role.assert_called_once_with(test_uuid, reason)



def test_delete_role(mock_factory):
    """Test deleting a specific role"""
    mock_instance, test_uuid = mock_factory

    session_mock = MagicMock()
    crud = StaffRoleCrud(session_mock)

    crud.delete_role(test_uuid)
    mock_instance.delete_role.assert_called_once_with(test_uuid)

def test_get_archived_role(mock_factory):
    """Test getting an archived role"""
    mock_instance, test_uuid = mock_factory

    session_mock = MagicMock()
    crud = StaffRoleCrud(session_mock)

    result = crud.get_archived_role(test_uuid)
    mock_instance.get_archived_role.assert_called_once_with(test_uuid)
    assert result.name == "Test role"
    assert result.description == "Test Description"

def test_get_all_archived_roles(mock_factory):
    """Test getting all archived roles"""
    mock_instance, _ = mock_factory

    session_mock = MagicMock()
    crud = StaffRoleCrud(session_mock)

    filters = RolesFilterParams()

    result = crud.get_all_archived_roles(filters)
    mock_instance.get_all_archived_roles.assert_called_once_with(filters)
    assert len(result) == 1
    assert result[0].name == "Test role"
    assert result[0].description == "Test Description"

def test_restore_role(mock_factory):
    """Test restoring an archived role"""
    mock_instance, test_uuid = mock_factory

    session_mock = MagicMock()
    crud = StaffRoleCrud(session_mock)

    result = crud.restore_role(test_uuid)
    mock_instance.restore_role.assert_called_once_with(test_uuid)
    assert result.name == "Test role"
    assert result.description == "Test Description"

def test_delete_archived_role(mock_factory):
    """Test deleting an archived role"""
    mock_instance, test_uuid = mock_factory

    session_mock = MagicMock()
    crud = StaffRoleCrud(session_mock)

    crud.delete_archived_role(test_uuid)
    mock_instance.delete_archived_role.assert_called_once_with(test_uuid)