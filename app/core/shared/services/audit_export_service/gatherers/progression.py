from typing import Dict, Tuple, Any
from app.core.progression.models.progression import Repetition, Promotion

class ProgressionGatherer:
    """Gathers data for progression entities"""

    @staticmethod
    def gather_repetition_data(repetition: Repetition) -> Tuple[Dict[str, Any], str]:
        """Gather data for Repetition entity."""
        file_name = f"Repetition_{repetition.student_id}_{repetition.academic_session}"

        return ({
                    "repetition": {
                        "id": str(repetition.id),
                        "student_id": str(repetition.student_id),
                        "academic_session": repetition.academic_session,
                        "previous_level_id": str(repetition.previous_level_id),
                        "new_level_id": str(repetition.new_level_id),
                        "previous_class_id": str(repetition.previous_class_id),
                        "new_class_id": str(repetition.new_class_id),
                        "reason": repetition.reason,
                        "status": repetition.status,
                        "status_updated_by": str(
                            repetition.status_updated_by) if repetition.status_updated_by else None,
                        "status_updated_at": repetition.status_updated_at,
                        "rejection_reason": repetition.rejection_reason,
                        "created_at": repetition.created_at,
                        "created_by": str(repetition.created_by) if repetition.created_by else None,
                        "last_modified_at": repetition.last_modified_at,
                        "last_modified_by": str(repetition.last_modified_by) if repetition.last_modified_by else None,
                        "archived_at": repetition.archived_at,
                        "archived_by": str(repetition.archived_by) if repetition.archived_by else None,
                        "archive_reason": repetition.archive_reason,
                    },
                    "student": {
                        "id": str(repetition.repeating_student.id),
                        "name": f"{repetition.repeating_student.first_name} {repetition.repeating_student.last_name}"
                    } if repetition.repeating_student else None,
                    "previous_level": {
                        "id": str(repetition.previous_level.id),
                        "name": repetition.previous_level.name
                    } if repetition.previous_level else None,
                    "new_level": {
                        "id": str(repetition.new_level.id),
                        "name": repetition.new_level.name
                    } if repetition.new_level else None,
                    "previous_class": {
                        "id": str(repetition.previous_class.id),
                        "code": repetition.previous_class.code
                    } if repetition.previous_class else None,
                    "new_class": {
                        "id": str(repetition.new_class.id),
                        "code": repetition.new_class.code
                    } if repetition.new_class else None,
                    "status_updated_by": {
                        "id": str(repetition.status_updated_staff.id),
                        "name": f"{repetition.status_updated_staff.first_name} {repetition.status_updated_staff.last_name}"
                    } if repetition.status_updated_staff else None
                }, file_name)

    @staticmethod
    def gather_promotion_data(promotion: Promotion) -> Tuple[Dict[str, Any], str]:
        """Gather data for promotion entity."""
        file_name = f"promotion_{promotion.student_id}_{promotion.academic_session}"

        return ({
                    "promotion": {
                        "id": str(promotion.id),
                        "student_id": str(promotion.student_id),
                        "academic_session": promotion.academic_session,
                        "previous_level_id": str(promotion.previous_level_id),
                        "new_level_id": str(promotion.new_level_id),
                        "previous_class_id": str(promotion.previous_class_id),
                        "new_class_id": str(promotion.new_class_id),
                        "status": promotion.status,
                        "status_updated_by": str(
                            promotion.status_updated_by) if promotion.status_updated_by else None,
                        "status_updated_at": promotion.status_updated_at,
                        "rejection_reason": promotion.rejection_reason,
                        "created_at": promotion.created_at,
                        "created_by": str(promotion.created_by) if promotion.created_by else None,
                        "last_modified_at": promotion.last_modified_at,
                        "last_modified_by": str(promotion.last_modified_by) if promotion.last_modified_by else None,
                        "archived_at": promotion.archived_at,
                        "archived_by": str(promotion.archived_by) if promotion.archived_by else None,
                        "archive_reason": promotion.archive_reason,
                    },
                    "student": {
                        "id": str(promotion.promoted_student.id),
                        "name": f"{promotion.promoted_student.first_name} {promotion.promoted_student.last_name}"
                    } if promotion.promoted_student else None,
                    "previous_level": {
                        "id": str(promotion.previous_level.id),
                        "name": promotion.previous_level.name
                    } if promotion.previous_level else None,
                    "new_level": {
                        "id": str(promotion.new_level.id),
                        "name": promotion.new_level.name
                    } if promotion.new_level else None,
                    "previous_class": {
                        "id": str(promotion.previous_class.id),
                        "code": promotion.previous_class.code
                    } if promotion.previous_class else None,
                    "new_class": {
                        "id": str(promotion.new_class.id),
                        "code": promotion.new_class.code
                    } if promotion.new_class else None,
                    "status_updated_by": {
                        "id": str(promotion.status_updated_staff.id),
                        "name": f"{promotion.status_updated_staff.first_name} {promotion.status_updated_staff.last_name}"
                    } if promotion.status_updated_staff else None
                }, file_name)


