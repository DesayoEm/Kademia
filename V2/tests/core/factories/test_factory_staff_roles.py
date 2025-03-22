import pytest
from unittest.mock import patch, MagicMock
from uuid import uuid4

from V2.app.core.factories.staff_organization.role import StaffRolesFactory
from V2.app.schemas.staff_organization.role import StaffRoleCreate, StaffRoleUpdate, RolesFilterParams
from V2.app.database.models.data_enums import ArchiveReason
from V2.app.core.errors.database_errors import EntityNotFoundError, UniqueViolationError
from V2.app.core.errors.staff_organisation_errors import RoleNotFoundError, DuplicateRoleError


@pytest.fixture
def mock_repository():
    with patch("V2.app.core.factories.staff_organization.role.SQLAlchemyRepository") as mock:
        mock_instance = MagicMock()
        mock.return_value = mock_instance

        test_uuid = uuid4()
        role_model = MagicMock()
        role_model.id = test_uuid
        role_model.name = "Test Role"
        role_model.description = "Test Description"
        role_model.manager_id = None

        mock_instance.create.return_value = role_model
        mock_instance.get_by_id.return_value = role_model
        mock_instance.execute_query.return_value = [role_model]
        mock_instance.update.return_value = role_model
        mock_instance.archive.return_value = role_model
        mock_instance.delete.return_value = None
        mock_instance.execute_archive_query.return_value = [role_model]
        mock_instance.get_archive_by_id.return_value = role_model
        mock_instance.restore.return_value = role_model
        mock_instance.delete_archive.return_value = None

        yield mock_instance, test_uuid, role_model


def test_create_staff_role(mock_repository):
    """Test the factory create_role method"""
    mock_instance, _, _ = mock_repository
    session_mock = MagicMock()

    with patch("V2.app.core.factories.staff_organization.role.StaffOrganizationValidators") as validator_mock:
        validator_instance = MagicMock()
        validator_mock.return_value = validator_instance

        validator_instance.validate_name = lambda x: x

        factory = StaffRolesFactory(session_mock)
        create_data = StaffRoleCreate(
            name="New Role",
            description="New Description"
        )

        result = factory.create_role(create_data)
        assert mock_instance.create.called
        assert result.name == "Test Role"

def create_role_duplicate_error(mock_repository):
    """Test duplicate role error handling"""
    mock_instance, _, _ = mock_repository

    unique_error = UniqueViolationError(field_name="name")
    mock_instance.create.side_effect = unique_error

    session_mock = MagicMock()

    with patch("V2.app.core.factories.staff_organization.role.StaffOrganizationValidators") as validator_mock:
        validator_instance = MagicMock()
        validator_mock.return_value = validator_instance
        validator_instance.validate_name = lambda x: x

        factory = StaffRolesFactory(session_mock)
        create_data = StaffRoleCreate(
            name="New Role",
            description="New Role"
        )
        with pytest.raises(DuplicateRoleError):
            factory.create_role(create_data)

def test_get_all_roles(mock_repository):
    """Test getting all roles"""
    mock_instance, _, role_model = mock_repository

    session_mock = MagicMock()
    with patch("V2.app.core.factories.staff_organization.role.StaffOrganizationValidators"):
        factory = StaffRolesFactory(session_mock)

        filters = RolesFilterParams()
        results = factory.get_all_roles(filters)

        mock_instance.execute_query.assert_called_once()
        call_args = mock_instance.execute_query.call_args[0]
        assert call_args[0] == ['name', 'description']
        assert call_args[1] == filters

        assert len(results) == 1
        assert results[0].name == "Test Role"

def test_get_staff_role(mock_repository):
    """Test getting a specific role"""
    mock_instance, test_uuid, _ = mock_repository

    session_mock = MagicMock()
    with patch("V2.app.core.factories.staff_organization.role.StaffOrganizationValidators"):
        factory = StaffRolesFactory(session_mock)

        result = factory.get_role(test_uuid)

        mock_instance.get_by_id.assert_called_once_with(test_uuid)
        assert result.name == "Test Role"

