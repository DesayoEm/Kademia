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
            Staff: self.gather_staff_data
        }

        entity_type = type(entity)
        gather_function = gatherers.get(entity_type)

        if not gather_function:
            raise UnimplementedGathererError(entity=entity_type.__name__)

        return gather_function(entity)

    @staticmethod
    def gather_staff_data(staff: Staff) -> tuple:
        """Gather data for Staff entity."""

        access_changes = staff.access_changes
        file_name = f"Staff_{staff.first_name}_{staff.last_name}"

        return ({
            "staff_member": {
                "id": str(staff.id),
                "full_name": f"{staff.first_name} {staff.last_name}",
                "user_type": staff.user_type,
                "status": staff.status,
                "staff_type": staff.staff_type,
                "image_url": staff.image_url,
                "email_address": staff.email_address,
                "address": staff.address,
                "phone": staff.phone,
                "department_id": staff.department_id,
                "role_id": staff.role_id,
                "date_joined": staff.date_joined,
                "date_left": staff.date_left,
                "created_by": staff.created_by_staff,
                "created_at": staff.created_at,
                "last_modified_at": staff.last_modified_at,
                "last_modified_by": staff.last_modified_by_staff,
            },
            "access_changes": [
                {
                    "id": str(access_change.id),
                    "previous_level": access_change.previous_level,
                    "new_level": access_change.new_level,
                    "reason": access_change.reason,
                    "changed_at": access_change.changed_at,
                    "changed_by_id": str(access_change.changed_by_id),
                }
                for access_change in access_changes
            ],
                 "total_access_changes": len(access_changes)

                },

            file_name)

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