import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from uuid import uuid4
from V2.app.main import app
from V2.app.schemas.staff_organization.staff_departments import StaffDepartmentResponse

client = TestClient(app)

@pytest.fixture
def mock_crud():
    test_uuid = uuid4()
    # Create a valid response object using the actual model
    valid_response = StaffDepartmentResponse(
        name="Test Department",
        description="Test Description",
        manager_id=None
    )
    response_dict = valid_response.model_dump()

    with patch("V2.app.routers.staff_organization.staff_departments.StaffDepartmentCrud") as mock:
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

    department_data = {
        "name": "HR Department",
        "description": "Human Resources"
    }
    response = client.post("/api/v1/staff/departments", json=department_data)

    mock_instance.create_department.assert_called_once()
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Department"  # This comes from our mock


def test_get_department(mock_crud):
    """Test getting a specific department"""
    mock_instance, test_uuid = mock_crud

    response = client.get(f"/api/v1/staff/departments/{test_uuid}")
    mock_instance.get_department.assert_called_once_with(test_uuid)

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Department"


