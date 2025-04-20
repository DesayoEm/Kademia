import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
import uuid
from uuid import uuid4
from V2.app.main import app


client = TestClient(app)

@pytest.fixture
def mock_crud():
    test_uuid = uuid4()
    educator_uuid = uuid4()

    valid_response = {
        "educator_id": str(educator_uuid),
        "name": "Test qualification",
        "description": "Test Description",
    }

    with patch("V2.app.routers.staff_management.archived_qualifications.QualificationsCrud") as mock:
        mock_instance = MagicMock()
        mock.return_value = mock_instance

        mock_instance.get_archived_qualification.return_value = valid_response
        mock_instance.get_all_archived_qualifications.return_value = [valid_response]
        mock_instance.restore_qualification.return_value = valid_response
        mock_instance.delete_archived_qualification.return_value = None

        yield mock_instance, test_uuid



def test_get_archived_qualification(mock_crud):
    """Test getting a specific qualification"""
    mock_instance, test_uuid = mock_crud

    response = client.get(f"/api/v1/archive/staff/qualifications/{test_uuid}")
    print("Mock Calls:", mock_instance.mock_calls)

    mock_instance.get_archived_qualification.assert_called_once()
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test qualification"


def test_get_all_archived_qualifications(mock_crud):
    """Test getting all qualifications"""
    mock_instance, _ = mock_crud
    response = client.get(f"/api/v1/archive/staff/qualifications/")
    print("Mock Calls:", mock_instance.mock_calls)

    mock_instance.get_all_archived_qualifications.assert_called_once()
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["name"] == "Test qualification"



def test_restore_qualification(mock_crud):
    """Test archiving a specific qualification"""
    mock_instance, test_uuid = mock_crud


    response = client.patch(f"/api/v1/archive/staff/qualifications/{test_uuid}")
    print("Mock Calls:", mock_instance.mock_calls)
    mock_instance.restore_qualification.assert_called_once_with(test_uuid)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test qualification"


def test_delete_qualification(mock_crud):
    """Test deleting a specific qualification"""
    mock_instance, test_uuid = mock_crud

    response = client.delete(f"/api/v1/archive/staff/qualifications/{test_uuid}")
    print("Mock Calls:", mock_instance.mock_calls)

    mock_instance.delete_archived_qualification.assert_called_once_with(test_uuid)
    assert response.status_code == 204
    assert response.content == b''