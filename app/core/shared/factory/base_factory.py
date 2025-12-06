from uuid import UUID

SYSTEM_USER_ID = UUID("00000000-0000-0000-0000-000000000000")


class BaseFactory:
    def __init__(self, current_user):
        self.current_user = current_user

    def get_actor_id(self):
        """Get the ID of the actor (current user or system)"""
        return self.current_user.id

    # if self.current_user else SYSTEM_USER_ID
