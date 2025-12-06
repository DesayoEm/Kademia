from typing import Dict, List
from app.core.shared.models.enums import Resource
from app.core.shared.models.enums import Action


matrix: Dict[str, Dict[Resource, List[Action]]] = {
    "SUPER_EDUCATOR": {
        # Identity Management
        Resource.STUDENT: [
            Action.CREATE,
            Action.READ,
            Action.UPDATE,
            Action.DELETE,
            Action.ARCHIVE,
            Action.RESTORE,
            Action.APPROVE,
            Action.REJECT,
        ],
        Resource.STAFF: [
            Action.CREATE,
            Action.READ,
            Action.UPDATE,
            Action.DELETE,
            Action.ARCHIVE,
            Action.RESTORE,
            Action.APPROVE,
            Action.REJECT,
        ],
        Resource.EDUCATOR: [
            Action.CREATE,
            Action.READ,
            Action.UPDATE,
            Action.DELETE,
            Action.ARCHIVE,
            Action.RESTORE,
            Action.APPROVE,
            Action.REJECT,
        ],
        Resource.GUARDIAN: [
            Action.CREATE,
            Action.READ,
            Action.UPDATE,
            Action.DELETE,
            Action.ARCHIVE,
            Action.RESTORE,
            Action.APPROVE,
            Action.REJECT,
        ],
        # Academic Structure
        Resource.CLASSES: [
            Action.CREATE,
            Action.READ,
            Action.UPDATE,
            Action.DELETE,
            Action.ARCHIVE,
            Action.RESTORE,
            Action.APPROVE,
            Action.REJECT,
        ],
        Resource.DEPARTMENT: [
            Action.CREATE,
            Action.READ,
            Action.UPDATE,
            Action.DELETE,
            Action.ARCHIVE,
            Action.RESTORE,
            Action.APPROVE,
            Action.REJECT,
        ],
        Resource.ACADEMIC_LEVEL: [
            Action.CREATE,
            Action.READ,
            Action.UPDATE,
            Action.DELETE,
            Action.ARCHIVE,
            Action.RESTORE,
            Action.APPROVE,
            Action.REJECT,
        ],
        # Curriculum
        Resource.SUBJECT: [
            Action.CREATE,
            Action.READ,
            Action.UPDATE,
            Action.DELETE,
            Action.ARCHIVE,
            Action.RESTORE,
            Action.APPROVE,
            Action.REJECT,
        ],
        Resource.ACADEMIC_LEVEL_SUBJECT: [
            Action.CREATE,
            Action.READ,
            Action.UPDATE,
            Action.DELETE,
            Action.ARCHIVE,
            Action.RESTORE,
            Action.APPROVE,
            Action.REJECT,
        ],
        Resource.STUDENT_SUBJECT: [
            Action.CREATE,
            Action.READ,
            Action.UPDATE,
            Action.DELETE,
            Action.ARCHIVE,
            Action.RESTORE,
            Action.APPROVE,
            Action.REJECT,
        ],
        Resource.SUBJECT_EDUCATOR: [
            Action.CREATE,
            Action.READ,
            Action.UPDATE,
            Action.DELETE,
            Action.ARCHIVE,
            Action.RESTORE,
            Action.APPROVE,
            Action.REJECT,
        ],
        # Assessment
        Resource.GRADE: [
            Action.CREATE,
            Action.READ,
            Action.UPDATE,
            Action.DELETE,
            Action.ARCHIVE,
            Action.RESTORE,
            Action.APPROVE,
            Action.REJECT,
        ],
        Resource.TOTAL_GRADE: [
            Action.CREATE,
            Action.READ,
            Action.UPDATE,
            Action.DELETE,
            Action.ARCHIVE,
            Action.RESTORE,
            Action.APPROVE,
            Action.REJECT,
        ],
        # Documents & Awards
        Resource.DOCUMENT: [
            Action.CREATE,
            Action.READ,
            Action.UPDATE,
            Action.DELETE,
            Action.ARCHIVE,
            Action.RESTORE,
            Action.APPROVE,
            Action.REJECT,
        ],
        Resource.AWARD: [
            Action.CREATE,
            Action.READ,
            Action.UPDATE,
            Action.DELETE,
            Action.ARCHIVE,
            Action.RESTORE,
            Action.APPROVE,
            Action.REJECT,
        ],
        # Progression
        Resource.TRANSFER: [
            Action.CREATE,
            Action.READ,
            Action.UPDATE,
            Action.DELETE,
            Action.ARCHIVE,
            Action.RESTORE,
            Action.APPROVE,
            Action.REJECT,
        ],
        Resource.PROMOTION: [
            Action.CREATE,
            Action.READ,
            Action.UPDATE,
            Action.DELETE,
            Action.ARCHIVE,
            Action.RESTORE,
            Action.APPROVE,
            Action.REJECT,
        ],
        Resource.REPETITION: [
            Action.CREATE,
            Action.READ,
            Action.UPDATE,
            Action.DELETE,
            Action.ARCHIVE,
            Action.RESTORE,
            Action.APPROVE,
            Action.REJECT,
        ],
    },
    "EDUCATOR": {
        # Identity Management - Contextual access
        Resource.STUDENT: [Action.READ, Action.UPDATE],  # Only their students
        Resource.STAFF: [Action.READ],
        Resource.EDUCATOR: [Action.READ],
        Resource.GUARDIAN: [Action.READ],  # Only for their students' guardians
        # Staff Management
        Resource.EDUCATOR_QUALIFICATION: [
            Action.CREATE,
            Action.READ,
            Action.UPDATE,
            Action.DELETE,
        ],  # Own qualifications only
        # Academic Structure
        Resource.CLASSE: [Action.READ],
        Resource.DEPARTMENT: [Action.READ],
        Resource.ACADEMIC_LEVEL: [Action.READ],
        # Curriculum
        Resource.SUBJECT: [Action.READ],
        Resource.ACADEMIC_LEVEL_SUBJECT: [Action.READ],  # Their subjects
        Resource.STUDENT_SUBJECT: [
            Action.CREATE,
            Action.READ,
            Action.UPDATE,
        ],  # For their students
        Resource.SUBJECT_EDUCATOR: [Action.READ],
        # Assessment
        Resource.GRADE: [
            Action.CREATE,
            Action.READ,
            Action.UPDATE,
            Action.DELETE,
        ],  # For their subjects
        Resource.TOTAL_GRADE: [Action.READ],  # For their students
        # Documents & Awards
        Resource.DOCUMENT: [
            Action.READ,
            Action.CREATE,
            Action.UPDATE,
        ],  # For their students
        Resource.AWARD: [
            Action.CREATE,
            Action.READ,
            Action.UPDATE,
        ],  # For their students
        # Progression
        Resource.TRANSFER: [
            Action.CREATE,
            Action.READ,
            Action.UPDATE,
            Action.APPROVE,
            Action.REJECT,
        ],  # For their students/department
        Resource.PROMOTION: [
            Action.CREATE,
            Action.READ,
            Action.UPDATE,
            Action.APPROVE,
            Action.REJECT,
        ],  # For their students
        Resource.REPETITION: [
            Action.CREATE,
            Action.READ,
            Action.UPDATE,
            Action.APPROVE,
            Action.REJECT,
        ],  # For their students
        # System
        Resource.ROLE_CHANGE: [Action.READ],  # Own changes only
    },
    "ADMIN": {
        # Identity Management
        Resource.STUDENT: [
            Action.CREATE,
            Action.READ,
            Action.UPDATE,
            Action.ARCHIVE,
            Action.RESTORE,
        ],
        Resource.STAFF: [
            Action.CREATE,
            Action.READ,
            Action.UPDATE,
            Action.ARCHIVE,
            Action.RESTORE,
        ],
        Resource.EDUCATOR: [
            Action.CREATE,
            Action.READ,
            Action.UPDATE,
            Action.ARCHIVE,
            Action.RESTORE,
        ],
        Resource.GUARDIAN: [
            Action.CREATE,
            Action.READ,
            Action.UPDATE,
            Action.ARCHIVE,
            Action.RESTORE,
        ],
        # Staff Management - Read only
        Resource.STAFF_DEPARTMENT: [Action.READ],
        Resource.STAFF_ROLE: [Action.READ],
        Resource.EDUCATOR_QUALIFICATION: [Action.READ],
        # Academic Structure
        Resource.CLASSE: [Action.CREATE, Action.READ, Action.UPDATE],
        Resource.DEPARTMENT: [Action.READ],
        Resource.ACADEMIC_LEVEL: [Action.READ],
        # Curriculum
        Resource.SUBJECT: [Action.READ],
        Resource.ACADEMIC_LEVEL_SUBJECT: [Action.READ],
        Resource.STUDENT_SUBJECT: [Action.CREATE, Action.READ, Action.UPDATE],
        Resource.SUBJECT_EDUCATOR: [Action.CREATE, Action.READ, Action.UPDATE],
        # Assessment - Read only
        Resource.GRADE: [Action.READ],
        Resource.TOTAL_GRADE: [Action.READ],
        # Documents & Awards
        Resource.DOCUMENT: [
            Action.CREATE,
            Action.READ,
            Action.UPDATE,
            Action.DELETE,
            Action.ARCHIVE,
            Action.RESTORE,
        ],
        Resource.AWARD: [
            Action.CREATE,
            Action.READ,
            Action.UPDATE,
            Action.DELETE,
            Action.ARCHIVE,
            Action.RESTORE,
        ],
        # Progression - Can process but not approve
        Resource.TRANSFER: [Action.CREATE, Action.READ, Action.UPDATE],
        Resource.PROMOTION: [Action.CREATE, Action.READ, Action.UPDATE],
        Resource.REPETITION: [Action.CREATE, Action.READ, Action.UPDATE],
        # System
        Resource.ROLE_CHANGE: [Action.READ],
        Resource.AUDIT: [Action.READ],
    },
}

