from typing import Dict, List, Set

from app.core.shared.models.enums import Resource
from app.core.shared.models.enums import Action


PERMISSION_MATRIX: Dict[str, Dict[Resource, List[Action]]] = {
    "SUPERUSER": {
        # Identity Management
        Resource.STUDENTS: [Action.CREATE, Action.READ, Action.UPDATE, Action.DELETE, Action.ARCHIVE, Action.RESTORE,
                            Action.APPROVE, Action.REJECT],
        Resource.STAFF: [Action.CREATE, Action.READ, Action.UPDATE, Action.DELETE, Action.ARCHIVE, Action.RESTORE,
                         Action.APPROVE, Action.REJECT],
        Resource.EDUCATORS: [Action.CREATE, Action.READ, Action.UPDATE, Action.DELETE, Action.ARCHIVE, Action.RESTORE,
                             Action.APPROVE, Action.REJECT],
        Resource.GUARDIANS: [Action.CREATE, Action.READ, Action.UPDATE, Action.DELETE, Action.ARCHIVE, Action.RESTORE,
                             Action.APPROVE, Action.REJECT],

        # Staff Management
        Resource.STAFF_DEPARTMENTS: [Action.CREATE, Action.READ, Action.UPDATE, Action.DELETE, Action.ARCHIVE,
                                     Action.RESTORE, Action.APPROVE, Action.REJECT],
        Resource.STAFF_ROLES: [Action.CREATE, Action.READ, Action.UPDATE, Action.DELETE, Action.ARCHIVE, Action.RESTORE,
                               Action.APPROVE, Action.REJECT],
        Resource.EDUCATOR_QUALIFICATIONS: [Action.CREATE, Action.READ, Action.UPDATE, Action.DELETE, Action.ARCHIVE,
                                           Action.RESTORE, Action.APPROVE, Action.REJECT],

        # Academic Structure
        Resource.CLASSES: [Action.CREATE, Action.READ, Action.UPDATE, Action.DELETE, Action.ARCHIVE, Action.RESTORE,
                           Action.APPROVE, Action.REJECT],
        Resource.DEPARTMENTS: [Action.CREATE, Action.READ, Action.UPDATE, Action.DELETE, Action.ARCHIVE, Action.RESTORE,
                               Action.APPROVE, Action.REJECT],
        Resource.ACADEMIC_LEVELS: [Action.CREATE, Action.READ, Action.UPDATE, Action.DELETE, Action.ARCHIVE,
                                   Action.RESTORE, Action.APPROVE, Action.REJECT],

        # Curriculum
        Resource.SUBJECTS: [Action.CREATE, Action.READ, Action.UPDATE, Action.DELETE, Action.ARCHIVE, Action.RESTORE,
                            Action.APPROVE, Action.REJECT],
        Resource.ACADEMIC_LEVEL_SUBJECTS: [Action.CREATE, Action.READ, Action.UPDATE, Action.DELETE, Action.ARCHIVE,
                                           Action.RESTORE, Action.APPROVE, Action.REJECT],
        Resource.STUDENT_SUBJECTS: [Action.CREATE, Action.READ, Action.UPDATE, Action.DELETE, Action.ARCHIVE,
                                    Action.RESTORE, Action.APPROVE, Action.REJECT],
        Resource.SUBJECT_EDUCATORS: [Action.CREATE, Action.READ, Action.UPDATE, Action.DELETE, Action.ARCHIVE,
                                     Action.RESTORE, Action.APPROVE, Action.REJECT],

        # Assessment
        Resource.GRADES: [Action.CREATE, Action.READ, Action.UPDATE, Action.DELETE, Action.ARCHIVE, Action.RESTORE,
                          Action.APPROVE, Action.REJECT],
        Resource.TOTAL_GRADES: [Action.CREATE, Action.READ, Action.UPDATE, Action.DELETE, Action.ARCHIVE, Action.RESTORE,
                                Action.APPROVE, Action.REJECT],

        # Documents & Awards
        Resource.DOCUMENTS: [Action.CREATE, Action.READ, Action.UPDATE, Action.DELETE, Action.ARCHIVE, Action.RESTORE,
                             Action.APPROVE, Action.REJECT],
        Resource.AWARDS: [Action.CREATE, Action.READ, Action.UPDATE, Action.DELETE, Action.ARCHIVE, Action.RESTORE,
                          Action.APPROVE, Action.REJECT],

        # Progression
        Resource.TRANSFERS: [Action.CREATE, Action.READ, Action.UPDATE, Action.DELETE, Action.ARCHIVE, Action.RESTORE,
                             Action.APPROVE, Action.REJECT],
        Resource.PROMOTIONS: [Action.CREATE, Action.READ, Action.UPDATE, Action.DELETE, Action.ARCHIVE, Action.RESTORE,
                              Action.APPROVE, Action.REJECT],
        Resource.REPETITIONS: [Action.CREATE, Action.READ, Action.UPDATE, Action.DELETE, Action.ARCHIVE, Action.RESTORE,
                               Action.APPROVE, Action.REJECT],

        # System
        Resource.ACCESS_LEVEL_CHANGE: [Action.CREATE, Action.READ, Action.UPDATE, Action.DELETE, Action.ARCHIVE, Action.RESTORE,
                                       Action.APPROVE, Action.REJECT],
        Resource.AUDITS: [Action.READ],
        Resource.SYSTEM_CONFIG: [Action.CREATE, Action.READ, Action.UPDATE, Action.DELETE, Action.ARCHIVE, Action.RESTORE,
                                 Action.APPROVE, Action.REJECT],
    },

    "SUPER_EDUCATOR": {
        # Identity Management
        Resource.STUDENTS: [Action.CREATE, Action.READ, Action.UPDATE, Action.DELETE, Action.ARCHIVE, Action.RESTORE,
                            Action.APPROVE, Action.REJECT],
        Resource.STAFF: [Action.CREATE, Action.READ, Action.UPDATE, Action.DELETE, Action.ARCHIVE, Action.RESTORE,
                         Action.APPROVE, Action.REJECT],
        Resource.EDUCATORS: [Action.CREATE, Action.READ, Action.UPDATE, Action.DELETE, Action.ARCHIVE, Action.RESTORE,
                             Action.APPROVE, Action.REJECT],
        Resource.GUARDIANS: [Action.CREATE, Action.READ, Action.UPDATE, Action.DELETE, Action.ARCHIVE, Action.RESTORE,
                             Action.APPROVE, Action.REJECT],

        # Staff Management
        Resource.STAFF_DEPARTMENTS: [Action.CREATE, Action.READ, Action.UPDATE, Action.DELETE, Action.ARCHIVE,
                                     Action.RESTORE, Action.APPROVE, Action.REJECT],
        Resource.STAFF_ROLES: [Action.CREATE, Action.READ, Action.UPDATE, Action.DELETE, Action.ARCHIVE, Action.RESTORE,
                               Action.APPROVE, Action.REJECT],
        Resource.EDUCATOR_QUALIFICATIONS: [Action.CREATE, Action.READ, Action.UPDATE, Action.DELETE, Action.ARCHIVE,
                                           Action.RESTORE, Action.APPROVE, Action.REJECT],

        # Academic Structure
        Resource.CLASSES: [Action.CREATE, Action.READ, Action.UPDATE, Action.DELETE, Action.ARCHIVE, Action.RESTORE,
                           Action.APPROVE, Action.REJECT],
        Resource.DEPARTMENTS: [Action.CREATE, Action.READ, Action.UPDATE, Action.DELETE, Action.ARCHIVE, Action.RESTORE,
                               Action.APPROVE, Action.REJECT],
        Resource.ACADEMIC_LEVELS: [Action.CREATE, Action.READ, Action.UPDATE, Action.DELETE, Action.ARCHIVE,
                                   Action.RESTORE, Action.APPROVE, Action.REJECT],

        # Curriculum
        Resource.SUBJECTS: [Action.CREATE, Action.READ, Action.UPDATE, Action.DELETE, Action.ARCHIVE, Action.RESTORE,
                            Action.APPROVE, Action.REJECT],
        Resource.ACADEMIC_LEVEL_SUBJECTS: [Action.CREATE, Action.READ, Action.UPDATE, Action.DELETE, Action.ARCHIVE,
                                           Action.RESTORE, Action.APPROVE, Action.REJECT],
        Resource.STUDENT_SUBJECTS: [Action.CREATE, Action.READ, Action.UPDATE, Action.DELETE, Action.ARCHIVE,
                                    Action.RESTORE, Action.APPROVE, Action.REJECT],
        Resource.SUBJECT_EDUCATORS: [Action.CREATE, Action.READ, Action.UPDATE, Action.DELETE, Action.ARCHIVE,
                                     Action.RESTORE, Action.APPROVE, Action.REJECT],

        # Assessment
        Resource.GRADES: [Action.CREATE, Action.READ, Action.UPDATE, Action.DELETE, Action.ARCHIVE, Action.RESTORE,
                          Action.APPROVE, Action.REJECT],
        Resource.TOTAL_GRADES: [Action.CREATE, Action.READ, Action.UPDATE, Action.DELETE, Action.ARCHIVE,
                                Action.RESTORE,
                                Action.APPROVE, Action.REJECT],

        # Documents & Awards
        Resource.DOCUMENTS: [Action.CREATE, Action.READ, Action.UPDATE, Action.DELETE, Action.ARCHIVE, Action.RESTORE,
                             Action.APPROVE, Action.REJECT],
        Resource.AWARDS: [Action.CREATE, Action.READ, Action.UPDATE, Action.DELETE, Action.ARCHIVE, Action.RESTORE,
                          Action.APPROVE, Action.REJECT],

        # Progression
        Resource.TRANSFERS: [Action.CREATE, Action.READ, Action.UPDATE, Action.DELETE, Action.ARCHIVE, Action.RESTORE,
                             Action.APPROVE, Action.REJECT],
        Resource.PROMOTIONS: [Action.CREATE, Action.READ, Action.UPDATE, Action.DELETE, Action.ARCHIVE, Action.RESTORE,
                              Action.APPROVE, Action.REJECT],
        Resource.REPETITIONS: [Action.CREATE, Action.READ, Action.UPDATE, Action.DELETE, Action.ARCHIVE, Action.RESTORE,
                               Action.APPROVE, Action.REJECT],

    },

    "EDUCATOR": {
        # Identity Management - Contextual access only
        Resource.STUDENTS: [Action.READ, Action.UPDATE],  # Only their students
        Resource.STAFF: [Action.READ],  # Basic read access
        Resource.EDUCATORS: [Action.READ],  # Basic read access
        Resource.GUARDIANS: [Action.READ],  # Only for their students' guardians

        # Staff Management
        Resource.EDUCATOR_QUALIFICATIONS: [Action.CREATE, Action.READ, Action.UPDATE, Action.DELETE],  # Own qualifications only

        # Academic Structure
        Resource.CLASSES: [Action.READ],  # Their assigned classes
        Resource.DEPARTMENTS: [Action.READ, Action.UPDATE],  # Their mentored department
        Resource.ACADEMIC_LEVELS: [Action.READ],

        # Curriculum
        Resource.SUBJECTS: [Action.READ],
        Resource.ACADEMIC_LEVEL_SUBJECTS: [Action.READ],  # Their subjects
        Resource.STUDENT_SUBJECTS: [Action.CREATE, Action.READ, Action.UPDATE],  # For their students
        Resource.SUBJECT_EDUCATORS: [Action.READ],  # Their assignments

        # Assessment
        Resource.GRADES: [Action.CREATE, Action.READ, Action.UPDATE, Action.DELETE],  # For their subjects
        Resource.TOTAL_GRADES: [Action.READ],  # For their students

        # Documents & Awards
        Resource.DOCUMENTS: [Action.READ, Action.APPROVE, Action.REJECT],  # For their students
        Resource.AWARDS: [Action.CREATE, Action.READ, Action.UPDATE, Action.APPROVE, Action.REJECT],  # For their students

        # Progression
        Resource.TRANSFERS: [Action.CREATE, Action.READ, Action.UPDATE, Action.APPROVE,
                             Action.REJECT],  # For their students/department
        Resource.PROMOTIONS: [Action.CREATE, Action.READ, Action.UPDATE, Action.APPROVE, Action.REJECT],  # For their students
        Resource.REPETITIONS: [Action.CREATE, Action.READ, Action.UPDATE, Action.APPROVE, Action.REJECT],  # For their students

        # System
        Resource.ACCESS_LEVEL_CHANGE: [Action.READ],  # Own changes only
        Resource.AUDITS: [Action.READ],  # Limited audit access
    },

    "ADMIN": {
        # Identity Management
        Resource.STUDENTS: [Action.CREATE, Action.READ, Action.UPDATE, Action.ARCHIVE, Action.RESTORE],
        Resource.STAFF: [Action.CREATE, Action.READ, Action.UPDATE, Action.ARCHIVE, Action.RESTORE],
        Resource.EDUCATORS: [Action.CREATE, Action.READ, Action.UPDATE, Action.ARCHIVE, Action.RESTORE],
        Resource.GUARDIANS: [Action.CREATE, Action.READ, Action.UPDATE, Action.ARCHIVE, Action.RESTORE],

        # Staff Management - Read only
        Resource.STAFF_DEPARTMENTS: [Action.READ],
        Resource.STAFF_ROLES: [Action.READ],
        Resource.EDUCATOR_QUALIFICATIONS: [Action.READ],

        # Academic Structure
        Resource.CLASSES: [Action.CREATE, Action.READ, Action.UPDATE],
        Resource.DEPARTMENTS: [Action.READ],
        Resource.ACADEMIC_LEVELS: [Action.READ],

        # Curriculum
        Resource.SUBJECTS: [Action.READ],
        Resource.ACADEMIC_LEVEL_SUBJECTS: [Action.READ],
        Resource.STUDENT_SUBJECTS: [Action.CREATE, Action.READ, Action.UPDATE],
        Resource.SUBJECT_EDUCATORS: [Action.CREATE, Action.READ, Action.UPDATE],

        # Assessment - Read only
        Resource.GRADES: [Action.READ],
        Resource.TOTAL_GRADES: [Action.READ],

        # Documents & Awards
        Resource.DOCUMENTS: [Action.CREATE, Action.READ, Action.UPDATE, Action.DELETE, Action.ARCHIVE, Action.RESTORE],
        Resource.AWARDS: [Action.CREATE, Action.READ, Action.UPDATE, Action.DELETE, Action.ARCHIVE, Action.RESTORE],

        # Progression - Can process but not approve
        Resource.TRANSFERS: [Action.CREATE, Action.READ, Action.UPDATE],
        Resource.PROMOTIONS: [Action.CREATE, Action.READ, Action.UPDATE],
        Resource.REPETITIONS: [Action.CREATE, Action.READ, Action.UPDATE],

        # System
        Resource.ACCESS_LEVEL_CHANGE: [Action.READ],
        Resource.AUDITS: [Action.READ],
    },

    "STUDENT": {
        # Identity Management - Own records only
        Resource.STUDENTS: [Action.READ, Action.UPDATE],  # Own record only
        Resource.STAFF: [Action.READ],  # Basic info of their teachers
        Resource.EDUCATORS: [Action.READ],  # Basic info of their teachers
        Resource.GUARDIANS: [Action.READ],  # Own guardian info

        # Academic Structure - Related to their studies
        Resource.CLASSES: [Action.READ],  # Their class
        Resource.DEPARTMENTS: [Action.READ],  # Their department
        Resource.ACADEMIC_LEVELS: [Action.READ],  # Their level

        # Curriculum - Their subjects
        Resource.SUBJECTS: [Action.READ],  # Their subjects
        Resource.ACADEMIC_LEVEL_SUBJECTS: [Action.READ],  # Their curriculum
        Resource.STUDENT_SUBJECTS: [Action.READ],  # Their enrollments
        Resource.SUBJECT_EDUCATORS: [Action.READ],  # Their teachers

        # Assessment - Own grades
        Resource.GRADES: [Action.READ],  # Own grades
        Resource.TOTAL_GRADES: [Action.READ],  # Own total grades

        # Documents & Awards - Own records
        Resource.DOCUMENTS: [Action.READ],  # Own documents
        Resource.AWARDS: [Action.READ],  # Own awards

        # Progression - Can request transfers
        Resource.TRANSFERS: [Action.CREATE, Action.READ],  # Can request own transfer
        Resource.PROMOTIONS: [Action.READ],  # View own promotions
        Resource.REPETITIONS: [Action.READ],  # View own repetitions
    },

    "GUARDIAN": {
        # Identity Management - Ward records only
        Resource.STUDENTS: [Action.READ],  # Ward records only
        Resource.STAFF: [Action.READ],  # Ward's teachers
        Resource.EDUCATORS: [Action.READ],  # Ward's teachers
        Resource.GUARDIANS: [Action.READ, Action.UPDATE],  # Own profile

        # Academic Structure - Ward's academic info
        Resource.CLASSES: [Action.READ],  # Ward's class
        Resource.DEPARTMENTS: [Action.READ],  # Ward's department
        Resource.ACADEMIC_LEVELS: [Action.READ],  # Ward's level

        # Curriculum - Ward's subjects
        Resource.SUBJECTS: [Action.READ],  # Ward's subjects
        Resource.ACADEMIC_LEVEL_SUBJECTS: [Action.READ],  # Ward's curriculum
        Resource.STUDENT_SUBJECTS: [Action.READ],  # Ward's enrollments
        Resource.SUBJECT_EDUCATORS: [Action.READ],  # Ward's teachers

        # Assessment - Ward's grades
        Resource.GRADES: [Action.READ],  # Ward's grades
        Resource.TOTAL_GRADES: [Action.READ],  # Ward's total grades

        # Documents & Awards - Ward's records
        Resource.DOCUMENTS: [Action.READ],  # Ward's documents
        Resource.AWARDS: [Action.READ],  # Ward's awards

        # Progression - Ward's progression
        Resource.TRANSFERS: [Action.READ],  # Ward's transfers
        Resource.PROMOTIONS: [Action.READ],  # Ward's promotions
        Resource.REPETITIONS: [Action.READ],  # Ward's repetitions
    }
}

