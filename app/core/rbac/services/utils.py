from sqlalchemy.orm import Session
from app.core.shared.exceptions import NegativeRankError, EntityNotFoundError


class RBACUtils:
    """
    Utility functions for RBAC operations.

    Provides static helper methods for validation and string generation
    used across the RBAC module. Stateless—no database access required.
    """
    def __init__(self):
        """
        Initialize RBACUtils.

        No dependencies required; all methods are static.
        """

    @staticmethod
    def validate_rank_number(value: int) -> int:
        """
        Validate that a role rank is non-negative.

        Role ranks are used for hierarchy comparisons (e.g., determining if
        one role outranks another). Negative ranks are not permitted.

        Args:
            value: The rank integer to validate.

        Returns:
            int: The validated rank value (unchanged) if valid.

        Raises:
            NegativeRankError: If value is less than 0.
        """
        if value < 0:
            raise NegativeRankError(value=value)
        return value

    @staticmethod
    def generate_permission_str(resource_name: str, action_name: str) -> str:
        """
        Generate a standardized permission name from resource and action.

        Combines resource and action into an uppercase permission identifier
        following the naming convention "RESOURCE_ACTION".

        Args:
            resource_name: The resource identifier (e.g., "students", "grades").
            action_name: The action identifier (e.g., "read", "update", "delete").

        Returns:
            str: The formatted permission string (e.g., "STUDENTS_READ").

        Example:
            perm = RBACUtils.generate_permission_str("grades", "update")
            # Returns "GRADES_UPDATE"
        """
        permission_name = f"{(resource_name + '_' + action_name).upper}"
        return permission_name