# Contextual access rules for roles that need row-level filtering
CONTEXTUAL_ACCESS_RULE: Dict[str, Dict[Resource, str]] = {
    "EDUCATOR": {
        Resource.STUDENT: "educator_student_access",
        Resource.GUARDIAN: "educator_guardian_access",
        Resource.GRADE: "educator_grade_access",
        Resource.DOCUMENT: "educator_document_access",
        Resource.AWARD: "educator_award_access",
        Resource.TRANSFER: "educator_transfer_access",
        Resource.PROMOTION: "educator_promotion_access",
        Resource.REPETITION: "educator_repetition_access",
        Resource.STUDENT_SUBJECT: "educator_student_subject_access",
    },
    "STUDENT": {
        Resource.STUDENT: "own_record_only",
        Resource.GUARDIAN: "own_guardian_only",
        Resource.GRADE: "own_grades_only",
        Resource.DOCUMENT: "own_documents_only",
        Resource.AWARD: "own_awards_only",
        Resource.TRANSFER: "own_transfers_only",
        Resource.PROMOTION: "own_promotions_only",
        Resource.REPETITION: "own_repetitions_only",
        Resource.STUDENT_SUBJECT: "own_subjects_only",
        Resource.CLASSE: "own_class_only",
        Resource.DEPARTMENT: "own_department_only",
        Resource.ACADEMIC_LEVEL: "own_level_only",
    },
    "GUARDIAN": {
        Resource.STUDENT: "ward_records_only",
        Resource.GUARDIAN: "own_record_only",
        Resource.GRADE: "ward_grades_only",
        Resource.DOCUMENT: "ward_documents_only",
        Resource.AWARD: "ward_awards_only",
        Resource.TRANSFER: "ward_transfers_only",
        Resource.PROMOTION: "ward_promotions_only",
        Resource.REPETITION: "ward_repetitions_only",
        Resource.STUDENT_SUBJECT: "ward_subjects_only",
        Resource.CLASSE: "ward_class_only",
        Resource.DEPARTMENT: "ward_department_only",
        Resource.ACADEMIC_LEVEL: "ward_level_only",
    },
}
