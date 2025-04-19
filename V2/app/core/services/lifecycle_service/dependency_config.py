from ....database.models import *
#[(relationship_name, model_class, fk, display name), ...]


DEPENDENCY_CONFIG = {
    # User
    Guardian: [
        ("wards", Student, "guardian_id", "wards")
    ],
    Student: [
        ("documents_owned", StudentDocument, "owner_id", "documents"),
        ("awards_earned", StudentAward, "owner_id", "awards"),
        ("subjects_taken", StudentSubject, "student_id", "subject enrollments"),
        ("grades", Grade, "student_id", "grades"),
        ("total_grades", TotalGrade, "student_id", "total grades"),
        ("classes_repeated", Repetition, "student_id", "class repetitions"),
        ("department_transfers", StudentDepartmentTransfer, "student_id", "department transfers"),
        ("class_transfers", ClassTransfer, "student_id", "class transfers")
    ],
    Staff: [
        ("access_changes", AccessLevelChange, "staff_id", "access level changes")
    ],

    Educator: [
        ("qualifications", EducatorQualification, "educator_id", "qualifications"),
        ("subject_assignments", SubjectEducator, "educator_id", "subject assignments"),
        ("mentored_department", StudentDepartment, "mentor_id", "mentored departments"),
        ("supervised_class", Classes, "supervisor_id", "supervised classes")
    ],

    # Student Organization
    StudentDepartment: [
        ("students", Student, "department_id", "students"),
        ("subjects", Subject, "department_id", "subjects")
    ],

    AcademicLevel: [
        ("subjects", AcademicLevelSubject, "level_id", "subject assignments"),
        ("classes", Classes, "level_id", "classes"),
        ("students", Student, "level_id", "students")
    ],

    Classes: [
        ("students", Student, "class_id", "students")
    ],

    # Staff Organization
    StaffRole: [
        ("staff_members", Staff, "role_id", "staff members")
    ],

    StaffDepartment: [
        ("staff_members", Staff, "department_id", "staff members")
    ],

    EducatorQualification: [],

#     #Academic
#     Subject: [
#         ("students", StudentSubject, "subject_id", "enrolled students"),
#         ("educators", SubjectEducator, "subject_id", "assigned educators"),
#         ("academic_levels", AcademicLevelSubject, "subject_id", "academic level assignments"),
#         ("grades", Grade, "subject_id", "grades"),
#         ("total_grades", TotalGrade, "subject_id", "total grades")
#     ],
#     AcademicLevelSubject: [],
#     StudentSubject: [],
#     SubjectEducator: [],
#     Grade: [],
#     TotalGrade: [],
#     Repetition: [],
#     StudentAward: [],
#     StudentDocument: [],
#     AccessLevelChange: []
}