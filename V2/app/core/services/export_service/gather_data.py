from uuid import UUID

from ...errors.export_errors import UnimplementedGathererError
from ....database.models import *


class GatherData:
    def __init__(self):
        pass

    def gather(self, entity) -> dict:
        """Dispatch to the correct gather method based on entity type."""

        gatherers = {
            StaffRole: self.gather_role_data,
        }
        entity_type = type(entity)
        gather_function = gatherers.get(entity_type)

        if not gather_function:
            raise UnimplementedGathererError(entity=entity_type.__name__)

        return gather_function(entity)


    @staticmethod
    def gather_role_data(role: StaffRole) -> dict:
        """Gather data for StaffRole entity."""
        staff_assigned = role.staff

        return {
            "role": {
                "id": str(role.id),
                "name": role.name,
                "description": role.description
            },
            "staff_assigned": [
                {
                    "id": str(staff.id),
                    "first_name": staff.first_name,
                    "last_name": staff.last_name,
                    "email": staff.email_address
                }
                for staff in staff_assigned
            ]
        }