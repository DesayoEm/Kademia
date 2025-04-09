# Foreign Key References in Kademia Database

This document outlines all tables/columns that are referenced as foreign keys in other tables, organized by the source table. This will help with properly handling deletion constraints.

## `academic_levels` Table
- `id` referenced in:
  - `AcademicLevelSubject.level_id` (RESTRICT)
  - `Classes.level_id` (RESTRICT)
  - `Student.level_id` (SET NULL)
  - `Repetition.previous_level_id` (RESTRICT)
  - `Repetition.new_level_id` (RESTRICT)
  - `StudentDepartmentTransfer.previous_level_id` (RESTRICT)
  - `StudentDepartmentTransfer.new_level_id` (RESTRICT)

## `classes` Table
- `id` referenced in:
  - `Student.class_id` (SET NULL)
  - `Repetition.previous_class_id` (RESTRICT)
  - `Repetition.new_class_id` (RESTRICT)
  - `ClassTransfer.previous_class_id` (RESTRICT)
  - `ClassTransfer.new_class_id` (RESTRICT)
  - `StudentDepartmentTransfer.previous_class_id` (RESTRICT)
  - `StudentDepartmentTransfer.new_class_id` (RESTRICT)

## `educators` Table
- `id` referenced in:
  - `AcademicLevelSubject.educator_id` (RESTRICT)
  - `SubjectEducator.educator_id` (RESTRICT)
  - `Classes.supervisor_id` (SET NULL)
  - `StudentDepartment.mentor_id` (RESTRICT)

## `guardians` Table
- `id` referenced in:
  - `Student.guardian_id` (RESTRICT)

## `staff` Table
- `id` referenced in:
  - Every model with AuditMixins or ArchiveMixins (created_by, last_modified_by, archived_by)
  - `Educator.id` (CASCADE)
  - `AdminStaff.id` (CASCADE)
  - `SupportStaff.id` (CASCADE)
  - `System.id` (CASCADE)
  - `StaffDepartment.manager_id` (SET NULL)
  - `Grade.graded_by` (RESTRICT)
  - `Repetition.status_updated_by` (RESTRICT)
  - `ClassTransfer.status_updated_by` (RESTRICT)
  - `StudentDepartmentTransfer.status_updated_by` (RESTRICT)
  - `AccessLevelChange.staff_id` (CASCADE)
  - `AccessLevelChange.changed_by_id` (RESTRICT)

## `staff_departments` Table
- `id` referenced in:
  - `Staff.department_id` (SET NULL)

## `staff_roles` Table
- `id` referenced in:
  - `Staff.role_id` (SET NULL)

## `student_departments` Table
- `id` referenced in:
  - `Subject.department_id` (RESTRICT)
  - `Student.department_id` (SET NULL)
  - `StudentDepartmentTransfer.previous_department_id` (RESTRICT)
  - `StudentDepartmentTransfer.new_department_id` (RESTRICT)

## `students` Table
- `id` referenced in:
  - `Classes.student_rep_id` (SET NULL)
  - `Classes.assistant_rep_id` (SET NULL)
  - `StudentDepartment.student_rep_id` (RESTRICT)
  - `StudentDepartment.assistant_rep_id` (RESTRICT)
  - `StudentSubject.student_id` (CASCADE)
  - `Grade.student_id` (CASCADE)
  - `TotalGrade.student_id` (CASCADE)
  - `Repetition.student_id` (CASCADE)
  - `StudentAward.owner_id` (CASCADE)
  - `StudentDocument.owner_id` (RESTRICT)
  - `ClassTransfer.student_id` (CASCADE)
  - `StudentDepartmentTransfer.student_id` (CASCADE)

## `subjects` Table
- `id` referenced in:
  - `AcademicLevelSubject.subject_id` (RESTRICT)
  - `StudentSubject.subject_id` (RESTRICT)
  - `SubjectEducator.subject_id` (RESTRICT)
  - `Grade.subject_id` (RESTRICT)
  - `TotalGrade.subject_id` (RESTRICT)

## Summary of Delete Rules

### CASCADE
- `Educator.id` → `staff.id`
- `AdminStaff.id` → `staff.id`
- `SupportStaff.id` → `staff.id`
- `System.id` → `staff.id`
- `StudentSubject.student_id` → `students.id`
- `Grade.student_id` → `students.id`
- `TotalGrade.student_id` → `students.id`
- `Repetition.student_id` → `students.id`
- `StudentAward.owner_id` → `students.id`
- `ClassTransfer.student_id` → `students.id`
- `StudentDepartmentTransfer.student_id` → `students.id`
- `AccessLevelChange.staff_id` → `staff.id`

### SET NULL
- `Student.level_id` → `academic_levels.id`
- `Student.class_id` → `classes.id`
- `Student.department_id` → `student_departments.id`
- `Classes.supervisor_id` → `educators.id`
- `StaffDepartment.manager_id` → `staff.id`
- `Classes.student_rep_id` → `students.id`
- `Classes.assistant_rep_id` → `students.id`
- `Staff.department_id` → `staff_departments.id`
- `Staff.role_id` → `staff_roles.id`

### RESTRICT
- All other foreign key relationships use RESTRICT, which prevents deletion if references exist

## Notes for Implementation
- When deleting `students`, most related records use CASCADE, but `StudentDocument.owner_id` uses RESTRICT
- When deleting `staff`, handle cascade deletion for staff subtypes (educators, admin, support, system)
- `academic_levels`, `classes`, and `subjects` are heavily referenced with RESTRICT, requiring careful handling
- Consider adding soft-delete functionality where RESTRICT constraints would prevent necessary operations
