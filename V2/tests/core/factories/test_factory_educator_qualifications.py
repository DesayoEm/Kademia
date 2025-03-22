import pytest
from unittest.mock import patch, MagicMock
from uuid import uuid4

from V2.app.core.factories.staff_organization.qualification import QualificationsFactory
from V2.app.schemas.staff_organization.educator_qualification import QualificationCreate, QualificationUpdate, QualificationFilterParams
from V2.app.database.models.enums import ArchiveReason
from V2.app.core.errors.database_errors import EntityNotFoundError, UniqueViolationError
from V2.app.core.errors.staff_organisation_errors import QualificationNotFoundError, DuplicateQualificationError


@pytest.fixture
def mock_repository():
    with patch("V2.app.core.factories.staff_organization.qualification.SQLAlchemyRepository") as mock:
        mock_instance = MagicMock()
        mock.return_value = mock_instance

        test_uuid = uuid4()
        educator_id = uuid4()
        qualification_model = MagicMock()
        qualification_model.id = test_uuid
        qualification_model.educator_id = educator_id
        qualification_model.name = "Test Qualification"
        qualification_model.description = "Test Description"
        qualification_model.manager_id = None

        mock_instance.create.return_value = qualification_model
        mock_instance.get_by_id.return_value = qualification_model
        mock_instance.execute_query.return_value = [qualification_model]
        mock_instance.update.return_value = qualification_model
        mock_instance.archive.return_value = qualification_model
        mock_instance.delete.return_value = None
        mock_instance.execute_archive_query.return_value = [qualification_model]
        mock_instance.get_archive_by_id.return_value = qualification_model
        mock_instance.restore.return_value = qualification_model
        mock_instance.delete_archive.return_value = None

        yield mock_instance, test_uuid, qualification_model


def test_create_qualification(mock_repository):
    """Test the factory create_qualification method"""
    mock_instance, _, _ = mock_repository
    session_mock = MagicMock()

    with patch("V2.app.core.factories.staff_organization.qualification.StaffOrganizationValidators") as validator_mock:
        validator_instance = MagicMock()
        educator_id = uuid4()
        validator_mock.return_value = validator_instance

        validator_instance.validate_name = lambda x: x

        factory = QualificationsFactory(session_mock)
        create_data = QualificationCreate(
            educator_id = educator_id,
            name="New qualification",
            description="New Description"
        )

        result = factory.create_qualification(create_data)
        assert mock_instance.create.called
        assert result.name == "Test Qualification"

def create_qualification_duplicate_error(mock_repository):
    """Test duplicate qualification error handling"""
    mock_instance, _, _ = mock_repository

    unique_error = DuplicateQualificationError(
        input_value = "New qualification", detail = "None", field = "name")
    mock_instance.create.side_effect = unique_error

    session_mock = MagicMock()

    with patch("V2.app.core.factories.staff_organization.qualification.StaffOrganizationValidators") as validator_mock:
        validator_instance = MagicMock()
        educator_id = uuid4()
        validator_mock.return_value = validator_instance
        validator_instance.validate_name = lambda x: x

        factory = QualificationsFactory(session_mock)
        create_data = QualificationCreate(
            educator_id = educator_id,
            name="New qualification",
            description="New qualification"
        )
        with pytest.raises(DuplicateQualificationError):
            factory.create_qualification(create_data)

def test_get_all_qualifications(mock_repository):
    """Test getting all qualifications"""
    mock_instance, _, qualification_model = mock_repository

    session_mock = MagicMock()
    with patch("V2.app.core.factories.staff_organization.qualification.StaffOrganizationValidators"):
        factory = QualificationsFactory(session_mock)

        filters = QualificationFilterParams()
        results = factory.get_all_qualifications(filters)

        mock_instance.execute_query.assert_called_once()
        call_args = mock_instance.execute_query.call_args[0]
        assert call_args[0] == ['name', 'description']
        assert call_args[1] == filters

        assert len(results) == 1
        assert results[0].name == "Test Qualification"

def test_get_qualification(mock_repository):
    """Test getting a specific qualification"""
    mock_instance, test_uuid, _ = mock_repository

    session_mock = MagicMock()
    with patch("V2.app.core.factories.staff_organization.qualification.StaffOrganizationValidators"):
        factory = QualificationsFactory(session_mock)

        result = factory.get_qualification(test_uuid)

        mock_instance.get_by_id.assert_called_once_with(test_uuid)
        assert result.name == "Test Qualification"

