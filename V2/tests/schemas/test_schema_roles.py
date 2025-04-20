from V2.app.core.staff_management.schemas.role import StaffRoleCreate

def test_unit_schema_staff_role_validation():
    valid_data = {"name":"HOD",
                  "description": "Manages departmental operations"}
    role = StaffRoleCreate(**valid_data)
    assert role.name == "HOD"
    assert role.description == "Manages departmental operations"
