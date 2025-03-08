import pytest
from unittest.mock import patch, MagicMock
from uuid import uuid4

from V2.app.crud.staff_organization.staff_departments import StaffDepartmentCrud
from V2.app.schemas.staff_organization.staff_departments import StaffDepartmentCreate, StaffDepartmentUpdate

@pytest.fixture
def mock_factory():
    with patch("V2.app.crud.staff_organization.staff_departments.StaffDepartmentsFactory") as mock:
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
        mock_instance.update_staff_department.return_value = factory_response
        mock_instance.archive_department.return_value = factory_response
        mock_instance.delete_department.return_value = None

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