# Contextual access rules for roles that need row-level filtering
CONTEXTUAL_ACCESS_RULES: Dict[str, Dict[Resource, str]] = {
    "EDUCATOR": {
        Resource.STUDENTS: "educator_student_access",
        Resource.GUARDIANS: "educator_guardian_access",
        Resource.GRADES: "educator_grade_access",
        Resource.DOCUMENTS: "educator_document_access",
        Resource.AWARDS: "educator_award_access",
        Resource.TRANSFERS: "educator_transfer_access",
        Resource.PROMOTIONS: "educator_promotion_access",
        Resource.REPETITIONS: "educator_repetition_access",
        Resource.STUDENT_SUBJECTS: "educator_student_subject_access",
    },
    "STUDENT": {
        Resource.STUDENTS: "own_record_only",
        Resource.GUARDIANS: "own_guardian_only",
        Resource.GRADES: "own_grades_only",
        Resource.DOCUMENTS: "own_documents_only",
        Resource.AWARDS: "own_awards_only",
        Resource.TRANSFERS: "own_transfers_only",
        Resource.PROMOTIONS: "own_promotions_only",
        Resource.REPETITIONS: "own_repetitions_only",
        Resource.STUDENT_SUBJECTS: "own_subjects_only",
        Resource.CLASSES: "own_class_only",
        Resource.DEPARTMENTS: "own_department_only",
        Resource.ACADEMIC_LEVELS: "own_level_only",
    },
    "GUARDIAN": {
        Resource.STUDENTS: "ward_records_only",
        Resource.GUARDIANS: "own_record_only",
        Resource.GRADES: "ward_grades_only",
        Resource.DOCUMENTS: "ward_documents_only",
        Resource.AWARDS: "ward_awards_only",
        Resource.TRANSFERS: "ward_transfers_only",
        Resource.PROMOTIONS: "ward_promotions_only",
        Resource.REPETITIONS: "ward_repetitions_only",
        Resource.STUDENT_SUBJECTS: "ward_subjects_only",
        Resource.CLASSES: "ward_class_only",
        Resource.DEPARTMENTS: "ward_department_only",
        Resource.ACADEMIC_LEVELS: "ward_level_only",
    }
}


