from typing import Dict, Tuple, Any
from app.core.transfer.models.transfer import DepartmentTransfer

class TransferGatherer:
    """Gathers data for auth entities"""


    @staticmethod
    def gather_student_department_transfer_data(transfer: DepartmentTransfer) -> Tuple[Dict[str, Any], str]:
        """Gather data for StudentDepartmentTransfer entity."""
        file_name = f"DepartmentTransfer_{transfer.student_id}_{transfer.academic_year}"

        return ({
                    "department_transfer": {
                        "id": str(transfer.id),
                        "student_id": str(transfer.student_id),
                        "academic_year": transfer.academic_year,
                        "previous_level_id": str(transfer.previous_level_id),
                        "new_level_id": str(transfer.new_level_id),
                        "previous_class_id": str(transfer.previous_class_id),
                        "new_class_id": str(transfer.new_class_id),
                        "previous_department_id": str(transfer.previous_department_id),
                        "new_department_id": str(transfer.new_department_id),
                        "reason": transfer.reason,
                        "status": transfer.status,
                        "status_updated_by": str(transfer.status_updated_by) if transfer.status_updated_by else None,
                        "status_updated_at": transfer.status_updated_at,
                        "rejection_reason": transfer.rejection_reason,
                        "created_at": transfer.created_at,
                        "created_by": str(transfer.created_by) if transfer.created_by else None,
                        "last_modified_at": transfer.last_modified_at,
                        "last_modified_by": str(transfer.last_modified_by) if transfer.last_modified_by else None,
                        "archived_at": transfer.archived_at,
                        "archived_by": str(transfer.archived_by) if transfer.archived_by else None,
                        "archive_reason": transfer.archive_reason,
                    },
                    "student": {
                        "id": str(transfer.transferred_student.id),
                        "name": f"{transfer.transferred_student.first_name} {transfer.transferred_student.last_name}"
                    } if transfer.transferred_student else None,
                    "previous_level": {
                        "id": str(transfer.previous_level_rel.id),
                        "name": transfer.previous_level_rel.name
                    } if transfer.previous_level_rel else None,
                    "new_level": {
                        "id": str(transfer.new_level_rel.id),
                        "name": transfer.new_level_rel.name
                    } if transfer.new_level_rel else None,
                    "previous_class": {
                        "id": str(transfer.former_class_rel.id),
                        "code": transfer.former_class_rel.code
                    } if transfer.former_class_rel else None,
                    "new_class": {
                        "id": str(transfer.new_class_rel.id),
                        "code": transfer.new_class_rel.code
                    } if transfer.new_class_rel else None,
                    "previous_department": {
                        "id": str(transfer.former_dept.id),
                        "name": transfer.former_dept.name
                    } if transfer.former_dept else None,
                    "new_department": {
                        "id": str(transfer.new_dept.id),
                        "name": transfer.new_dept.name
                    } if transfer.new_dept else None,
                    "status_updated_by": {
                        "id": str(transfer.status_changer.id),
                        "name": f"{transfer.status_changer.first_name} {transfer.status_changer.last_name}"
                    } if transfer.status_changer else None
                }, file_name)
