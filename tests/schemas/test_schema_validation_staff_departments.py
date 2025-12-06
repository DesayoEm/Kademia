from app.core.staff_management.schemas.department import StaffDepartmentCreate


def test_unit_schema_qualification_validation():
    valid_data = {"name": "Education", "description": "Manages academic programs"}
    department = StaffDepartmentCreate(**valid_data)
    assert department.name == "Education"
    assert department.description == "Manages academic programs"
    assert department.manager_id == None
