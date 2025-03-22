# Kademia API Endpoints Checklist

## Authentication

- [ ] POST /auth/login - Authenticate user and get tokens
- [ ] POST /auth/refresh - Refresh access token
- [ ] POST /auth/logout - Invalidate tokens
- [ ] GET /auth/me - Get current user profile
- [ ] PUT /auth/change-password - Change user password

## Users - General
- [x] GET /users/{id} - Get user by ID
- [x] GET /users - List users with filtering

## Students

- [x] POST /students - Create new student
- [x] GET /students - List students with filtering
- [x] GET /students/{id} - Get student by ID 
- [x] PUT /students/{id} - Update student
- [x] DELETE /students/{id} - Archive student
- [x] GET /students/archived - List archived students
- [x] GET /students/archived/{id} - Get archived student
- [x] POST /students/archived/{id}/restore - Restore archived student
- [x] DELETE /students/archived/{id} - Permanently delete archived student
- [ ] GET /students/{id}/grades - Get student grades
- [ ] GET /students/{id}/total-grades - Get student total grades
- [ ] GET /students/{id}/subjects - Get student subjects
- [ ] GET /students/{id}/documents - Get student documents
- [ ] GET /students/{id}/awards - Get student awards
- [ ] GET /students/class/{class_id} - Get students by class
- [ ] GET /students/department/{department_id} - Get students by department
- [ ] GET /students/level/{level_id} - Get students by academic level

## Guardians

- [x] POST /guardians - Create new guardian
- [x] GET /guardians - List guardians with filtering
- [x] GET /guardians/{id} - Get guardian by ID
- [x] PUT /guardians/{id} - Update guardian
- [x] DELETE /guardians/{id} - Archive guardian
- [x] GET /guardians/archived - List archived guardians
- [x] GET /guardians/archived/{id} - Get archived guardian
- [x] POST /guardians/archived/{id}/restore - Restore archived guardian
- [x] DELETE /guardians/archived/{id} - Permanently delete archived guardian
- [ ] GET /guardians/{id}/wards - Get guardian's wards

## Staff (General)

- [x] POST /staff - Create new staff member
- [x] GET /staff - List staff with filtering
- [x] GET /staff/{id} - Get staff by ID
- [x] PUT /staff/{id} - Update staff
- [x] DELETE /staff/{id} - Archive staff
- [x] GET /staff/archived - List archived staff
- [x] GET /staff/archived/{id} - Get archived staff
- [x] POST /staff/archived/{id}/restore - Restore archived staff
- [x] DELETE /staff/archived/{id} - Permanently delete archived staff
- [ ] PUT /staff/{id}/access-level - Update staff access level
- [ ] GET /staff/department/{department_id} - Get staff by department
- [ ] GET /staff/role/{role_id} - Get staff by role

## Educators

- [ ] GET /educators/{id}/qualifications - Get educator qualifications
- [ ] POST /educators/{id}/qualifications - Add educator qualification
- [ ] GET /educators/{id}/subjects - Get educator's subject assignments
- [ ] GET /educators/{id}/mentored-department - Get educator's mentored department
- [ ] GET /educators/{id}/supervised-class - Get educator's supervised class

## Staff Departments

- [x] POST /staff-departments - Create new staff department
- [x] GET /staff-departments - List staff departments
- [x] GET /staff-departments/{id} - Get staff department by ID
- [x] PUT /staff-departments/{id} - Update staff department
- [x] DELETE /staff-departments/{id} - Archive staff department
- [x] GET /staff-departments/archived - List archived staff departments
- [x] POST /staff-departments/archived/{id}/restore - Restore archived staff department
- [x] DELETE /staff-departments/archived/{id} - Permanently delete archived staff department
- [ ] GET /staff-departments/{id}/staff - Get staff in department

## Staff Roles

- [x] POST /staff-roles - Create new staff role
- [x] GET /staff-roles - List staff roles
- [x] GET /staff-roles/{id} - Get staff role by ID
- [x] PUT /staff-roles/{id} - Update staff role
- [x] DELETE /staff-roles/{id} - Archive staff role
- [x] GET /staff-roles/archived - List archived staff roles
- [x] POST /staff-roles/archived/{id}/restore - Restore archived staff role
- [x] DELETE /staff-roles/archived/{id} - Permanently delete archived staff role
- [ ] GET /staff-roles/{id}/staff - Get staff with role

## Academic Levels

- [x] POST /academic-levels - Create new academic level
- [x] GET /academic-levels - List academic levels
- [x] GET /academic-levels/{id} - Get academic level by ID
- [x] PUT /academic-levels/{id} - Update academic level
- [x] DELETE /academic-levels/{id} - Archive academic level
- [x] GET /academic-levels/archived - List archived academic levels
- [x] POST /academic-levels/archived/{id}/restore - Restore archived academic level
- [x] DELETE /academic-levels/archived/{id} - Permanently delete archived academic level
- [ ] GET /academic-levels/{id}/students - Get students in academic level
- [ ] GET /academic-levels/{id}/classes - Get classes in academic level
- [ ] GET /academic-levels/{id}/subjects - Get subjects for academic level