def test_get_qualification_not_found(mock_repository):
    """Test getting a non-existent qualification"""
    mock_instance, test_uuid, _ = mock_repository
    mock_instance.get_by_id.side_effect = QualificationNotFoundError(id=test_uuid)

    session_mock = MagicMock()
    with patch("V2.app.core.factories.staff_organization.qualification.StaffOrganizationValidators"):
        factory = QualificationsFactory(session_mock)
        with pytest.raises(QualificationNotFoundError):
            factory.get_qualification(test_uuid)

def test_update_qualification(mock_repository):
    """Test updating a qualification"""
    mock_instance, test_uuid, qualification_model = mock_repository

    updated_qualification = MagicMock()
    updated_qualification.name = "Updated qualification"
    updated_qualification.description = "Updated Description"
    mock_instance.update.return_value = updated_qualification

    session_mock = MagicMock()
    with patch("V2.app.core.factories.staff_organization.qualification.StaffOrganizationValidators") as validator_mock:
        validator_instance = MagicMock()
        validator_mock.return_value = validator_instance
        validator_instance.validate_name = lambda x: x

        factory = QualificationsFactory(session_mock)

        update_data = {
            "name": "Updated qualification",
            "description": "Updated Description"
        }

        result = factory.update_qualification(test_uuid, update_data)
        mock_instance.update.assert_called_once()
        assert result.name == "Updated qualification"

def test_update_qualification_not_found(mock_repository):
    """Test updating a non-existent qualification"""
    mock_instance, test_uuid, _ = mock_repository
    mock_instance.get_by_id.side_effect = EntityNotFoundError(
        entity_type="EducatorQualifications")

    session_mock = MagicMock()
    with patch("V2.app.core.factories.staff_organization.qualification.StaffOrganizationValidators"):
        factory = QualificationsFactory(session_mock)

        update_data = {
            "name": "Updated qualification",
            "description": "Updated Description"
        }

        with pytest.raises(QualificationNotFoundError):
            factory.update_qualification(test_uuid, update_data)

def test_update_qualification_duplicate(mock_repository):
    """Test updating a qualification with a duplicate name"""
    mock_instance, test_uuid, _ = mock_repository

    unique_error = DuplicateQualificationError(
        input_value = "New qualification", detail = "None", field = "name")
    mock_instance.update.side_effect = unique_error

    session_mock = MagicMock()
    with patch("V2.app.core.factories.staff_organization.qualification.StaffOrganizationValidators") as validator_mock:
        validator_instance = MagicMock()
        validator_mock.return_value = validator_instance
        validator_instance.validate_name = lambda x: x

        factory = QualificationsFactory(session_mock)

        update_data = {
            "name": "Updated qualification",
            "description": "Updated Description"
        }
        with pytest.raises(DuplicateQualificationError):
            factory.update_qualification(test_uuid, update_data)

def test_archive_qualification(mock_repository):
    """Test archiving a qualification"""
    mock_instance, test_uuid, _ = mock_repository

    archived_qualification = MagicMock()
    archived_qualification.name = "Test qualification"
    archived_qualification.is_archived = True
    mock_instance.archive.return_value = archived_qualification

    session_mock = MagicMock()
    with patch("V2.app.core.factories.staff_organization.qualification.StaffOrganizationValidators"):
        factory = QualificationsFactory(session_mock)

        reason = ArchiveReason.ADMINISTRATIVE
        result = factory.archive_qualification(test_uuid, reason)

        mock_instance.archive.assert_called_once()

        assert result.name == "Test qualification"
        assert result.is_archived == True

def test_archive_qualification_not_found(mock_repository):
    """Test archiving a non-existent qualification"""
    mock_instance, test_uuid, _ = mock_repository
    mock_instance.archive.side_effect = EntityNotFoundError(entity_type="EducatorQualifications")

    session_mock = MagicMock()
    with patch("V2.app.core.factories.staff_organization.qualification.StaffOrganizationValidators"):
        factory = QualificationsFactory(session_mock)

        reason = ArchiveReason.ADMINISTRATIVE
        with pytest.raises(QualificationNotFoundError):
            factory.archive_qualification(test_uuid, reason)

def test_delete_qualification(mock_repository):
    """Test deleting a qualification"""
    mock_instance, test_uuid, _ = mock_repository

    session_mock = MagicMock()
    with patch("V2.app.core.factories.staff_organization.qualification.StaffOrganizationValidators"):
        factory = QualificationsFactory(session_mock)

        factory.delete_qualification(test_uuid)
        mock_instance.delete.assert_called_once_with(test_uuid)

