# Academic Management System (AMS)
## Product Requirements Document

### Project Overview
The Academic Management System (AMS) is designed to manage student records, academic performance, and school operations for a secondary school environment. The system handles student information, course management, grade calculations, and academic workflows with proper security and scalability.

### System Architecture

#### Backend Stack
- Framework: FastAPI
- Database: PostgreSQL
- ORM: SQLAlchemy
- Authentication: JWT + OAuth2
- File Storage: Cloud storage (S3 or similar) for documents and images
- Cache: Redis for session management

### Database Schema

#### Core Tables

1. **students**
```sql
Table students {
  id uuid [pk]
  student_id varchar [unique]
  first_name varchar
  last_name varchar
  class char [ref: > classes.id]
  department_id uuid [ref: > departments.id]
  email varchar [unique]
  parent_id uuid [ref: > parents.id]
  emergency_phone varchar
  image_url varchar
  admission_date date
  leaving_date date
  is_graduated boolean
  is_enrolled boolean
  created_at timestamp
  updated_at timestamp
}
```

2. **educators**
```sql
Table educators {
  id uuid [pk]
  first_name varchar
  last_name varchar
  email varchar [unique]
  phone varchar
  date_joined date
  date_left date
  is_active boolean
  created_at timestamp
  updated_at timestamp
}
```

3. **parents**
```sql
Table parents {
  id uuid [pk]
  first_name varchar
  last_name varchar
  address varchar
  email varchar [unique]
  created_at timestamp
  updated_at timestamp
}
```

4. **departments**
```sql
Table departments {
  id uuid [pk]
  name varchar
  code varchar [unique]
  description varchar
  mentor_id uuid [ref: > educators.id]
}
```

5. **classes**
```sql
Table classes {
  level enum
  code char
  id pk (level, code)
  mentor_id uuid [ref: > educators.id]
}
```

#### Academic Records

6. **subjects**
```sql
Table subjects {
    id uuid [pk]
    name varchar
    class_level char [ref: > classes.level]
    department_id uuid [ref: > departments.id, null]
    is_compulsory boolean
    tag enum
    is_active boolean
}
```

7. **educator_subjects**
```sql
Table educator_subjects {
    id uuid [pk]
    educator_id uuid [ref: > educators.id]
    subject_id uuid [ref: > subjects.id]
    classes array
    academic_year varchar
    is_active boolean
    created_at timestamp
    updated_at timestamp
}
```

8. **student_subjects**
```sql
Table student_subjects {
    id uuid [pk]
    student_id uuid [ref: > students.id]
    subject_id uuid [ref: > subjects.id]
    academic_year varchar
    is_active boolean
    created_at timestamp
}
```

9. **grades**
```sql
Table grades {
    id uuid [pk]
    student_id uuid [ref: > students.id]
    subject_id uuid [ref: > subjects.id]
    term enum
    marks decimal
    total_marks decimal
    grade_date timestamp
    graded_by uuid [ref: > educators.id]
    created_at timestamp
    updated_at timestamp
    file_url varchar
}
```

10. **student_documents**
```sql
Table student_documents {
  id uuid [pk]
  student_id uuid [ref: > students.id]
  title varchar
  academic_year varchar
  document_type varchar
  file_path varchar
  status varchar
  upload_date timestamp
  verified_at timestamp
  verified_by uuid
}
```

### Key Features & Implementation Notes

#### Phase 1: Core System
1. **Student Management**
   - Basic CRUD operations for student records
   - Class assignment and department tracking
   - Document management (report cards, certificates)

2. **Academic Structure**
   - Classes 1-3: General education, no departments
   - Classes 4-6: Department-based (Science, Business, Humanities)
   - Subject assignment based on class level and department

3. **Grade Management**
   - Term-wise grade recording
   - File attachments for physical exam papers
   - Class position calculation
   - Report generation

#### Phase 2: Advanced Features
1. **Attendance Tracking**
2. **Homework Management**
3. **Timetable System**
4. **Parent Communication Portal**

### API Endpoints Structure

#### Authentication
```
POST /auth/login
POST /auth/refresh
POST /auth/logout
```

#### Student Management
```
GET /students
POST /students
GET /students/{id}
PUT /students/{id}
DELETE /students/{id}
```

#### Academic Records
```
GET /students/{id}/grades
POST /grades
GET /students/{id}/documents
POST /documents
```

#### Class Management
```
GET /classes/{id}/positions
POST /classes/promote  // Bulk promotion endpoint
```

### Security Requirements

1. Authentication
   - JWT implementation
   - Role-based access control
   - Session management

2. Data Protection
   - Input validation
   - Request rate limiting
   - Audit logging

### Development Workflow

1. Version Control
   - Git-based workflow
   - Feature branch strategy
   - Code review process

2. Testing Strategy
   - Unit tests for models
   - Integration tests for endpoints
   - Grade calculation validation

3. Deployment
   - Development environment setup
   - Staging environment
   - Production deployment plan

### Infrastructure Requirements

1. Development Environment
   - Python 3.10+
   - PostgreSQL 14+
   - Redis
   - S3-compatible storage

2. Production Environment
   - Scalable hosting platform
   - Automated backups
   - Monitoring setup