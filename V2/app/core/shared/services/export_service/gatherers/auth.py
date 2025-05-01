from typing import Dict, Tuple, Any
from V2.app.core.auth.models.auth import AccessLevelChange

class AuthGatherer:
    """Gathers data for auth entities"""

    @staticmethod
    def gather_access_level_change_data(change: AccessLevelChange) -> Tuple[Dict[str, Any], str]:
        """Gather data for AccessLevelChange entity."""
        file_name = f"AccessLevelChange_{change.staff_id}_{change.changed_at.date()}"

        return ({
                    "access_level_change": {
                        "id": str(change.id),
                        "staff_id": str(change.staff_id),
                        "previous_level": change.previous_level,
                        "new_level": change.new_level,
                        "reason": change.reason,
                        "changed_at": change.changed_at,
                        "changed_by_id": str(change.changed_by_id),
                    },
                    "staff": {
                        "id": str(change.user.id),
                        "name": f"{change.user.first_name} {change.user.last_name}",
                        "role": str(change.user.role.name) if change.user.role else None,
                    } if change.user else None
                }, file_name)
