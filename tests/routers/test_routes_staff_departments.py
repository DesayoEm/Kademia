import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from uuid import uuid4
from app import app
from app.core.staff_management.schemas.department import(
    StaffDepartmentResponse, StaffDepartmentUpdate, StaffDepartmentCreate
    )
from app import ArchiveReason

client = TestClient(app)

@pytest.fixture
def mock_crud():
    test_uuid = uuid4()
    valid_response = StaffDepartmentResponse(
        name="Test Department",
        description="Test Description",
        manager_id=None
    )
    response_dict = valid_response.model_dump()

    with patch("V2.app.academic_structure.staff_management.staff_departments.StaffDepartmentCrud") as mock:
        mock_instance = MagicMock()
        mock.return_value = mock_instance

        mock_instance.create_department.return_value = response_dict
        mock_instance.get_department.return_value = response_dict
        mock_instance.get_all_departments.return_value = [response_dict]
        mock_instance.update_department.return_value = {**response_dict, "name": "Updated Department"}
        mock_instance.archive_department.return_value = response_dict
        mock_instance.delete_department.return_value = None

        yield mock_instance, test_uuid


def test_create_department(mock_crud):
    """Test creating a new department"""
    mock_instance, _ = mock_crud

    department_data =StaffDepartmentCreate(
        name = "HR Department",
        description = "Human Resources"
    )

    response = client.post("/api/v1/staff/departments", json=department_data.model_dump())

    print("Mock Calls:", mock_instance.mock_calls)
    mock_instance.create_department.assert_called_once_with(department_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Department"


def test_get_department(mock_crud):
    """Test getting a specific department"""
    mock_instance, test_uuid = mock_crud

    response = client.get(f"/api/v1/staff/departments/{test_uuid}")
    print("Mock Calls:", mock_instance.mock_calls)

    mock_instance.get_department.assert_called_once_with(test_uuid)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Department"


def test_get_all_departments(mock_crud):
    """Test getting all departments"""
    mock_instance, _ = mock_crud
    response = client.get(f"/api/v1/staff/departments/")
    print("Mock Calls:", mock_instance.mock_calls)

    mock_instance.get_all_departments.assert_called_once()
    assert response.status_code == 200
    data = [item for item in response.json()]
    assert data[0]["name"] == "Test Department"


def test_update_department(mock_crud):
    """Test updating a specific department"""
    mock_instance, test_uuid = mock_crud
    update_data = StaffDepartmentUpdate(name="Updated Department",
                                        description = "Human Resources")

    response = client.put(f"/api/v1/staff/departments/{test_uuid}", json = update_data.model_dump())
    print("Mock Calls:", mock_instance.mock_calls)

    mock_instance.update_department.assert_called_once_with(test_uuid,update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Department"


def test_archive_department(mock_crud):
    """Test archiving a specific department"""
    mock_instance, test_uuid = mock_crud

    archive_data = {"reason": "ADMINISTRATIVE"}
    response = client.patch(f"/api/v1/staff/departments/{test_uuid}", json=archive_data)
    print("Mock Calls:", mock_instance.mock_calls)
    reason = ArchiveReason.ADMINISTRATIVE
    mock_instance.archive_department.assert_called_once_with(test_uuid, reason)
    assert response.status_code == 204
    assert response.content == b''


def test_delete_department(mock_crud):
    """Test deleting a specific department"""
    mock_instance, test_uuid = mock_crud

    response = client.delete(f"/api/v1/staff/departments/{test_uuid}")
    print("Mock Calls:", mock_instance.mock_calls)

    mock_instance.delete_department.assert_called_once_with(test_uuid)
    assert response.status_code == 204
    assert response.content == b''