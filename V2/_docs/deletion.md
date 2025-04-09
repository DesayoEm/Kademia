# Data Deletion and Archival Policy

## 1. Types of Removal

| Type | Behavior | Who Can See | Notes |
|:---|:---|:---|:---|
| **Archive** | Hides the record but preserves it forever. | Admins / Special Users. | Default for students, staff, and important entities (e.g., graduation, resignation). |
| **Safe Deletion** | Deletes the record if no dependencies exist. | Authorized Users. | Only allowed if no critical dependencies (e.g., no classes, grades, or subjects linked). |
| **Hard Deletion** | Forcefully deletes a record and its dependencies. | Admins / Superusers only. | Dangerous. Must export data first. Requires manual dependency cleanup. |

---

## 2. Default Foreign Key Strategy

- **RESTRICT** deletion everywhere by default.
- **SET NULL** only for minor fields (e.g., staff roles, student guardians) where data fragmentation is manageable.
- **Never** use **CASCADE** directly on critical entities.

---

## 3. Role Deletion Process

| Scenario | Action |
|:---|:---|
| Deleting a `Role` | Must check if Staff members still have the role. |
| Staff linked to Role | Two Options: |
| a) Force delete Staff (dangerous) | Deleting staff will trigger deletions in Grades, Awards, Subjects, Departments, etc. |
| b) Reassign Staff to another Role | Safer. Allow admins to select a replacement role for all staff before deletion. |

**Important:**  
- Deleting a role without reassignment can cause a dangerous cascade of deletion.
- Staff may exist without a role (role_id = NULL) if handled manually.

---

## 4. Staff Deletion Process

| Step | Action |
|:---|:---|
| 1. Export staff data | Create a PDF or Excel export before deleting. |
| 2. Delete dependents | Grades, Subjects, Awards, etc. |
| 3. Delete Staff entity | Only after safe cleanup. |
| 4. Audit the deletion | Log all hard deletions for recovery. |

---

## 5. Export System

- Before hard deleting important entities (Staff, Students, AcademicLevels), the system must allow **data export**.
- Export options:
  - **PDF** (human-readable archive)
  - **Excel** (raw database table export)

---

## 6. Permissions

| Action | Allowed for |
|:---|:---|
| Archive | Regular Users / Admins. |
| Safe Delete | Authorized Users (no dependencies). |
| Hard Delete | Admins / Superusers only. |

---

## 7. Data Integrity Goals

- **No fragmented orphaned data.**
- **No silent mass deletion.**
- **Everything dangerous must be deliberate and logged.**
- **Archived data stays available for admins even after normal users cannot see it.**

---

# 🎯 Core Philosophy

> "Normal users archive, managers safely delete isolated entities, and admins perform hard deletions after exporting and cleaning up dependents."

