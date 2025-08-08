
Kademia is a modular, scalable backend system for managing academic institutions. 

## Tech Stack
- **Python 3.12**
- **FastAPI**
- **SQLAlchemy ORM**
- **PostgreSQL**
- **Redis** 


## Core Architecture
- Repository + Factory + Service layering
- Decorator-based error and FK/unique violation handling
- SQLAlchemy + PostgreSQL with Redis for token tracking
- Archival system and with soft-deletion and restoring of entities


## Design Decisions

**UUID-Based Identification**

Chose UUIDs over auto-incrementing integers for all primary keys to support distributed systems and prevent enumeration attacks.

**Three-Layer Architecture (Repository + Factory + Service)**

Implemented strict separation between data access (Repository), object creation (Factory), and business logic (Service) to maintain testability and prevent the "God controller" anti-pattern common in academic management systems.

**Cascade Archival System**

Built a dependency-aware archival system that prevents orphaned data while maintaining referential integrity. When archiving a student, the system automatically handles their grades, documents, and awards avoiding the problem of "soft delete" creating inconsistent data states.

**Cascade Deletion System**

Built a dependency-aware deletion system that restricts data deletion to prevent orphaned data and maintain referential integrity.

**Polymorphic Staff Inheritance**

Used joined table inheritance for staff types (Educator, Admin, Support) to handle role-specific relationships efficiently. Educators have complex dependencies (qualifications, subject assignments, mentored departments) while other staff types remain lightweight.

**Audit-First Design**

Every entity includes comprehensive audit trails (created_by, modified_by, archived_by) with enum-based reasons. Critical for educational institutions that require compliance reporting and accountability tracking.

**Comprehensive Decorator-Based Error Handling**

Domain-specific exception hierarchy with middleware that translates technical errors into actionable user messages. Foreign key violations and unique constraint errors are centralized using decorators to provide consistent, user-friendly error messages across all endpoints while maintaining detailed logging for debugging.





## Core Modules

### User & Identity Management
- Students, Guardians, Staff (Educator, Admin, Support, System)
- Role and access level auditing 
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
- Subject-wise grading with type differentiation (exam, assignments, etc.)
- Educator-linked grading and feedback

### Documents & Awards
- Document uploads per student
- Award management with file support

