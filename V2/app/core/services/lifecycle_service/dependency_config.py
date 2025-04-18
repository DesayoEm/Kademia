from ....database.models import *
#[(relationship_name, model_class, fk, display name), ...]


DEPENDENCY_CONFIG = {
    StaffRole: [("staff_members", Staff, "role_id", "staff members")],
    StaffDepartment: [("staff_members", Staff, "department_id", "staff members")],
    EducatorQualification: [],

    StudentDepartment: [("students", Student, "department_id", "students")],

    AcademicLevel: [("subjects", AcademicLevelSubject, "level_id", "subjects"),
                    ("classes", Classes, "level_id", "subjects"),
                    ("students", Student, "level_id", "students")],

    Classes: ["students", Student, "class_id", "students"],


    # Educator: [("qualifications", "qualifications"), ("subject_assignments", "assigned subjects"),
    #            ("mentored_department", "mentored departments"), ("supervised_class", "supervised classes")
    #            ],
    #
    # Student: [("documents_owned", "documents"), ("awards_earned", "awards"), ("subjects_taken", "subjects"),
    #            ("grades", "grades"), ("total_grades", "total grades"), ("classes_repeated", "repeated classes"),
    #             ("department_transfers", "department transfers"), ("class_transfers", "class transfers"),
    #         ],

    #
    #
    # Subject: [("students", "students"), ("educators", "educators"), ("grades", "grades"),
    #           ("total_grades", "total grades"), ("academic_levels", "academic levels")],
    #
    # StudentDocument: [],
    # StudentAward: [],
    # StudentSubject: [],
    # Grade: [],
    # TotalGrade: [],
    # StudentDepartmentTransfer: [],
    # ClassTransfer: [],
    # Repetition: [],
    # AccessLevelChange: [],
}
