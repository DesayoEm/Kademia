# Data Deletion and Archival Notes

## Overview
The deletion handling rules I've mentioned in this doc are **critical** to maintain data integrity, avoid accidental data loss and fragmentation, and ensure safe future scaling and maintenance.


## Data Integrity Goals

- **No fragmented orphaned data.**
- **No silent mass deletion.**
- **Archived data stays available for admins even after normal users cannot see it.**

---

## Default Foreign Key Strategy

- **RESTRICT** deletion everywhere by default.
- **SET NULL** only for minor fields (e.g., staff roles, student guardians) where data fragmentation is manageable.
- **Never** use **CASCADE** directly on critical entities.

---

## Export System

- Before hard deleting any entity, (Staff, Students, AcademicLevels), the entity and its related entities must be exported.
- Export options:
  - **Excel** 
  - **CSV**
  - **PDF** (human-readable archive)

---


## Types of Data Removal

| Type | Behavior                                                       | Who Can See | Notes                                                                                              |
|:---|:---------------------------------------------------------------|:---|:---------------------------------------------------------------------------------------------------|
| **Archive** | Hides the record form normal queries but preserves it forever. | Admins / Special Users. | Default for students, staff, and important entities (e.g., graduation, resignation).               |
| **Safe Deletion** | Deletes the record if no dependencies exist.                   | Authorized Users. | Only allowed if there are no critical dependencies (e.g., no classes, grades, or subjects linked). |
| **Hard Deletion** | Forcefully deletes a record and its dependencies.              | Admins / Superusers only. | Discouraged. Must export data first. Requires manual dependency cleanup.                           |

## 1. Nullify Relationship

### Description
Entities that are **referenced** but **not owned** should NOT cause dependent deletions. Instead, their deletion should either:
* Raise an error if still referenced.
* Or in forced mode, set the referencing field to `NULL`.

### Examples
| Entity            | Related Entity | On Deletion                        |
|-------------------|---------------|------------------------------------|
| StaffRole         | Staff | Set `staff.role_id = NULL`         |
| StudentDepartment | Staff | Set `student.department_id = NULL` |

### Behavior
* Normal Delete: Raise error if active references exist.
* Forced Delete: Set foreign key fields to NULL before deleting.

### Rationale
Roles, Departments are **shared resources**. Staff "uses" a role, but is not "owned" by a role. Deleting a role must not delete Staff accounts.


## 2. Cascade True Deletion

### Description
Entities that **own** dependent records must cascade delete them safely before being deleted.

### Examples
| Entity | Related Entity                      | On Deletion |
|--------|-------------------------------------|-------------|
| Student | Grades, Subjects, Documents         | Cascade delete all grades, subjects, documents |
| Staff (User) | Qualifications, Subject assignments | Cascade delete all owned records |

### Behavior
* Normal Delete: Block if dependencies exist.
* Forced Delete: Export, cascade delete all related records, then delete the entity.

### Rationale
A Student "owns" their grades and subjects. A Staff "owns" their qualifications and assignment history. Deleting the parent should delete all truly owned child records.


##  General Rules
* **Export First**: Always export data before force deleting.
* **Mark Exported**: Entities must be marked as `is_exported = True` before deletion.
* **Document Explicit Relationships**: Each model should clearly define whether its related entities are "owned" or "referenced."
* **Error Handling**: Raise clean, specific dependency errors when deletion is blocked.


##  Examples

| Scenario | Action |
|:---|:---|
| Deleting a `Role` | Must check if Staff members still have the role. |
| Staff linked to Role | Two Options: |
| a) Force delete Staff (dangerous) | Deleting staff will trigger deletions in Grades, Awards, Subjects, Departments, etc. |
| b) Reassign Staff to another Role | Safer. Allow admins to select a replacement role for all staff before deletion. |

**Important:**  
- Deleting a role without reassignment can cause a dangerous cascade of deletion.
- Staff may exist without a role (role_id = NULL) if handled manually.


## General Rules
* **Export First**: Always export data before force deleting.
* **Mark Exported**: Entities must be marked as `is_exported = True` before deletion.
* **Document Explicit Relationships**: Each model should clearly define whether its related entities are "owned" or "referenced."
* **Error Handling**: Raise clean, specific dependency errors when deletion is blocked.


## Developer Notes
If adding a new model:
* Decide early: **Nullify or Cascade?**
All entity deletion behavior must be documented in:
* Dependency Configuration (`dependency_config.py`)
* Deletion Dependency Map (`error_maps.py`)



