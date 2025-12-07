# Data Deletion & Archival Patterns

This document defines the rules and patterns for removing data from Kademia. These patterns are **critical** for maintaining data integrity, preventing accidental data loss, and ensuring safe future scaling.

---

## Core Integrity Goals

1. **No fragmented orphaned data** - Related records must be handled together
2. **No silent mass deletion** - Cascades require explicit authorization
3. **Archived data stays accessible** - Admins can always query archived records

---

## Types of Data Removal

| Type | Behavior | Access Level | Use Case                             |
|------|----------|--------------|--------------------------------------|
| **Archive** | Sets `is_archived=true`, preserves record forever | Authorized Users | Graduation, resignation, end of term |
| **Safe Delete** | Deletes only if no active dependencies exist | Authorized Users | Cleanup of unused/draft entities     |
| **Hard Delete** | Forces deletion with cascade, requires export | Superusers Only | Data purge, Data Protection requests |

### When to Use Each

```
┌─────────────────────────────────────────────────────────────┐
│  Student graduates                    ->> ARCHIVE           │
│  Staff resigns                        ->> ARCHIVE           │
│  Unused draft created by mistake ->> SAFE DELETE    │
│  Test data cleanup in staging         ->> HARD DELETE       │
│  Fata Protection "right to be forgotten ->> HARD DELETE     │
└─────────────────────────────────────────────────────────────┘
```

---

## Relationship Ownership Model

The system distinguishes between **owned** and **referenced** relationships to determine deletion behavior.

### Owned Relationships ->> CASCADE

The parent entity **owns** the child. Deleting/archiving the parent cascades to children.

```
Student OWNS:
├── grades
├── total_grades
├── subjects_taken (StudentSubject)
├── documents_owned (StudentDocument)
├── awards_earned (StudentAward)
├── promotions
├── classes_repeated (Repetition)
└── department_transfers

Educator OWNS:
├── qualifications (EducatorQualification)
└── subject_assignments (SubjectEducator)

Staff OWNS:
└── role_changes (RoleHistory)
```

**Behavior**: When a Student is deleted, all their grades, documents, awards, and progression records are automatically deleted.

### Referenced Relationships ->> NULLIFY or RESTRICT

The entity **uses** a shared resource but doesn't own it.

```
Staff USES (SET NULL on delete):
├── department_id ->> StaffDepartment
├── job_title_id ->> StaffJobTitle
└── current_role_id ->> Role

Student USES (SET NULL on delete):
├── level_id ->> AcademicLevel
├── class_id ->> Classes
└── department_id ->> StudentDepartment

Classes USES (SET NULL on delete):
├── supervisor_id ->> Educator
├── student_rep_id ->> Student
└── assistant_rep_id ->> Student
```

**Behavior**: Deleting a Role doesn't delete Staff members. Instead, their `role_id` is set to NULL.

### Protected Relationships ->> RESTRICT

Critical references that must be explicitly handled before deletion.

```
Student REQUIRES (RESTRICT):
└── guardian_id ->> Guardian  (must reassign guardian first)

Subject REQUIRES (RESTRICT):
└── department_id ->> StudentDepartment  (must reassign or archive subjects first)

AcademicLevelSubject REQUIRES (RESTRICT):
├── level_id ->> AcademicLevel
└── subject_id ->> Subject
```

**Behavior**: Attempting to delete a Guardian with active wards raises an error. The admin must first reassign the students to another guardian.

---

## Dependency Configuration

All deletion dependencies are centralized in `dependency_config.py`. This is the single source of truth for what blocks or cascades with each entity.

### Structure

```python
DEPENDENCY_CONFIG = {
    EntityModel: [
        (relationship_name, related_model, fk_field, display_name),
        ...
    ]
}
```

### Full Dependency Map

| Entity | Depends On | FK Field | Display Name |
|--------|-----------|----------|--------------|
| **StudentDepartment** | Student | department_id | students |
| | Subject | department_id | subjects |
| | DepartmentTransfer | new_department_id | transfers |
| **AcademicLevel** | AcademicLevelSubject | level_id | academic level subjects |
| | Classes | level_id | classes |
| | Student | level_id | students |
| **Classes** | Student | class_id | students |
| **StaffJobTitle** | Staff | job_title_id | staff members |
| **StaffDepartment** | Staff | department_id | staff members |
| **Guardian** | Student | guardian_id | wards |
| **Student** | StudentDocument | student_id | documents |
| | StudentAward | student_id | awards |
| | StudentSubject | student_id | subject enrollments |
| | Grade | student_id | grades |
| | TotalGrade | student_id | total grades |
| | Repetition | student_id | class repetitions |
| | Promotion | student_id | promotions |
| | DepartmentTransfer | student_id | department transfers |
| **Staff** | RoleHistory | staff_id | permission changes |
| **Educator** | EducatorQualification | educator_id | qualifications |
| | SubjectEducator | educator_id | subject assignments |
| | RoleHistory | staff_id | permission changes |
| **Subject** | AcademicLevelSubject | subject_id | academic level assignments |
| **AcademicLevelSubject** | StudentSubject | academic_level_subject_id | enrolled students |
| | SubjectEducator | academic_level_subject_id | assigned educators |
| **StudentSubject** | Grade | student_subject_id | grades |
| | TotalGrade | student_subject_id | total grades |