## Classes

- [x] POST /classes - Create new class
- [x] GET /classes - List classes
- [x] GET /classes/{id} - Get class by ID
- [x] PUT /classes/{id} - Update class
- [x] DELETE /classes/{id} - Archive class
- [x] GET /classes/archived - List archived classes
- [x] POST /classes/archived/{id}/restore - Restore archived class
- [x] DELETE /classes/archived/{id} - Permanently delete archived class
- [ ] GET /classes/{id}/students - Get students in class
- [ ] PUT /classes/{id}/supervisor - Assign class supervisor
- [ ] PUT /classes/{id}/student-rep - Assign class student representative
- [ ] PUT /classes/{id}/assistant-rep - Assign class assistant representative

## Student Departments

- [x] POST /student-departments - Create new student department
- [x] GET /student-departments - List student departments
- [x] GET /student-departments/{id} - Get student department by ID
- [x] PUT /student-departments/{id} - Update student department
- [x] DELETE /student-departments/{id} - Archive student department
- [x] GET /student-departments/archived - List archived student departments
- [x] POST /student-departments/archived/{id}/restore - Restore archived student department
- [x] DELETE /student-departments/archived/{id} - Permanently delete archived student department
- [ ] GET /student-departments/{id}/students - Get students in department
- [ ] PUT /student-departments/{id}/mentor - Assign department mentor
- [ ] PUT /student-departments/{id}/student-rep - Assign department student representative
- [ ] PUT /student-departments/{id}/assistant-rep - Assign department assistant representative

## Subjects

- [ ] POST /subjects - Create new subject
- [ ] GET /subjects - List subjects
- [ ] GET /subjects/{id} - Get subject by ID
- [ ] PUT /subjects/{id} - Update subject
- [ ] DELETE /subjects/{id} - Archive subject
- [ ] GET /subjects/archived - List archived subjects
- [ ] POST /subjects/archived/{id}/restore - Restore archived subject
- [ ] DELETE /subjects/archived/{id} - Permanently delete archived subject
- [ ] GET /subjects/{id}/students - Get students taking subject
- [ ] GET /subjects/{id}/educators - Get educators teaching subject
- [ ] GET /subjects/department/{department_id} - Get subjects by department
- [ ] GET /subjects/level/{level_id} - Get subjects by academic level

## Academic Level Subjects

- [ ] POST /academic-level-subjects - Create new academic level subject
- [ ] GET /academic-level-subjects - List academic level subjects
- [ ] GET /academic-level-subjects/{id} - Get academic level subject by ID
- [ ] PUT /academic-level-subjects/{id} - Update academic level subject
- [ ] DELETE /academic-level-subjects/{id} - Archive academic level subject
- [ ] GET /academic-level-subjects/level/{level_id} - Get subjects for academic level
- [ ] GET /academic-level-subjects/subject/{subject_id} - Get academic levels for subject

## Student Subjects

- [ ] POST /student-subjects - Enroll student in subject
- [ ] GET /student-subjects - List student subject enrollments
- [ ] GET /student-subjects/{id} - Get student subject enrollment by ID
- [ ] PUT /student-subjects/{id} - Update student subject enrollment
- [ ] DELETE /student-subjects/{id} - Archive student subject enrollment
- [ ] GET /student-subjects/student/{student_id} - Get subject enrollments for student
- [ ] GET /student-subjects/subject/{subject_id} - Get students enrolled in subject
- [ ] GET /student-subjects/academic-year/{year} - Get enrollments by academic year
- [ ] GET /student-subjects/term/{term} - Get enrollments by term

## Subject Educators

- [ ] POST /subject-educators - Assign educator to subject
- [ ] GET /subject-educators - List subject educator assignments
- [ ] GET /subject-educators/{id} - Get subject educator assignment by ID
- [ ] PUT /subject-educators/{id} - Update subject educator assignment
- [ ] DELETE /subject-educators/{id} - Archive subject educator assignment
- [ ] GET /subject-educators/educator/{educator_id} - Get subject assignments for educator
- [ ] GET /subject-educators/subject/{subject_id} - Get educators assigned to subject
- [ ] GET /subject-educators/academic-year/{year} - Get assignments by academic year
- [ ] GET /subject-educators/term/{term} - Get assignments by term

## Grades

