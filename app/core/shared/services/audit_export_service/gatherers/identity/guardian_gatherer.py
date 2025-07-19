from typing import Dict, Tuple, Any
from app.core.identity.models.guardian import Guardian

class GuardianGatherer:
    """Gatherer for student-related entities"""

    @staticmethod
    def gather_guardian_data(guardian: Guardian) -> Tuple[Dict[str, Any], str]:
        """Gather data for Guardian entity."""
        file_name = f"Guardian_{guardian.first_name}_{guardian.last_name}"
        wards = guardian.wards

        return ({
                    "guardian": {
                        "id": str(guardian.id),
                        "title": guardian.title,
                        "full_name": f"{guardian.first_name} {guardian.last_name}",
                        "gender": guardian.gender,
                        "email_address": guardian.email_address,
                        "phone": guardian.phone,
                        "address": guardian.address,
                        "image_url": guardian.image_url,
                        "access_level": guardian.access_level,
                        "user_type": guardian.user_type,
                        "last_login": str(guardian.last_login) if guardian.last_login else None,
                        "created_at": guardian.created_at,
                        "last_modified_at": guardian.last_modified_at,
                        "created_by": guardian.created_by_staff,
                        "last_modified_by": guardian.last_modified_by_staff,
                    },
                    "wards": [
                        {
                            "id": str(ward.id),
                            "student_id": ward.student_id,
                            "full_name": f"{ward.first_name} {ward.last_name}",
                            "gender": ward.gender,
                            "date_of_birth": str(ward.date_of_birth),
                            "level": ward.level.name if ward.level else None,
                            "class": f"{ward.class_.academic_level.name} {ward.class_.code}" if ward.class_ and ward.class_.academic_level else None,
                            "department": ward.department.name if ward.department else None,
                            "status": ward.status,
                            "is_repeating": ward.is_repeating,
                            "session_start_year": ward.session_start_year
                        }
                        for ward in wards
                    ],
                    "total_wards": len(wards)
                }, file_name)