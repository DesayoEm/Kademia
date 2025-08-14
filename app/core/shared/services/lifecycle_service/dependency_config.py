from ....curriculum.models.curriculum import SubjectEducator, StudentSubject, Subject, AcademicLevelSubject
from ....documents.models.documents import StudentDocument, StudentAward
from ....rbac.models import RoleHistory
from app.core.staff_management.models import StaffDepartment, StaffTitle, EducatorQualification
from app.core.academic_structure.models import StudentDepartment, Classes, AcademicLevel
from ....transfer.models.transfer import DepartmentTransfer
from ....assessment.models.assessment import Grade, TotalGrade
from app.core.progression.models.progression import Repetition, Promotion
from ....identity.models.staff import Staff, Educator
from ....identity.models.student import Student
from ....identity.models.guardian import Guardian


#[(relationship_name, model_class, fk, display name), ...]

DEPENDENCY_CONFIG = {

    # Student Organization
    StudentDepartment: [
        ("students", Student, "department_id", "students"),
        ("subjects", Subject, "department_id", "subjects"),
        ("new_department", DepartmentTransfer, "new_department_id", "transfers"),
    ],

    AcademicLevel: [
        ("subjects", AcademicLevelSubject, "level_id", "academic level subjects"),
        ("classes", Classes, "level_id", "classes"),
        ("students", Student, "level_id", "students")
    ],

    Classes: [
        ("students", Student, "class_id", "students")
    ],

    # Staff Organization
    StaffTitle: [
        ("staff_members", Staff, "title_id", "staff members")
    ],

    StaffDepartment: [
        ("staff_members", Staff, "department_id", "staff members")
    ],

    #Users

    Guardian: [
            ("wards", Student, "guardian_id", "wards")
        ],

    Student: [
            ("documents_owned", StudentDocument, "student_id", "documents"),
            ("awards_earned", StudentAward, "student_id", "awards"),
            ("subjects_taken", StudentSubject, "student_id", "subject enrollments"),
            ("grades", Grade, "student_id", "grades"),
            ("total_grades", TotalGrade, "student_id", "total grades"),
            ("classes_repeated", Repetition, "student_id", "class repetitions"),
            ("promotions", Promotion, "student_id", "promotions"),
            ("department_transfers", DepartmentTransfer, "student_id", "department transfers"),

    ],

    Staff: [
        ("role_changes", RoleHistory, "staff_id", "permission changes")
    ],

    Educator: [
        ("qualifications", EducatorQualification, "educator_id", "qualifications"),
        ("subject_assignments", SubjectEducator, "educator_id", "subject assignments"),
        ("role_changes", RoleHistory, "staff_id", "permission changes"),

    ],

    #Curriculum
    Subject: [
        ("academic_levels", AcademicLevelSubject, "subject_id", "academic level assignments"),
    ],

    AcademicLevelSubject: [
            ("students", StudentSubject, "academic_level_subject_id", "enrolled students"),
            ("educators", SubjectEducator, "academic_level_subject_id", "assigned educators"),
        ],

    StudentSubject: [
                ("grades", Grade, "student_subject_id", "grades"),
                ("total_grades", TotalGrade, "student_subject_id", "total grades")
            ],

    Promotion: [],
    Repetition: [],
    EducatorQualification: [],
    SubjectEducator: [],
    Grade: [],
    TotalGrade: [],
    StudentAward: [],
    StudentDocument: [],
    RoleHistory: []
}