- [ ] POST /grades - Create new grade
- [ ] GET /grades - List grades with filtering
- [ ] GET /grades/{id} - Get grade by ID
- [ ] PUT /grades/{id} - Update grade
- [ ] DELETE /grades/{id} - Archive grade
- [ ] GET /grades/archived - List archived grades
- [ ] POST /grades/archived/{id}/restore - Restore archived grade
- [ ] DELETE /grades/archived/{id} - Permanently delete archived grade
- [ ] GET /grades/student/{student_id} - Get grades for student
- [ ] GET /grades/subject/{subject_id} - Get grades for subject
- [ ] GET /grades/academic-year/{year} - Get grades by academic year
- [ ] GET /grades/term/{term} - Get grades by term
- [ ] GET /grades/type/{grade_type} - Get grades by type

## Total Grades

- [ ] POST /total-grades - Create new total grade
- [ ] GET /total-grades - List total grades with filtering
- [ ] GET /total-grades/{id} - Get total grade by ID
- [ ] PUT /total-grades/{id} - Update total grade
- [ ] DELETE /total-grades/{id} - Archive total grade
- [ ] GET /total-grades/student/{student_id} - Get total grades for student
- [ ] GET /total-grades/subject/{subject_id} - Get total grades for subject
- [ ] GET /total-grades/academic-year/{year} - Get total grades by academic year
- [ ] GET /total-grades/term/{term} - Get total grades by term

## Repetitions

- [ ] POST /repetitions - Create new repetition request
- [ ] GET /repetitions - List repetition requests
- [ ] GET /repetitions/{id} - Get repetition request by ID
- [ ] PUT /repetitions/{id} - Update repetition request
- [ ] PUT /repetitions/{id}/status - Update repetition request status
- [ ] GET /repetitions/student/{student_id} - Get repetition requests for student
- [ ] GET /repetitions/status/{status} - Get repetition requests by status
- [ ] GET /repetitions/academic-year/{year} - Get repetition requests by academic year

## Class Transfers

- [ ] POST /class-transfers - Create new class transfer request
- [ ] GET /class-transfers - List class transfer requests
- [ ] GET /class-transfers/{id} - Get class transfer request by ID
- [ ] PUT /class-transfers/{id} - Update class transfer request
- [ ] PUT /class-transfers/{id}/status - Update class transfer request status
- [ ] GET /class-transfers/student/{student_id} - Get class transfer requests for student
- [ ] GET /class-transfers/status/{status} - Get class transfer requests by status
- [ ] GET /class-transfers/academic-year/{year} - Get class transfer requests by academic year

## Department Transfers

- [ ] POST /department-transfers - Create new department transfer request
- [ ] GET /department-transfers - List department transfer requests
- [ ] GET /department-transfers/{id} - Get department transfer request by ID
- [ ] PUT /department-transfers/{id} - Update department transfer request
- [ ] PUT /department-transfers/{id}/status - Update department transfer request status
- [ ] GET /department-transfers/student/{student_id} - Get department transfer requests for student
- [ ] GET /department-transfers/status/{status} - Get department transfer requests by status
- [ ] GET /department-transfers/academic-year/{year} - Get department transfer requests by academic year

## Student Documents

- [ ] POST /student-documents - Upload new student document
- [ ] GET /student-documents - List student documents
- [ ] GET /student-documents/{id} - Get student document by ID
- [ ] PUT /student-documents/{id} - Update student document
- [ ] DELETE /student-documents/{id} - Archive student document
- [ ] GET /student-documents/archived - List archived student documents
- [ ] POST /student-documents/archived/{id}/restore - Restore archived student document
- [ ] DELETE /student-documents/archived/{id} - Permanently delete archived student document
- [ ] GET /student-documents/student/{student_id} - Get documents for student
- [ ] GET /student-documents/type/{document_type} - Get documents by type
- [ ] GET /student-documents/academic-year/{year} - Get documents by academic year

## Student Awards

- [ ] POST /student-awards - Create new student award
- [ ] GET /student-awards - List student awards
- [ ] GET /student-awards/{id} - Get student award by ID
- [ ] PUT /student-awards/{id} - Update student award
- [ ] DELETE /student-awards/{id} - Archive student award
- [ ] GET /student-awards/archived - List archived student awards
- [ ] POST /student-awards/archived/{id}/restore - Restore archived student award
- [ ] DELETE /student-awards/archived/{id} - Permanently delete archived student award
- [ ] GET /student-awards/student/{student_id} - Get awards for student
- [ ] GET /student-awards/academic-year/{year} - Get awards by academic year

## Access Level Changes

- [ ] GET /access-level-changes - List access level changes with filtering
- [ ] GET /access-level-changes/{id} - Get access level change by ID
- [ ] GET /access-level-changes/staff/{staff_id} - Get access level changes for staff member

## Educator Qualifications

- [x] POST /educator-qualifications - Create new educator qualification
- [x] GET /educator-qualifications - List educator qualifications
- [x] GET /educator-qualifications/{id} - Get educator qualification by ID
- [x] PUT /educator-qualifications/{id} - Update educator qualification
- [x] DELETE /educator-qualifications/{id} - Archive educator qualification
- [ ] GET /educator-qualifications/educator/{educator_id} - Get qualifications for educator
