from ....database.models import *
#[(relationship_name, model_class, fk, display name), ...]


DEPENDENCY_CONFIG = {
    StaffRole: [("staff_members", Staff, "role_id", "staff members")],
    StaffDepartment: [("staff_members", Staff, "department_id", "staff members")],


    # Educator: [("qualifications", "qualifications"), ("subject_assignments", "assigned subjects"),
    #            ("mentored_department", "mentored departments"), ("supervised_class", "supervised classes")
    #            ],
    #
    # Student: [("documents_owned", "documents"), ("awards_earned", "awards"), ("subjects_taken", "subjects"),
    #            ("grades", "grades"), ("total_grades", "total grades"), ("classes_repeated", "repeated classes"),
    #             ("department_transfers", "department transfers"), ("class_transfers", "class transfers"),
    #         ],
    #
    # StudentDepartment: [("students", "students")],
    #
    # AcademicLevel: [("classes", "classes"), ("subjects", "subjects"), ("students", "students")],
    #
    # Classes: [("students", "students")],
    #
    # Subject: [("students", "students"), ("educators", "educators"), ("grades", "grades"),
    #           ("total_grades", "total grades"), ("academic_levels", "academic levels")],
    #
    # StudentDocument: [],
     EducatorQualification: [],
    # StudentAward: [],
    # StudentSubject: [],
    # Grade: [],
    # TotalGrade: [],
    # StudentDepartmentTransfer: [],
    # ClassTransfer: [],
    # Repetition: [],
    # AccessLevelChange: [],
}
