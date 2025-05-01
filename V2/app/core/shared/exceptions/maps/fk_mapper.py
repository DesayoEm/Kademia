"""

This file maps each factory class to a dictionary of foreign key constraint names
and their corresponding (model, attribute, identity-facing label) tuples.
Format:
    {
        "FactoryClassName": {
            "fk_constraint_name": ("RelatedModelName", attr_name_on_obj, user_friendly_label)
        }
    }
Usage:
    - Inline for simple factories with 1-2 constraints
    - With helper (`resolve_fk_violation(...)`) for factories with 3+ FK constraints
"""

# NO factory class imports here to avoid circular dependencies
# Model names are used as strings to keep the mapping clean and safe

fk_error_map = {
    "common": {
        "staff_created_by": ("Staff", "created_by", "Creator"),
        "staff_last_modified_by": ("Staff", "last_modified_by", "Last Modifier"),
        "staff_archived_by": ("Staff", "archived_by", "Archiver"),
    },

    "StudentFactory": {
        "fk_students_guardians_guardian_id": ("Guardian", "guardian_id", "Guardian"),
        "fk_students_academic_levels_level_id": ("AcademicLevel", "level_id", "Academic Level"),
        "fk_students_classes_class_id": ("Classes", "class_id", "Class"),
        "fk_students_student_departments_department_id": ("StudentDepartment", "department_id", "Department"),
    },

    "GuardianFactory": {},

    "StaffFactory": {
        "fk_staff_staff_departments_department_id": ("StaffDepartment", "department_id", "Staff Department"),
        "fk_staff_staff_roles_role_id": ("StaffRole", "role_id", "Staff Role"),
    },

    "AcademicLevelFactory": {},

    "ClassFactory": {
        "fk_classes_academic_levels_level_id": ("AcademicLevel", "level_id", "Academic Level"),
        "fk_classes_educators_supervisor_id": ("Educator", "supervisor_id", "Supervisor"),
        "fk_classes_students_student_rep": ("Student", "student_rep_id", "Student Representative"),
        "fk_classes_students_assistant_rep": ("Student", "assistant_rep_id", "Assistant Representative"),
    },

    "StudentDepartmentFactory": {
        "fk_student_departments_educators_mentor_id": ("Educator", "mentor_id", "Mentor"),
        "fk_student_departments_students_student_rep": ("Student", "student_rep_id", "Student Representative"),
        "fk_student_departments_students_assistant_rep": ("Student", "assistant_rep_id", "Assistant Representative"),
    },

    "StaffDepartmentFactory": {
        "fk_staff_departments_staff_manager_id": ("Staff", "manager_id", "Manager"),
    },

    "QualificationFactory": {
        "fk_educator_qualifications_educators_educator_id": ("Educator", "educator_id", "Educator"),
    },

    "StaffRoleFactory": {}
}
