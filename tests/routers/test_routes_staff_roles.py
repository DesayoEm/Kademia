import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from uuid import uuid4
from app import app
from app.core.staff_management.schemas.staff_title import(
    StaffRoleCreate, StaffRoleUpdate, StaffRoleResponse
)
from app import ArchiveReason

client = TestClient(app)

@pytest.fixture
def mock_crud():
    test_uuid = uuid4()
    valid_response = StaffRoleResponse(
        name="Test Role",
        description="Test Description",
    )
    response_dict = valid_response.model_dump()

    with patch("V2.app.academic_structure.staff_management.staff_roles.StaffRoleCrud") as mock:
        mock_instance = MagicMock()
        mock.return_value = mock_instance

        mock_instance.create_role.return_value = response_dict
        mock_instance.get_role.return_value = response_dict
        mock_instance.get_all_roles.return_value = [response_dict]
        mock_instance.update_role.return_value = {**response_dict, "name": "Updated role"}
        mock_instance.archive_role.return_value = response_dict
        mock_instance.delete_role.return_value = None

        yield mock_instance, test_uuid


def test_create_role(mock_crud):
    """Test creating a new role"""
    mock_instance, _ = mock_crud

    role_data =StaffRoleCreate(
        name = "HR role",
        description = "Human Resources"
    )

    response = client.post("/api/v1/staff/roles", json=role_data.model_dump())

    print("Mock Calls:", mock_instance.mock_calls)
    mock_instance.create_role.assert_called_once_with(role_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Role"


def test_get_role(mock_crud):
    """Test getting a specific role"""
    mock_instance, test_uuid = mock_crud

    response = client.get(f"/api/v1/staff/roles/{test_uuid}")
    print("Mock Calls:", mock_instance.mock_calls)

    mock_instance.get_role.assert_called_once_with(test_uuid)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Role"


def test_get_all_roles(mock_crud):
    """Test getting all roles"""
    mock_instance, _ = mock_crud
    response = client.get(f"/api/v1/staff/roles/")
    print("Mock Calls:", mock_instance.mock_calls)

    mock_instance.get_all_roles.assert_called_once()
    assert response.status_code == 200
    data = [item for item in response.json()]
    assert data[0]["name"] == "Test Role"


def test_update_role(mock_crud):
    """Test updating a specific role"""
    mock_instance, test_uuid = mock_crud
    update_data = StaffRoleUpdate(name="Updated role",
                                        description = "Human Resources")

    response = client.put(f"/api/v1/staff/roles/{test_uuid}", json = update_data.model_dump())
    print("Mock Calls:", mock_instance.mock_calls)

    mock_instance.update_role.assert_called_once_with(test_uuid,update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated role"


def test_archive_role(mock_crud):
    """Test archiving a specific role"""
    mock_instance, test_uuid = mock_crud

    archive_data = {"reason": "ADMINISTRATIVE"}
    response = client.patch(f"/api/v1/staff/roles/{test_uuid}", json=archive_data)
    print("Mock Calls:", mock_instance.mock_calls)
    reason = ArchiveReason.ADMINISTRATIVE
    mock_instance.archive_role.assert_called_once_with(test_uuid, reason)
    assert response.status_code == 204
    assert response.content == b''


def test_delete_role(mock_crud):
    """Test deleting a specific role"""
    mock_instance, test_uuid = mock_crud

    response = client.delete(f"/api/v1/staff/roles/{test_uuid}")
    print("Mock Calls:", mock_instance.mock_calls)

    mock_instance.delete_role.assert_called_once_with(test_uuid)
    assert response.status_code == 204
    assert response.content == b''