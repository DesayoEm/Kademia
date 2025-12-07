Kademia is an academic management system designed to handle the complex relationships within an educational institution.
The database supports three distinct user types (Staff, Students, Guardians) with Role-Based Access Control (RBAC) for managing permissions across different educational contexts.

## Domain Architecture

The database is organized into **7 core domains**:

| Domain | Purpose | Key Tables |
|--------|---------|------------|
| **Identity** | User management across all user types | `staff`, `educators`, `students`, `guardians` |
| **Academic Structure** | Institution organization | `academic_levels`, `classes`, `student_departments` |
| **Curriculum** | Subject and enrollment management | `subjects`, `academic_level_subjects`, `student_subjects`, `subject_educators` |
| **Assessment** | Grading system | `grades`, `total_grades` |
| **Progression** | Student academic advancement | `promotions`, `repetitions` |
| **Transfer** | Department transfers | `department_transfers` |
| **Documents** | Student records and awards | `student_documents`, `student_awards` |
| **Staff Management** | Staff organization | `staff_departments`, `staff_job_titles`, `educator_qualifications` |
| **RBAC** | Authorization system | `roles`, `permissions`, `role_permissions`, `role_history` |

---


## Key  Patterns

### 1. Soft Delete (Archive Pattern)
All major entities use the `ArchiveMixins` providing:
- `is_archived` - Boolean flag
- `archived_at` - Timestamp
- `archive_reason` - Enum-based reason
- `archived_by` - Staff reference (implicit)

### 2. Audit Trail
Entities inherit `AuditMixins` providing:
- `created_by` → FK to `staff.id`
- `last_modified_by` → FK to `staff.id`
- Relationships to Staff for audit queries

All entities also include `TimeStampMixins`:
- `created_at` - Auto-set on creation
- `last_modified_at` - Auto-updated on modification

---

## Entity Relationship Details

### Identity Domain and User Type Hierarchy

#### Staff Hierarchy (Single Table Inheritance)

```
Staff (base)
├── Educator      - Teaching staff with qualifications and subject assignments
├── AdminStaff    - Administrative personnel
├── SupportStaff  - Support personnel
└── System        - System user for bootstrap operations (UUID: 00000000-...)
```

The `staff_type` column acts as the discriminator with polymorphic identity.

### Separate User Tables
- **Students** - Enrolled learners with academic placement
- **Guardians** - Parents/guardians linked to students



### Academic Structure Domain

**AcademicLevel** - Grade levels (JSS1, SSS1, etc.)
- `display_order` - UI ordering
- `promotion_rank` - Determines progression sequence
- `is_final` - Marks graduation level

**Classes** - Physical class sections
- Belongs to academic level
- Has supervisor (Educator) and student representatives
- Unique constraint on level + code combination

**StudentDepartment** - Academic streams (Science, Arts, Commercial)
- Has mentor (Educator) and student representatives
- Links to subjects for department-specific curriculum

### Curriculum Domain

**Subject** - Base subject definitions (Mathematics, English, etc.)
- Optionally linked to a department

**AcademicLevelSubject** - Subject + Level combination
- Creates the actual curriculum entries
- Tracks if subject is elective
- Has unique code for identification

**StudentSubject** - Student enrollment in subjects
- Links student → academic_level_subject
- Scoped by academic_session and term
- Unique per student/subject/session/term

**SubjectEducator** - Teacher assignments
- Links educator → academic_level_subject
- Tracks assignment date and session

### Assessment Domain

**Grade** - Individual assessment scores
- Links to student and student_subject
- Has type (exam, test, assignment), score, weight
- Records grader and grading date
- `student_id` is denormalized for query performance

**TotalGrade** - Aggregated scores per subject enrollment
- One-to-one with StudentSubject
- Computed from individual grades

### Progression Domain

**Promotion** - Student advancement records
- Tracks previous and promoted level
- Approval workflow (status, completed_by, completed_at)

**Repetition** - Class repeat records
- Similar structure to Promotion
- Records failed level and repeat level
- Requires reason for repetition

### Transfer Domain

**DepartmentTransfer** - Department change records
- Tracks previous and new department
- Approval workflow
- One transfer per student per session

### Documents Domain

**StudentDocument** - Uploaded documents
- Types: transcripts, certificates, etc.
- S3 key for file storage
- Unique per student/title/session

**StudentAward** - Student achievements
- Title, description, S3 key
- Unique per student/title/session

### Staff Management Domain

**StaffDepartment** - Organizational units for staff
- Has manager (Staff reference)

**StaffJobTitle** - Position titles
- Name and description

**EducatorQualification** - Teacher credentials
- Validity tracking (temporary/permanent, expiry)
- Cascade delete with educator

### RBAC Domain

**Permission** - Resource + Action combinations
- `resource` - What entity (Student, Grade, etc.)
- `action` - What operation (Create, Read, Update, etc.)

**Role** - Named permission groups
- Hierarchical ranking
- Links to permissions via junction table

**RolePermission** - Junction table for Role ↔ Permission

**RoleHistory** - Audit trail for role changes
- Tracks previous/new role
- Effective date ranges
- Change reason and who made the change

---

## Foreign Key Strategies

| Strategy | Use Case |
|----------|----------|
| `CASCADE` | Child records deleted with parent (grades → student) |
| `RESTRICT` | Prevent deletion if references exist (department → subject) |
| `SET NULL` | Clear reference but keep record (supervisor → class) |

---

## Constraints Summary

### Unique Constraints
- `academic_levels.name`, `display_order`, `promotion_rank`
- `classes.(level_id, code)`, `classes.(level_id, order)`
- `student_departments.name`, `code`
- `subjects.name`
- `academic_level_subjects.(level_id, subject_id)`
- `student_subjects.(student_id, academic_level_subject_id, academic_session, term)`
- `students.student_id`
- `staff.email_address`, `phone`
- `guardians.email_address`, `phone`
- `roles.name`

### Composite Keys
- `role_permissions.(role_id, permission_id)`

---

## Indexes

Indexes are defined for:
- Foreign key columns (automatic lookups)
- Search fields (names, codes, emails)
- Filter columns (status, session, term)
- Composite queries (student + subject + score)