def test_get_staff_role_not_found(mock_repository):
    """Test getting a non-existent role"""
    mock_instance, test_uuid, _ = mock_repository
    mock_instance.get_by_id.side_effect = EntityNotFoundError(entity_type="Staffroles")

    session_mock = MagicMock()
    with patch("V2.app.core.factories.staff_organization.role.StaffOrganizationValidators"):
        factory = StaffRolesFactory(session_mock)
        with pytest.raises(RoleNotFoundError):
            factory.get_role(test_uuid)

def test_update_staff_role(mock_repository):
    """Test updating a role"""
    mock_instance, test_uuid, role_model = mock_repository

    updated_role = MagicMock()
    updated_role.name = "Updated role"
    updated_role.description = "Updated Description"
    mock_instance.update.return_value = updated_role

    session_mock = MagicMock()
    with patch("V2.app.core.factories.staff_organization.role.StaffOrganizationValidators") as validator_mock:
        validator_instance = MagicMock()
        validator_mock.return_value = validator_instance
        validator_instance.validate_name = lambda x: x

        factory = StaffRolesFactory(session_mock)

        update_data = {
            "name": "Updated role",
            "description": "Updated Description"
        }

        result = factory.update_role(test_uuid, update_data)
        mock_instance.update.assert_called_once()
        assert result.name == "Updated role"

def test_update_staff_role_not_found(mock_repository):
    """Test updating a non-existent role"""
    mock_instance, test_uuid, _ = mock_repository
    mock_instance.get_by_id.side_effect = EntityNotFoundError(entity_type="StaffRoles")

    session_mock = MagicMock()
    with patch("V2.app.core.factories.staff_organization.role.StaffOrganizationValidators"):
        factory = StaffRolesFactory(session_mock)

        update_data = {
            "name": "Updated role",
            "description": "Updated Description"
        }

        with pytest.raises(RoleNotFoundError):
            factory.update_role(test_uuid, update_data)

def test_update_staff_role_duplicate(mock_repository):
    """Test updating a role with a duplicate name"""
    mock_instance, test_uuid, _ = mock_repository

    unique_error = DuplicateRoleError(input_value ="Updated role", field="name", detail = "None")
    mock_instance.update.side_effect = unique_error

    session_mock = MagicMock()
    with patch("V2.app.core.factories.staff_organization.role.StaffOrganizationValidators") as validator_mock:
        validator_instance = MagicMock()
        validator_mock.return_value = validator_instance
        validator_instance.validate_name = lambda x: x

        factory = StaffRolesFactory(session_mock)

        update_data = {
            "name": "Updated role",
            "description": "Updated Description"
        }
        with pytest.raises(DuplicateRoleError):
            factory.update_role(test_uuid, update_data)

def test_archive_role(mock_repository):
    """Test archiving a role"""
    mock_instance, test_uuid, _ = mock_repository

    archived_role = MagicMock()
    archived_role.name = "Test Role"
    archived_role.is_archived = True
    mock_instance.archive.return_value = archived_role

    session_mock = MagicMock()
    with patch("V2.app.core.factories.staff_organization.role.StaffOrganizationValidators"):
        factory = StaffRolesFactory(session_mock)

        reason = ArchiveReason.ADMINISTRATIVE
        result = factory.archive_role(test_uuid, reason)

        mock_instance.archive.assert_called_once()

        assert result.name == "Test Role"
        assert result.is_archived == True

def test_archive_role_not_found(mock_repository):
    """Test archiving a non-existent role"""
    mock_instance, test_uuid, _ = mock_repository
    mock_instance.archive.side_effect = EntityNotFoundError(entity_type="StaffRoles")

    session_mock = MagicMock()
    with patch("V2.app.core.factories.staff_organization.role.StaffOrganizationValidators"):
        factory = StaffRolesFactory(session_mock)

        reason = ArchiveReason.ADMINISTRATIVE
        with pytest.raises(RoleNotFoundError):
            factory.archive_role(test_uuid, reason)

def test_delete_role(mock_repository):
    """Test deleting a role"""
    mock_instance, test_uuid, _ = mock_repository

    session_mock = MagicMock()
    with patch("V2.app.core.factories.staff_organization.role.StaffOrganizationValidators"):
        factory = StaffRolesFactory(session_mock)

        factory.delete_role(test_uuid)
        mock_instance.delete.assert_called_once_with(test_uuid)