### Leaf Entities (No Dependencies)

These can be safely deleted without dependency checks:

- `Promotion`, `Repetition`, `DepartmentTransfer`
- `EducatorQualification`, `SubjectEducator`
- `Grade`, `TotalGrade`
- `StudentAward`, `StudentDocument`
- `RoleHistory`

---

## Service Implementations

### ArchiveService

Handles soft-deletion by setting `is_archived = true` on entities and their owned children.

```
┌─────────────────────────────────────────────────────────────┐
│                    ARCHIVE REQUEST                          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  1. check_active_dependencies_exists()                      │
│     - Load DEPENDENCY_CONFIG for entity type                │
│     - For each dependency:                                  │
│       SELECT EXISTS WHERE fk = target_id AND is_archived=F  │
│     - Collect display names of blocking dependencies        │
└─────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┴───────────────┐
              │                               │
              ▼                               ▼
┌──────────────────────────┐    ┌──────────────────────────────┐
│  Dependencies Found      │    │  No Dependencies             │
│  ->> Return error with     │    │  ->> Proceed to archive        │
│    blocking entity names │    └──────────────────────────────┘
└──────────────────────────┘                  │
                                              ▼
┌─────────────────────────────────────────────────────────────┐
│  2. cascade_archive_object()                                │
│     - For each relationship in DEPENDENCY_CONFIG:           │
│       - Get related objects via back_populates              │
│       - Call .archive() on each                             │
│     - Archive parent entity                                 │
│     - Commit transaction                                    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  3. Return Result                                           │
│     {                                                       │
│       "entity_id": uuid,                                    │
│       "archived_entities": {                                │
│         "grades": 45,                                       │
│         "documents": 3,                                     │
│         "awards": 2                                         │
│       }                                                     │
│     }                                                       │
└─────────────────────────────────────────────────────────────┘
```

### DeleteService

Handles permanent deletion with safety checks.

```
┌─────────────────────────────────────────────────────────────┐
│                    DELETE REQUEST                           │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  1. Check Export Status (for hard delete)                   │
│     - entity.is_exported must be True                       │
│     - Prevents accidental permanent data loss               │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  2. check_active_dependencies_exists()                      │
│     - Same as archive flow                                  │
│     - Returns list of blocking entity types                 │
└─────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┴───────────────┐
              │                               │
              ▼                               ▼
┌──────────────────────────┐    ┌──────────────────────────────┐
│  SAFE DELETE MODE        │    │  FORCE DELETE MODE           │
│  ->> Block if any deps     │    │  ->> Export data first         │
│    exist                 │    │  ->> Cascade delete children   │
│  ->> Delete only if clean  │    │  ->> Nullify shared references │
└──────────────────────────┘    │  ->> Delete parent             │
                                └──────────────────────────────┘
```

---

## FK Delete Rules Reference

### CASCADE (Owned Children)

| Parent Table | Child Table | FK Column |
|-------------|-------------|-----------|
| staff | educators | id |
| staff | admin_staff | id |
| staff | support_staff | id |
| staff | system | id |
| staff | access_level_changes | staff_id |
| students | student_subjects | student_id |
| students | grades | student_id |
| students | total_grades | student_id |
| students | repetitions | student_id |
| students | promotions | student_id |
| students | student_awards | student_id |
| students | student_documents | student_id |
| students | department_transfers | student_id |
| educators | educator_qualifications | educator_id |
| educators | subject_educators | educator_id |
| roles | role_permissions | role_id |
| permissions | role_permissions | permission_id |

### SET NULL (Shared Resources)

| Referenced Table | Referencing Table | FK Column |
|-----------------|-------------------|-----------|
| academic_levels | students | level_id |
| classes | students | class_id |
| student_departments | students | department_id |
| educators | classes | supervisor_id |
| students | classes | student_rep_id |
| students | classes | assistant_rep_id |
| staff | staff_departments | manager_id |
| staff_departments | staff | department_id |
| staff_job_titles | staff | job_title_id |
| roles | staff | current_role_id |

### RESTRICT (Protected References)

| Referenced Table | Referencing Table | FK Column |
|-----------------|-------------------|-----------|
| guardians | students | guardian_id |
| subjects | academic_level_subjects | subject_id |
| academic_levels | academic_level_subjects | level_id |
| academic_levels | classes | level_id |
| academic_level_subjects | student_subjects | academic_level_subject_id |
| student_subjects | grades | student_subject_id |
| student_subjects | total_grades | student_subject_id |
| student_departments | subjects | department_id |
| staff | grades | graded_by |
| staff | promotions | status_completed_by |
| staff | repetitions | status_completed_by |
| staff | department_transfers | status_completed_by |


---

## Error Handling

### Dependency Blocking Error

When an entity cannot be archived/deleted due to active dependencies:

```python
raise DeletionDependencyError(
    entity_model="AcademicLevel",
    entity_id=uuid,
    blocking_entities=["classes", "students", "academic level subjects"]
)

# User sees:
# "Cannot archive AcademicLevel. Active dependencies exist: 
#  classes, students, academic level subjects"
```

### Cascade Failure Error

When cascade archival fails midway:

```python
raise CascadeArchivalError(
    f"[{relationship_name}] Cascade failed: {original_error}"
)
# Transaction is rolled back automatically
```