def has_permission(role: str, resource: Resource, action: Action) -> bool:
    """Check if a role has permission to perform an action on a resource"""
    if role not in PERMISSION_MATRIX:
        return False

    resource_permissions = PERMISSION_MATRIX[role].get(resource, [])
    return action in resource_permissions


def get_role_permissions(role: str) -> Dict[Resource, List[Action]]:
    """Get all permissions for a specific role"""
    return PERMISSION_MATRIX.get(role, {})


def get_contextual_access_rule(role: str, resource: Resource) -> str:
    """Get the contextual access rule for a role and resource"""
    return CONTEXTUAL_ACCESS_RULES.get(role, {}).get(resource, "no_access")


def requires_contextual_access(role: str, resource: Resource) -> bool:
    """Check if a role requires contextual access for a resource"""
    return role in CONTEXTUAL_ACCESS_RULES and resource in CONTEXTUAL_ACCESS_RULES[role]


def generate_permission_strings() -> Set[str]:
    """Generate all possible permission strings in format 'resource:action'"""
    permissions = set()
    for role_perms in PERMISSION_MATRIX.values():
        for resource, actions in role_perms.items():
            for action in actions:
                permissions.add(f"{resource.value}:{action.value}")
    return permissions


ALL_PERMISSIONS = generate_permission_strings()