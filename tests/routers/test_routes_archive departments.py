import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
import uuid
from uuid import uuid4
from app import app

client = TestClient(app)

@pytest.fixture
def mock_crud():
    test_uuid = uuid4()


    valid_response = {
        "name": "Test department",
        "description": "Test Description",
    }

    with patch("V2.app.academic_structure.staff_management.archived_staff_departments.StaffDepartmentCrud") as mock:
        mock_instance = MagicMock()
        mock.return_value = mock_instance

        mock_instance.get_archived_department.return_value = valid_response
        mock_instance.get_all_archived_departments.return_value = [valid_response]
        mock_instance.restore_department.return_value = valid_response
        mock_instance.delete_archived_department.return_value = None

        yield mock_instance, test_uuid


def test_get_archived_department(mock_crud):
    """Test getting a specific department"""
    mock_instance, test_uuid = mock_crud

    response = client.get(f"/api/v1/archive/staff/departments/{test_uuid}")
    print("Mock Calls:", mock_instance.mock_calls)

    mock_instance.get_archived_department.assert_called_once_with(test_uuid)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test department"


def test_get_all_archived_staff_departments(mock_crud):
    """Test getting all departments"""
    mock_instance, _ = mock_crud
    mock_instance.reset_mock()

    response = client.get("/api/v1/archive/staff/departments/")
    print("Mock Calls:", mock_instance.mock_calls)
    print("Response status:", response.status_code)
    print("Response data:", response.json())


    assert mock_instance.get_all_archived_departments.called

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["name"] == "Test department"


def test_restore_department(mock_crud):
    """Test restoring a specific department"""
    mock_instance, test_uuid = mock_crud

    response = client.patch(f"/api/v1/archive/staff/departments/{test_uuid}")
    print("Mock Calls:", mock_instance.mock_calls)

    mock_instance.restore_department.assert_called_once_with(test_uuid)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test department"


def test_delete_department(mock_crud):
    """Test deleting a specific department"""
    mock_instance, test_uuid = mock_crud

    response = client.delete(f"/api/v1/archive/staff/departments/{test_uuid}")
    print("Mock Calls:", mock_instance.mock_calls)

    mock_instance.delete_archived_department.assert_called_once_with(test_uuid)
    assert response.status_code == 204
    assert response.content == b''