def test_delete_qualification_not_found(mock_repository):
    """Test deleting a non-existent qualification"""
    mock_instance, test_uuid, _ = mock_repository

    mock_instance.delete.side_effect = EntityNotFoundError(
        entity_type="EducatorQualifications")

    session_mock = MagicMock()
    with patch("V2.app.core.factories.staff_organization.qualification.StaffOrganizationValidators"):
        factory = QualificationsFactory(session_mock)

        with pytest.raises(QualificationNotFoundError):
            factory.delete_qualification(test_uuid)

def test_get_all_archived_qualifications(mock_repository):
    """Test getting all archived qualifications"""
    mock_instance, _, qualification_model = mock_repository

    session_mock = MagicMock()
    with patch("V2.app.core.factories.staff_organization.qualification.StaffOrganizationValidators"):
        factory = QualificationsFactory(session_mock)

        filters = QualificationFilterParams()
        results = factory.get_all_archived_qualifications(filters)
        mock_instance.execute_archive_query.assert_called_once()
        call_args = mock_instance.execute_archive_query.call_args[0]
        assert call_args[0] == ['name', 'description']
        assert call_args[1] == filters

        assert len(results) == 1
        assert results[0].name == "Test Qualification"

def test_get_archived_qualification(mock_repository):
    """Test getting a specific archived qualification"""
    mock_instance, test_uuid, _ = mock_repository

    session_mock = MagicMock()
    with patch("V2.app.core.factories.staff_organization.qualification.StaffOrganizationValidators"):
        factory = QualificationsFactory(session_mock)

        result = factory.get_archived_qualification(test_uuid)
        mock_instance.get_archive_by_id.assert_called_once_with(test_uuid)

        assert result.name == "Test Qualification"

def test_get_archived_qualification_not_found(mock_repository):
    """Test getting a non-existent archived qualification"""
    mock_instance, test_uuid, _ = mock_repository

    mock_instance.get_archive_by_id.side_effect = EntityNotFoundError(
        entity_type="EducatorQualifications")

    session_mock = MagicMock()
    with patch("V2.app.core.factories.staff_organization.qualification.StaffOrganizationValidators"):
        factory = QualificationsFactory(session_mock)

        with pytest.raises(QualificationNotFoundError):
            factory.get_archived_qualification(test_uuid)

def test_restore_qualification(mock_repository):
    """Test restoring an archived qualification"""
    mock_instance, test_uuid, _ = mock_repository

    session_mock = MagicMock()
    with patch("V2.app.core.factories.staff_organization.qualification.StaffOrganizationValidators"):
        factory = QualificationsFactory(session_mock)

        result = factory.restore_qualification(test_uuid)

        mock_instance.restore.assert_called_once_with(test_uuid)
        assert result.name == "Test Qualification"

def test_restore_qualification_not_found(mock_repository):
    """Test restoring a non-existent archived qualification"""
    mock_instance, test_uuid, _ = mock_repository

    mock_instance.get_archive_by_id.side_effect = EntityNotFoundError(
        entity_type="EducatorQualifications")

    session_mock = MagicMock()
    with patch("V2.app.core.factories.staff_organization.qualification.StaffOrganizationValidators"):
        factory = QualificationsFactory(session_mock)

        with pytest.raises(QualificationNotFoundError):
            factory.restore_qualification(test_uuid)

def test_delete_archived_qualification(mock_repository):
    """Test deleting an archived qualification"""
    mock_instance, test_uuid, _ = mock_repository

    session_mock = MagicMock()
    with patch("V2.app.core.factories.staff_organization.qualification.StaffOrganizationValidators"):
        factory = QualificationsFactory(session_mock)

        factory.delete_archived_qualification(test_uuid)
        mock_instance.delete_archive.assert_called_once_with(test_uuid)

def test_delete_archived_qualification_not_found(mock_repository):
    """Test deleting a non-existent archived qualification"""
    mock_instance, test_uuid, _ = mock_repository

    mock_instance.delete_archive.side_effect = EntityNotFoundError(
        entity_type="EducatorQualifications")

    session_mock = MagicMock()
    with patch("V2.app.core.factories.staff_organization.qualification.StaffOrganizationValidators"):
        factory = QualificationsFactory(session_mock)
        with pytest.raises(QualificationNotFoundError):
            factory.delete_archived_qualification(test_uuid)
