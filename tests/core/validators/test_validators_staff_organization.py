import pytest
from app.core import StaffOrganizationValidators
from app.core import (
    EmptyFieldError, BlankFieldError, TextTooShortError
)

@pytest.fixture
def validator():
    return StaffOrganizationValidators()

class TestValidateName:
    """Tests for the validate_name method"""

    def test_valid_name(self, validator):
        """Test validation of a valid name"""
        result = validator.validate_name("test department")
        assert result == "Test Department"

        result = validator.validate_name("  marketing  ")
        assert result == "Marketing"

    def test_empty_name(self, validator):
        """Test validation with empty name"""
        with pytest.raises(EmptyFieldError):
            validator.validate_name("")

    def test_blank_name(self, validator):
        """Test validation with blank name (only whitespace)"""
        with pytest.raises(BlankFieldError):
            validator.validate_name("   ")

    def test_too_short_name(self, validator):
        """Test validation with name that's too short"""
        with pytest.raises(TextTooShortError):
            validator.validate_name("Ed")

        with pytest.raises(TextTooShortError):
            validator.validate_name("  A  ")

    def test_edge_cases(self, validator):
        """Test edge cases for the name validator"""
        result = validator.validate_name("dev")
        assert result == "Dev"

        result = validator.validate_name("hUmAn ReSOurCeS")
        assert result == "Human Resources"

class TestValidateDescription:
    """Tests for the validate_description method"""

    def test_valid_description(self, validator):
        """Test validation of a valid description"""
        result = validator.validate_description("this is a test description")
        assert result == "This is a test description"

        result = validator.validate_description("  handles marketing tasks  ")
        assert result == "Handles marketing tasks"

    def test_empty_description(self, validator):
        """Test validation with empty description"""
        with pytest.raises(EmptyFieldError):
            validator.validate_description("")

    def test_blank_description(self, validator):
        """Test validation with blank description (only whitespace)"""
        with pytest.raises(BlankFieldError):
            validator.validate_description("   ")

    def test_short_description(self, validator):
        """Test validation with very short description - should pass since no min length"""
        result = validator.validate_description("OK")
        assert result == "Ok"