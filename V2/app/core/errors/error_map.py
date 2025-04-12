from ...database.models import *
from ..errors import *



not_found_map = {
            StaffRole: (RoleNotFoundError, "role")
        }

deletion_dependency_map = {
    StaffRole: (RoleDeletionDependencyError, "role")
}
