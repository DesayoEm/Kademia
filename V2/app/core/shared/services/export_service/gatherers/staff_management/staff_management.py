from typing import Dict, Tuple, Any
from V2.app.core.shared.database.models import (
     EducatorQualification, StaffDepartment, StaffRole
 )

class StaffOrganizationGatherer:
    """Gathers data for staff organization entities including departments, roles, and qualifications"""

    @staticmethod
    def gather_qualification_data(qualification: EducatorQualification) -> Tuple[Dict[str, Any], str]:
        """Gather data for EducatorQualification entity."""
        file_name = f"Qualification_{qualification.name}"

        return ({
                    "qualification": {
                        "id": str(qualification.id),
                        "name": qualification.name,
                        "description": qualification.description,
                        "validity_type": qualification.validity_type,
                        "valid_until": qualification.valid_until,
                        "created_at": qualification.created_at,
                        "created_by": str(qualification.created_by) if qualification.created_by else None,
                        "last_modified_at": qualification.last_modified_at,
                        "last_modified_by": str(
                            qualification.last_modified_by) if qualification.last_modified_by else None,
                    },
                    "educator": {
                        "id": str(qualification.educator.id) if qualification.educator else None,
                        "name": f"{qualification.educator.first_name} {qualification.educator.last_name}" if qualification.educator else None,
                    }
                }, file_name)

    @staticmethod
    def gather_department_data(department: StaffDepartment) -> Tuple[Dict[str, Any], str]:
        """Gather data for StaffDepartment entity."""
        file_name = f"StaffDepartment_{department.name}"

        staff_members = department.staff if hasattr(department, "staff") else []

        return ({
                    "department": {
                        "id": str(department.id),
                        "name": department.name,
                        "description": department.description,
                        "created_at": department.created_at,
                        "created_by": str(department.created_by) if department.created_by else None,
                        "last_modified_at": department.last_modified_at,
                        "last_modified_by": str(department.last_modified_by) if department.last_modified_by else None,
                    },
                    "manager": {
                        "id": str(department.manager.id) if department.manager else None,
                        "name": f"{department.manager.first_name} {department.manager.last_name}" if department.manager else None,
                    },
                    "staff": {
                        "count": len(staff_members),
                        "by_type": {
                            "educator": sum(1 for s in staff_members if s.staff_type == "Educator"),
                            "admin": sum(1 for s in staff_members if s.staff_type == "Admin"),
                            "support": sum(1 for s in staff_members if s.staff_type == "Support"),
                            "system": sum(1 for s in staff_members if s.staff_type == "System"),
                        },
                        "by_status": {
                            "active": sum(1 for s in staff_members if s.status == "ACTIVE"),
                            "left": sum(1 for s in staff_members if s.status == "LEFT"),
                        },
                        "by_availability": {
                            "available": sum(1 for s in staff_members if s.availability == "AVAILABLE"),
                            "unavailable": sum(1 for s in staff_members if s.availability == "UNAVAILABLE"),
                        }
                    }
                }, file_name)

    @staticmethod
    def gather_role_data(role: StaffRole) -> Tuple[Dict[str, Any], str]:
        """Gather data for StaffRole entity."""
        file_name = f"StaffRole_{role.name}"

        staff_members = role.staff if hasattr(role, "staff") else []

        return ({
                    "role": {
                        "id": str(role.id),
                        "name": role.name,
                        "description": role.description,
                        "created_at": role.created_at,
                        "created_by": str(role.created_by) if role.created_by else None,
                        "last_modified_at": role.last_modified_at,
                        "last_modified_by": str(role.last_modified_by) if role.last_modified_by else None,
                    },
                    "staff": {
                        "count": len(staff_members),
                        "by_type": {
                            "educator": sum(1 for s in staff_members if s.staff_type == "Educator"),
                            "admin": sum(1 for s in staff_members if s.staff_type == "Admin"),
                            "support": sum(1 for s in staff_members if s.staff_type == "Support"),
                            "system": sum(1 for s in staff_members if s.staff_type == "System"),
                        },
                        "by_department": {
                            dept.name: sum(1 for s in staff_members if s.department and s.department.id == dept.id)
                            for dept in set(s.department for s in staff_members if s.department)
                        }
                    },
                    "staff_members": [
                        {
                            "id": str(staff.id),
                            "name": f"{staff.first_name} {staff.last_name}",
                            "email_service": staff.email_address,
                            "phone": staff.phone,
                            "department": staff.department.name if staff.department else None,
                            "joined": str(staff.date_joined),
                        }
                        for staff in staff_members
                    ]
                }, file_name)

