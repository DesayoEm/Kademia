
Kademia is a modular, scalable backend system for managing academic institutions. 

It supports user roles, academic structures, progression workflows, and lifecycle operations with full audit tracking and export functionality.

## System Architecture
---

## Tech Stack
- **Python 3.12**
- **FastAPI**
- **SQLAlchemy ORM**
- **PostgreSQL**
- **Redis** 

### Database Design
- UUID-based identification system
- Audit trail implementation (created_by, modified_by, etc.)
- Archive support across all entities
- Indexing for performance optimization

### Core Architecture
- Repository + Factory + Service layering
- Decorator-based error and FK/unique violation handling
- SQLAlchemy + PostgreSQL with Redis for token tracking
- Archival system and with soft-deletion and restoring of entities


## Core Modules
---

### User & Identity Management
- Students, Guardians, Staff (Educator, Admin, Support, System)
- Role and access level auditing (AccessLevelChange)
- Guardian-ward relationships
- Staff departments and roles with audit trails

### Academic Structure
- Academic levels, classes, departments
- Curriculum mappings 
- Educator-subject assignments 


### Progression Workflows
- Repetition, Promotion, Graduation workflows
- Class and Department Transfers
- Approval statuses with audit and rejection logging

### Assessments
- Grade and TotalGrade tracking
- Subject-wise grading with type differentiation (exam, test, etc.)
- Educator-linked grading and feedback

### Documents & Awards
- Document uploads per student
- Award management with file support

