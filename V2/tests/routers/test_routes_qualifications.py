import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
import uuid
from uuid import uuid4
from V2.app.main import app
from V2.app.schemas.staff_organization.educator_qualifications import(
    QualificationCreate, QualificationUpdate, QualificationResponse
)
from V2.app.database.models.data_enums import ArchiveReason

client = TestClient(app)

@pytest.fixture
def mock_crud():
    test_uuid = uuid4()
    educator_uuid = uuid4()

    valid_response = QualificationResponse(
        educator_id = educator_uuid,
        name="Test qualification",
        description="Test Description",
    )
    response_dict = valid_response.model_dump()

    with patch("V2.app.routers.staff_organization.qualifications.QualificationsCrud") as mock:
        mock_instance = MagicMock()
        mock.return_value = mock_instance

        mock_instance.create_qualification.return_value = response_dict
        mock_instance.get_qualification.return_value = response_dict
        mock_instance.get_all_qualifications.return_value = [response_dict]
        mock_instance.update_qualification.return_value = {**response_dict, "name": "Updated qualification"}
        mock_instance.archive_qualification.return_value = response_dict
        mock_instance.delete_qualification.return_value = None

        yield mock_instance, test_uuid


def test_create_qualification(mock_crud):
    """Test creating a new qualification"""
    mock_instance, _ = mock_crud

    educator_uuid = uuid4()
    qualification_data = QualificationCreate(
        educator_id = educator_uuid,
        name = "Teaching qualification",
        description = "Teaching"
    )
    json_data = qualification_data.model_dump()
    for key, value in json_data.items():
        if isinstance(value, uuid.UUID):
            json_data[key] = str(value)

    response = client.post("/api/v1/staff/qualifications", json=json_data)

    print("Mock Calls:", mock_instance.mock_calls)
    mock_instance.create_qualification.assert_called_once_with(qualification_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test qualification"

def test_get_qualification(mock_crud):
    """Test getting a specific qualification"""
    mock_instance, test_uuid = mock_crud

    response = client.get(f"/api/v1/staff/qualifications/{test_uuid}")
    print("Mock Calls:", mock_instance.mock_calls)

    mock_instance.get_qualification.assert_called_once_with(test_uuid)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test qualification"


def test_get_all_qualifications(mock_crud):
    """Test getting all qualifications"""
    mock_instance, _ = mock_crud
    response = client.get(f"/api/v1/staff/qualifications/")
    print("Mock Calls:", mock_instance.mock_calls)

    mock_instance.get_all_qualifications.assert_called_once()
    assert response.status_code == 200
    data = [item for item in response.json()]
    assert data[0]["name"] == "Test qualification"


def test_update_qualification(mock_crud):
    """Test updating a specific qualification"""
    mock_instance, test_uuid = mock_crud
    update_data = QualificationUpdate(name="Updated qualification",
                                  description = "Human Resources")

    response = client.put(f"/api/v1/staff/qualifications/{test_uuid}", json = update_data.model_dump())
    print("Mock Calls:", mock_instance.mock_calls)

    mock_instance.update_qualification.assert_called_once_with(test_uuid,update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated qualification"


def test_archive_qualification(mock_crud):
    """Test archiving a specific qualification"""
    mock_instance, test_uuid = mock_crud

    archive_data = {"reason": "ADMINISTRATIVE"}
    response = client.patch(f"/api/v1/staff/qualifications/{test_uuid}", json=archive_data)
    print("Mock Calls:", mock_instance.mock_calls)
    reason = ArchiveReason.ADMINISTRATIVE
    mock_instance.archive_qualification.assert_called_once_with(test_uuid, reason)
    assert response.status_code == 204
    assert response.content == b''


def test_delete_qualification(mock_crud):
    """Test deleting a specific qualification"""
    mock_instance, test_uuid = mock_crud

    response = client.delete(f"/api/v1/staff/qualifications/{test_uuid}")
    print("Mock Calls:", mock_instance.mock_calls)

    mock_instance.delete_qualification.assert_called_once_with(test_uuid)
    assert response.status_code == 204
    assert response.content == b''