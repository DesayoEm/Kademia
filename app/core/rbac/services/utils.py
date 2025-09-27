
from sqlalchemy.orm import Session
from app.core.shared.exceptions import NegativeRankError, EntityNotFoundError



class RBACUtils:
    def __init__(self):
        pass


    @staticmethod
    def validate_rank_number(value: int)-> int:
        if value < 0:
            raise NegativeRankError(value=value)
        return value

    @staticmethod
    def generate_permission_str(resource_name: str, action_name: str) -> str:
        permission_name = f"{(resource_name +"_" + action_name).upper}"
        return permission_name