def test_delete_role_not_found(mock_repository):
    """Test deleting a non-existent role"""
    mock_instance, test_uuid, _ = mock_repository

    mock_instance.delete.side_effect = EntityNotFoundError(entity_type="StaffRoles")

    session_mock = MagicMock()
    with patch("V2.app.core.factories.staff_organization.role.StaffOrganizationValidators"):
        factory = StaffRolesFactory(session_mock)

        with pytest.raises(RoleNotFoundError):
            factory.delete_role(test_uuid)

def test_get_all_archived_roles(mock_repository):
    """Test getting all archived roles"""
    mock_instance, _, role_model = mock_repository

    session_mock = MagicMock()
    with patch("V2.app.core.factories.staff_organization.role.StaffOrganizationValidators"):
        factory = StaffRolesFactory(session_mock)

        filters = RolesFilterParams()
        results = factory.get_all_archived_roles(filters)
        mock_instance.execute_archive_query.assert_called_once()
        call_args = mock_instance.execute_archive_query.call_args[0]
        assert call_args[0] == ['name', 'description']
        assert call_args[1] == filters

        assert len(results) == 1
        assert results[0].name == "Test Role"

def test_get_archived_role(mock_repository):
    """Test getting a specific archived role"""
    mock_instance, test_uuid, _ = mock_repository

    session_mock = MagicMock()
    with patch("V2.app.core.factories.staff_organization.role.StaffOrganizationValidators"):
        factory = StaffRolesFactory(session_mock)

        result = factory.get_archived_role(test_uuid)
        mock_instance.get_archive_by_id.assert_called_once_with(test_uuid)

        assert result.name == "Test Role"

def test_get_archived_role_not_found(mock_repository):
    """Test getting a non-existent archived role"""
    mock_instance, test_uuid, _ = mock_repository

    mock_instance.get_archive_by_id.side_effect = EntityNotFoundError(entity_type="StaffRoles")

    session_mock = MagicMock()
    with patch("V2.app.core.factories.staff_organization.role.StaffOrganizationValidators"):
        factory = StaffRolesFactory(session_mock)

        with pytest.raises(RoleNotFoundError):
            factory.get_archived_role(test_uuid)

def test_restore_role(mock_repository):
    """Test restoring an archived role"""
    mock_instance, test_uuid, _ = mock_repository

    session_mock = MagicMock()
    with patch("V2.app.core.factories.staff_organization.role.StaffOrganizationValidators"):
        factory = StaffRolesFactory(session_mock)

        result = factory.restore_role(test_uuid)

        mock_instance.restore.assert_called_once_with(test_uuid)
        assert result.name == "Test Role"

def test_restore_role_not_found(mock_repository):
    """Test restoring a non-existent archived role"""
    mock_instance, test_uuid, _ = mock_repository

    mock_instance.get_archive_by_id.side_effect = EntityNotFoundError(entity_type="StaffRoles")

    session_mock = MagicMock()
    with patch("V2.app.core.factories.staff_organization.role.StaffOrganizationValidators"):
        factory = StaffRolesFactory(session_mock)

        with pytest.raises(RoleNotFoundError):
            factory.restore_role(test_uuid)

def test_delete_archived_role(mock_repository):
    """Test deleting an archived role"""
    mock_instance, test_uuid, _ = mock_repository

    session_mock = MagicMock()
    with patch("V2.app.core.factories.staff_organization.role.StaffOrganizationValidators"):
        factory = StaffRolesFactory(session_mock)

        factory.delete_archived_role(test_uuid)
        mock_instance.delete_archive.assert_called_once_with(test_uuid)

def test_delete_archived_role_not_found(mock_repository):
    """Test deleting a non-existent archived role"""
    mock_instance, test_uuid, _ = mock_repository

    mock_instance.delete_archive.side_effect = EntityNotFoundError(entity_type="StaffRoles")

    session_mock = MagicMock()
    with patch("V2.app.core.factories.staff_organization.role.StaffOrganizationValidators"):
        factory = StaffRolesFactory(session_mock)
        with pytest.raises(RoleNotFoundError):
            factory.delete_archived_role(test_uuid)
