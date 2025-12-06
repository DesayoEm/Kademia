from uuid import UUID
from app.core.staff_management.schemas.qualification import QualificationCreate

SYSTEM_USER_ID = UUID("00000000-0000-0000-0000-000000000000")


def test_unit_schema_qualification_validation():
    valid_data = {"educator_id": SYSTEM_USER_ID, "name": "B.Sc"}
    qualification = QualificationCreate(**valid_data)
    assert qualification.educator_id == SYSTEM_USER_ID
    assert qualification.name == "B.Sc"
    assert qualification.description == None
