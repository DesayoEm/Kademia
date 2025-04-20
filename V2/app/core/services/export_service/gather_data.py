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
            AdminStaff: self.gather_admin_staff_data,
            SupportStaff: self.gather_support_staff_data,
            Educator: self.gather_educator_data
        }

        entity_type = type(entity)
        gather_function = gatherers.get(entity_type)

        if not gather_function:
            raise UnimplementedGathererError(entity=entity_type.__name__)

        return gather_function(entity)

    @staticmethod
    def gather_admin_staff_data(staff: AdminStaff) -> tuple:
        """Gather data for Admin Staff entity."""

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
    def gather_support_staff_data(staff: SupportStaff) -> tuple:
        """Gather data for support Staff entity."""

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
    def gather_educator_data(educator: Educator) -> tuple:
        """Gather data for Staff entity."""

        access_changes = educator.access_changes
        file_name = f"Staff_{educator.first_name}_{educator.last_name}"
        qualifications = educator.qualifications
        subject_assignments = educator.subject_assignments
        mentored_department = educator.mentored_department
        supervised_class = educator.supervised_class
        return ({
                    "staff_member": {
                        "id": str(educator.id),
                        "full_name": f"{educator.first_name} {educator.last_name}",
                        "user_type": educator.user_type,
                        "status": educator.status,
                        "staff_type": educator.staff_type,
                        "image_url": educator.image_url,
                        "email_address": educator.email_address,
                        "address": educator.address,
                        "phone": educator.phone,
                        "department_id": educator.department_id,
                        "role_id": educator.role_id,
                        "date_joined": educator.date_joined,
                        "date_left": educator.date_left,
                        "created_by": educator.created_by_staff,
                        "created_at": educator.created_at,
                        "last_modified_at": educator.last_modified_at,
                        "last_modified_by": educator.last_modified_by_staff,
                    },
                    "mentored_department": educator.mentored_department,
                    "supervised_class =": educator.supervised_class,

                    "qualifications": [
                        {
                            "id": str(qualification.id),
                            "name": qualification.name,
                            "description": qualification.description,
                            "validity_type": qualification.validity_type,
                            "valid_until": qualification.valid_until

                        } for qualification in qualifications],

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

                    "total_access_changes": len(access_changes),

                    "subject_assignments": [
                    {
                        "id": str(assignment.id),
                        "subject_id": assignment.subject_id,
                        "level_id": assignment.level_id,
                        "academic_year": assignment.academic_year,
                        "term": assignment.term,
                        "is_active": assignment.is_active,
                        "date_assigned": assignment.date_assigned,

                    }for assignment in subject_assignments],

                    "total_assignments ": len(subject_assignments),

        }, file_name)


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