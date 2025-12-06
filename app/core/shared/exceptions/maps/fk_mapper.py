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

# model names are represented as strings to avoid circular imports

fk_error_map = {
    "common": {
        "staff_created_by": ("Staff", "created_by", "Creator"),
        "staff_last_modified_by": ("Staff", "last_modified_by", "Last Modifier"),
        "staff_archived_by": ("Staff", "archived_by", "Archiver"),
    },
    "StudentFactory": {
        "fk_students_guardians_guardian_id": ("Guardian", "guardian_id", "Guardian"),
        "fk_students_academic_levels_level_id": (
            "AcademicLevel",
            "level_id",
            "Academic Level",
        ),
        "fk_students_classes_class_id": ("Classes", "class_id", "Class"),
        "fk_students_student_departments_department_id": (
            "StudentDepartment",
            "department_id",
            "Department",
        ),
    },
    "GuardianFactory": {},
    "StaffFactory": {
        "fk_staff_staff_departments_department_id": (
            "StaffDepartment",
            "department_id",
            "Staff Department",
        ),
        "fk_staff_staff_roles_role_id": ("StaffRole", "role_id", "Staff Role"),
    },
    "AcademicLevelFactory": {},
    "ClassFactory": {
        "fk_classes_academic_levels_level_id": (
            "AcademicLevel",
            "level_id",
            "Academic Level",
        ),
        "fk_classes_educators_supervisor_id": (
            "Educator",
            "supervisor_id",
            "Supervisor",
        ),
        "fk_classes_students_student_rep": (
            "Student",
            "student_rep_id",
            "Student Representative",
        ),
        "fk_classes_students_assistant_rep": (
            "Student",
            "assistant_rep_id",
            "Assistant Representative",
        ),
    },
    "StudentDepartmentFactory": {
        "fk_student_departments_educators_mentor_id": (
            "Educator",
            "mentor_id",
            "Mentor",
        ),
        "fk_student_departments_students_student_rep": (
            "Student",
            "student_rep_id",
            "Student Representative",
        ),
        "fk_student_departments_students_assistant_rep": (
            "Student",
            "assistant_rep_id",
            "Assistant Representative",
        ),
    },
    "StaffDepartmentFactory": {
        "fk_staff_departments_staff_manager_id": ("Staff", "manager_id", "Manager"),
    },
    "QualificationFactory": {
        "fk_educator_qualifications_educators_educator_id": (
            "Educator",
            "educator_id",
            "Educator",
        ),
    },
    "StaffTitleFactory": {},
    "SubjectFactory": {
        "fk_subjects_student_departments_department_id": (
            "StudentDepartment",
            "department_id",
            "department",
        ),
    },
    "AcademicLevelSubjectFactory": {
        "fk_academic_level_subjects_academic_levels_level_id": (
            "AcademicLevel",
            "level_id",
            "Academic Level",
        ),
        "fk_academic_level_subjects_subjects_subject_id": (
            "Subject",
            "subject_id",
            "Subject",
        ),
        "fk_academic_level_subjects_educators_educator_id": (
            "Educator",
            "educator_id",
            "Educator",
        ),
    },
    "StudentSubjectFactory": {
        "fk_student_subjects_students_student_id": ("Student", "student_id", "Student"),
        "fk_student_subjects_subjects_subject_id": ("Subject", "subject_id", "Subject"),
    },
    "SubjectEducatorFactory": {
        "fk_subject_educators_subjects_subject_id": (
            "Subject",
            "subject_id",
            "Subject",
        ),
        "fk_subject_educators_educators_educator_id": (
            "Educator",
            "educator_id",
            "Educator",
        ),
        "fk_subject_educators_academic_levels_level_id": (
            "AcademicLevel",
            "level_id",
            "Academic Level",
        ),
    },
    "GradeFactory": {
        "fk_grades_students_student_id": ("Student", "student_id", "Student"),
        "fk_grades_subjects_subject_id": ("Subject", "subject_id", "Subject"),
        "fk_grades_staff_graded_by": ("Staff", "graded_by", "Grader"),
    },
    "TotalGradeFactory": {
        "fk_total_grades_students_student_id": ("Student", "student_id", "Student"),
        "fk_total_grades_subjects_subject_id": ("Subject", "subject_id", "Subject"),
    },
    "RepetitionFactory": {
        "fk_student_repetitions_students_student_id": (
            "Student",
            "student_id",
            "Student",
        ),
        "fk_student_repetitions_academic_levels_previous_level": (
            "AcademicLevel",
            "previous_level_id",
            "Previous Level",
        ),
        "fk_student_repetitions_academic_levels_new_level": (
            "AcademicLevel",
            "new_level_id",
            "New Level",
        ),
        "fk_student_repetitions_classes_previous_class": (
            "Classes",
            "previous_class_id",
            "Previous Class",
        ),
        "fk_student_repetitions_classes_new_class": (
            "Classes",
            "new_class_id",
            "New Class",
        ),
        "fk_student_repetitions_staff_status_updated_by": (
            "Staff",
            "status_updated_by",
            "Status Updated By",
        ),
    },
    "ClassTransferFactory": {
        "fk_student_department_transfers_students_student_id": (
            "Student",
            "student_id",
            "Student",
        ),
        "fk_student_department_transfers_classes_previous_class": (
            "Classes",
            "previous_class_id",
            "Previous Class",
        ),
        "fk_student_department_transfers_classes_new_class": (
            "Classes",
            "new_class_id",
            "New Class",
        ),
        "fk_student_department_transfers_staff_status_updated_by": (
            "Staff",
            "status_updated_by",
            "Status Updated By",
        ),
    },
    "StudentDepartmentTransferFactory": {
        "fk_student_department_transfers_students_student_id": (
            "Student",
            "student_id",
            "Student",
        ),
        "fk_student_department_transfers_academic_levels_previous_level": (
            "AcademicLevel",
            "previous_level_id",
            "Previous Level",
        ),
        "fk_student_department_transfers_academic_levels_new_level": (
            "AcademicLevel",
            "new_level_id",
            "New Level",
        ),
        "fk_student_department_transfers_classes_previous_class": (
            "Classes",
            "previous_class_id",
            "Previous Class",
        ),
        "fk_student_department_transfers_classes_new_class": (
            "Classes",
            "new_class_id",
            "New Class",
        ),
        "fk_student_transfers_previous_department": (
            "StudentDepartment",
            "previous_department_id",
            "Previous Department",
        ),
        "fk_student_transfers_new_department": (
            "StudentDepartment",
            "new_department_id",
            "New Department",
        ),
        "fk_student_department_transfers_staff_status_updated_by": (
            "Staff",
            "status_updated_by",
            "Status Updated By",
        ),
    },
    "StudentDocumentFactory": {
        "fk_student_documents_students_student_id": (
            "Student",
            "student_id",
            "Student",
        ),
    },
    "StudentAwardFactory": {
        "fk_student_documents_students_student_id": (
            "Student",
            "student_id",
            "Student",
        ),
    },
    "RoleHistoryFactory": {
        "fk_role_history_staff_staff_id": ("Staff", "staff_id", "Target Staff"),
        "fk_role_history_staff_changed_by": ("Staff", "changed_by_id", "Changed By"),
    },
}
