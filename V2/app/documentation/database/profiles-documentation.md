# School Management System Database Documentation

## Overview
This document describes the database schema for the school management system. The system uses PostgreSQL as the database and SQLAlchemy as the ORM. All tables include audit trails and soft delete capabilities through mixins.

## Common Features
All tables inherit the following mixins:
- **TimeStampMixins**: Tracks creation and update timestamps
- **AuditMixins**: Tracks who created and updated records
- **SoftDeleteMixins**: Enables soft deletion with reason tracking

## Tables

### Subjects
Represents academic subjects taught in the school.

**Fields:**
- `id`: UUID (Primary Key)
- `name`: String(30)
- `class_level`: Enum(ClassLevel)
- `department_type`: Enum(SubjectDepartmentType)
- `is_compulsory`: Boolean (default: True)

**Relationships:**
- `student`: One-to-Many with Students
- `grades`: One-to-Many with Grades
- `total_grades`: One-to-Many with TotalGrades
- `student_subjects`: One-to-Many with StudentSubjects
- `educators`: One-to-Many with EducatorSubjects

### Grades
Stores individual grade entries for students.

**Fields:**
- `id`: UUID (Primary Key)
- `student_id`: UUID (Foreign Key to students, CASCADE on delete)
- `subject_id`: UUID (Foreign Key to subjects, SET NULL on delete)
- `department_id`: UUID (Foreign Key to departments, SET NULL on delete)
- `academic_year`: Integer
- `term`: Enum(Term)
- `type`: Enum(GradeType)
- `marks`: Integer
- `file_url`: String(300), optional
- `graded_by`: UUID (Foreign Key to staff)

**Indexes:**
- `idx_subject_id`
- `idx_marks`
- `idx_graded_by`
- `idx_grade_academic_year`

**Relationships:**
- `subject`: Many-to-One with Subjects
- `student`: Many-to-One with Students
- `grader`: Many-to-One with Staff
- `department`: Many-to-One with Department

### TotalGrades
Aggregates total grades for students per subject.

**Fields:**
- `id`: UUID (Primary Key)
- `student_id`: UUID (Foreign Key to students, CASCADE on delete)
- `subject_id`: UUID (Foreign Key to subjects, SET NULL on delete)
- `academic_year`: Integer
- `term`: Enum(Term)
- `total_marks`: Float
- `rank`: Integer, optional

**Constraints:**
- Unique constraint on (student_id, subject_id, academic_year, term)

**Indexes:**
- `idx_total_grade_subject_id`
- `idx_total_marks`
- `idx_total_grade_academic_year`

### StudentSubjects
Maps students to their enrolled subjects.

**Fields:**
- `id`: UUID (Primary Key)
- `student_id`: UUID (Foreign Key to students, CASCADE on delete)
- `subject_id`: UUID (Foreign Key to subjects, SET NULL on delete)
- `academic_year`: Integer
- `term`: Enum(Term)
- `is_active`: Boolean (default: True)
- `title`: String(50)

### EducatorSubjects
Maps educators to subjects they teach.

**Fields:**
- `id`: UUID (Primary Key)
- `educator_id`: UUID (Foreign Key to staff, SET NULL on delete)
- `subject_id`: UUID (Foreign Key to subjects, SET NULL on delete)
- `term`: Enum(Term)
- `academic_year`: Integer
- `is_active`: Boolean (default: False)

### Repetitions
Tracks student class repetitions.

**Fields:**
- `id`: UUID (Primary Key)
- `student_id`: UUID (Foreign Key to students, CASCADE on delete)
- `academic_year`: Integer
- `from_class_level`: ClassLevel (Foreign Key to classes)
- `to_class_level`: ClassLevel (Foreign Key to classes)
- `from_class_id`: UUID (Foreign Key to classes)
- `to_class_id`: UUID (Foreign Key to classes)
- `reason`: String(500)
- `status`: Enum(ApprovalStatus), default: PENDING
- `status_updated_by`: UUID (Foreign Key to staff)
- `status_updated_at`: DateTime
- `rejection_reason`: String(500), optional

**Indexes:**
- `idx_repetition_status`
- `idx_student_status`
- `idx_student_academic_year`
- `idx_from_class`
- `idx_to_class`

### StudentTransfers
Manages student transfers between departments.

**Fields:**
- `id`: UUID (Primary Key)
- `student_id`: UUID (Foreign Key to students, CASCADE on delete)
- `academic_year`: Integer
- `from_class_level`: ClassLevel (Foreign Key to classes)
- `to_class_level`: ClassLevel (Foreign Key to classes)
- `from_department`: UUID (Foreign Key to departments)
- `to_department`: UUID (Foreign Key to departments)
- `reason`: String(500)
- `status`: Enum(ApprovalStatus), default: PENDING
- `status_updated_by`: UUID (Foreign Key to staff)
- `status_updated_at`: DateTime
- `rejection_reason`: String(500), optional

**Indexes:**
- `idx_transfer_status`
- `idx_student_transfer_status`
- `idx_student-transfer_academic_year`
- `idx_from_department`
- `idx_to_department`

## Notes
- All tables use UUIDs as primary keys
- Deletion strategies vary between CASCADE and SET NULL depending on the relationship
- Extensive use of indexes for performance optimization
- Approval workflows implemented for student transfers and repetitions
- All datetime fields are timezone-aware