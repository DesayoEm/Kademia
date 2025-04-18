from uuid import UUID

from ...errors.export_errors import UnimplementedGathererError
from ....database.models import *

class GatherData:
    def __init__(self):
        pass

    def gather(self, entity) -> tuple:
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
    def gather_role_data(role: StaffRole) -> tuple:
        """Gather data for StaffRole entity."""
        staff_assigned = role.staff_members
        file_name = f"StaffRole_{role.name}"

        return ({
            "role": {
                "id": str(role.id),
                "name": role.name,
                "description": role.description,
                "created_by": role.created_by_staff,
                "created_at": role.created_at,
                "last_modified_at": role.last_modified_at,
                "last_modified_by": role.last_modified_by_staff,
            },
            "staff_assigned": [
                {
                    "id": str(staff.id),
                    "first_name": staff.first_name,
                    "last_name": staff.last_name,
                    "gender": staff.gender,
                    "email": staff.email_address,
                    "access_level": str(staff.access_level),
                    "date_joined": str(staff.date_joined),
                    "date_left": str(staff.date_left),

                }
                for staff in staff_assigned
            ]
        },
            file_name)