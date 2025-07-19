import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from uuid import uuid4
from app import app

client = TestClient(app)

@pytest.fixture
def mock_crud():
    test_uuid = uuid4()
    

    valid_response = {
        "name": "Test role",
        "description": "Test Description",
    }

    with patch("V2.app.academic_structure.staff_management.archived_staff_roles.StaffRoleCrud") as mock:
        mock_instance = MagicMock()
        mock.return_value = mock_instance
        mock_instance.get_archived_role.return_value = valid_response
        mock_instance.get_all_archived_roles.return_value = [valid_response]
        mock_instance.restore_role.return_value = valid_response
        mock_instance.delete_archived_role.return_value = None

        yield mock_instance, test_uuid


def test_get_archived_role(mock_crud):
    """Test getting a specific role"""
    mock_instance, test_uuid = mock_crud

    response = client.get(f"/api/v1/archive/staff/roles/{test_uuid}")
    print("Mock Calls:", mock_instance.mock_calls)

    mock_instance.get_archived_role.assert_called_once_with(test_uuid)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test role"


def test_get_all_archived_staff_roles(mock_crud):
    """Test getting all roles"""
    mock_instance, _ = mock_crud
    mock_instance.reset_mock()

    response = client.get("/api/v1/archive/staff/roles/")
    print("Mock Calls:", mock_instance.mock_calls)
    print("Response status:", response.status_code)
    print("Response data:", response.json())


    assert mock_instance.get_all_archived_roles.called

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["name"] == "Test role"


def test_restore_role(mock_crud):
    """Test restoring a specific role"""
    mock_instance, test_uuid = mock_crud

    response = client.patch(f"/api/v1/archive/staff/roles/{test_uuid}")
    print("Mock Calls:", mock_instance.mock_calls)

    mock_instance.restore_role.assert_called_once_with(test_uuid)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test role"


def test_delete_role(mock_crud):
    """Test deleting a specific role"""
    mock_instance, test_uuid = mock_crud

    response = client.delete(f"/api/v1/archive/staff/roles/{test_uuid}")
    print("Mock Calls:", mock_instance.mock_calls)

    mock_instance.delete_archived_role.assert_called_once_with(test_uuid)
    assert response.status_code == 204
    assert response.content == b''