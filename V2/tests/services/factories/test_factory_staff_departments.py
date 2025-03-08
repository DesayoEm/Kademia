import pytest
from unittest.mock import patch, MagicMock
from uuid import uuid4

from V2.app.services.staff_organization.factories.staff_departments import StaffDepartmentsFactory
from V2.app.schemas.staff_organization.staff_departments import StaffDepartmentCreate

# Mock the repository layer
@pytest.fixture
def mock_repository():
    with patch("V2.app.services.staff_organization.factories.staff_departments.SQLAlchemyRepository") as mock:
        mock_instance = MagicMock()
        mock.return_value = mock_instance

        # Create test response data
        test_uuid = uuid4()
        department_model = MagicMock()
        department_model.id = test_uuid
        department_model.name = "Test Department"
        department_model.description = "Test Description"
        department_model.manager_id = None

        # Mock repository methods
        mock_instance.create.return_value = department_model
        mock_instance.get_by_id.return_value = department_model
        mock_instance.execute_query.return_value = [department_model]
        mock_instance.update.return_value = department_model
        mock_instance.archive.return_value = department_model
        mock_instance.delete.return_value = None

        yield mock_instance, test_uuid

def test_create_staff_department(mock_repository):
    """Test the factory create_staff_department method"""
    mock_instance, _ = mock_repository

    # Create a session mock (not used but needed for initialization)
    session_mock = MagicMock()

    # Create the validator mock to avoid validation issues
    with patch("V2.app.services.staff_organization.factories.staff_departments.StaffOrganizationValidators") as validator_mock:
        validator_instance = MagicMock()
        validator_mock.return_value = validator_instance

        # Make validate_name return the input (passthrough)
        validator_instance.validate_name = lambda x: x

        # Initialize the factory
        factory = StaffDepartmentsFactory(session_mock)

        # Create test data
        create_data = StaffDepartmentCreate(
            name="New Department",
            description="New Description"
        )

        # Call the method under test
        result = factory.create_staff_department(create_data)

        # Verify the repository was called with the right data
        assert mock_instance.create.called

        # Verify the result
        assert result.name == "Test Department"