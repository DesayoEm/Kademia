
from sqlalchemy.orm import Session
from uuid import UUID
from typing import Union, Optional
from app.core.identity.models.staff import Staff, Educator
from app.core.identity.models.student import Student
from app.core.identity.models.guardian import Guardian
from app.core.rbac.models import Permission, Role
from app.core.shared.models.enums import Resource, Action
from app.core.rbac.matrix import CONTEXTUAL_ACCESS_RULES

from app.core.assessment.models.assessment import Grade, TotalGrade
from app.core.documents.models.documents import StudentDocument, StudentAward
from app.core.progression.models.progression import Promotion, Repetition
from app.core.transfer.models.transfer import DepartmentTransfer
from app.core.curriculum.models.curriculum import StudentSubject

class PermissionService:
    def __init__(self, session: Session, current_user = None):
        self.session = session
        self.current_user = current_user

    def has_permission(self, current_role_id: UUID, resource: Resource, action: Action) -> bool:
        """Check if a role has permission to perform an action on a resource"""
        role = #get_role_from_db
        role_permissions = role.permissions

        
        if user_role.value not in PERMISSION_MATRIX:
            return False

        resource_permissions = PERMISSION_MATRIX[user_role.value].get(resource, [])
        return action in resource_permissions


    def check_educator_contextual_access(self):
        pass

    def check_permission(self, user, resource: Resource, action: Action, resource_id: UUID = None):
        user_role = user.current_role


        if not self.has_permission(user_role, resource, action):
            raise

        if user_role in CONTEXTUAL_ACCESS_RULES and resource in CONTEXTUAL_ACCESS_RULES[user_role]:
            return self.check_contextual_access(user, resource, resource_id)

        return True

    def check_contextual_access(self, user: Union[Staff, Student, Guardian], resource: Resource,resource_id: Optional[UUID]) -> bool:
        """Route to appropriate contextual access checker"""

        if user.current_role == Role.EDUCATOR:
            return self.check_educator_contextual_access(user, resource, resource_id)
        elif user.current_role == Role.STUDENT:
            return self.check_student_contextual_access(user, resource, resource_id)
        elif user.current_role == Role.GUARDIAN:
            return self.check_guardian_contextual_access(user, resource, resource_id)

        return False

    def check_educator_contextual_access(self, educator: Staff, resource: Resource,resource_id: Optional[UUID]) -> bool:
        """Check if educator can access specific resource based on their assignments"""

        if not isinstance(educator, Educator):

            educator_record = self.session.query(Educator).filter(Educator.id == educator.id).first()
            if not educator_record:
                return False
            educator = educator_record

        if resource == Resource.STUDENTS:
            return self.educator_can_access_student(educator, resource_id)
        elif resource == Resource.GRADES:
            return self.educator_can_access_grade(educator, resource_id)
        elif resource == Resource.DOCUMENTS:
            return self.educator_can_access_document(educator, resource_id)
        elif resource == Resource.AWARDS:
            return self.educator_can_access_award(educator, resource_id)
        elif resource in [Resource.TRANSFERS, Resource.PROMOTIONS, Resource.REPETITIONS]:
            return self.educator_can_access_progression(educator, resource, resource_id)

        return False

    def check_student_contextual_access(self, student: Student, resource: Resource,resource_id: Optional[UUID]) -> bool:
        """Check if student can access their own records"""
        if resource == Resource.STUDENTS:
            return resource_id == student.id

        elif resource == Resource.GRADES:
            if not resource_id:
                return False
            grade = self.session.query(Grade).filter(Grade.id == resource_id).first()
            return grade and grade.student_id == student.id

        elif resource == Resource.TOTAL_GRADES:
            if not resource_id:
                return False
            total_grade = self.session.query(TotalGrade).filter(TotalGrade.id == resource_id).first()
            return total_grade and total_grade.student_id == student.id

        elif resource == Resource.DOCUMENTS:
            if not resource_id:
                return False
            document = self.session.query(StudentDocument).filter(StudentDocument.id == resource_id).first()
            return document and document.student_id == student.id

        elif resource == Resource.AWARDS:
            if not resource_id:
                return False
            award = self.session.query(StudentAward).filter(StudentAward.id == resource_id).first()
            return award and award.student_id == student.id

        elif resource == Resource.GUARDIANS:
            return resource_id == student.guardian_id

        elif resource in [Resource.CLASSES, Resource.DEPARTMENTS, Resource.ACADEMIC_LEVELS]:
            return self._student_can_access_academic_structure(student, resource, resource_id)

        return False

    def check_guardian_contextual_access(self, guardian: Guardian, resource: Resource,resource_id: Optional[UUID]) -> bool:
        """Check if guardian can access their ward's records"""
        if resource == Resource.GUARDIANS:
            return resource_id == guardian.id


        ward_ids = [ward.id for ward in guardian.wards]

        if resource == Resource.STUDENTS:
            return resource_id in ward_ids

        elif resource == Resource.GRADES:
            if not resource_id:
                return False
            grade = self.session.query(Grade).filter(Grade.id == resource_id).first()
            return grade and grade.student_id in ward_ids

        elif resource == Resource.DOCUMENTS:
            if not resource_id:
                return False
            document = self.session.query(StudentDocument).filter(StudentDocument.id == resource_id).first()
            return document and document.student_id in ward_ids

        return False


    #Educator access helpers

    def educator_can_access_student(self, educator: Educator, student_id: Optional[UUID]) -> bool:
        """Check if educator can access specific student"""

        if not student_id:
            return False

        student = self.session.query(Student).filter(Student.id == student_id).first()
        if not student:
            return False

        if educator.supervised_class and student.class_id == educator.supervised_class.id:
            return True

        if educator.mentored_department:
            for dept in educator.mentored_department:
                if student.department_id == dept.id:
                    return True

        student_subjects = self.session.query(StudentSubject).filter(
            StudentSubject.student_id == student_id,
            StudentSubject.is_active == True
        ).all()

        educator_subject_ids = [se.academic_level_subject_id for se in educator.subject_assignments if se.is_active]

        for ss in student_subjects:
            if ss.academic_level_subject_id in educator_subject_ids:
                return True

        return False

    def _educator_can_access_grade(self, educator: Educator, grade_id: Optional[UUID]) -> bool:
        """Check if educator can access specific grade"""
        if not grade_id:
            return False

        grade = self.session.query(Grade).filter(Grade.id == grade_id).first()
        if not grade:
            return False

        # Check if the grade belongs to a student they can access
        return self.educator_can_access_student(educator, grade.student_id)

    def _educator_can_access_document(self, educator: Educator, document_id: Optional[UUID]) -> bool:
        """Check if educator can access specific document"""
        if not document_id:
            return False

        document = self.session.query(StudentDocument).filter(StudentDocument.id == document_id).first()
        if not document:
            return False

        return self.educator_can_access_student(educator, document.student_id)

    def _educator_can_access_award(self, educator: Educator, award_id: Optional[UUID]) -> bool:
        """Check if educator can access specific award"""
        if not award_id:
            return False

        award = self.session.query(StudentAward).filter(StudentAward.id == award_id).first()
        if not award:
            return False

        return self._educator_can_access_student(educator, award.student_id)

    def _educator_can_access_progression(self, educator: Educator, resource: Resource,
                                         progression_id: Optional[UUID]) -> bool:
        """Check if educator can access progression records (transfers, promotions, repetitions)"""
        if not progression_id:
            return False

        if resource == Resource.TRANSFERS:
            transfer = self.session.query(DepartmentTransfer).filter(DepartmentTransfer.id == progression_id).first()
            return transfer and self._educator_can_access_student(educator, transfer.student_id)
        elif resource == Resource.PROMOTIONS:
            promotion = self.session.query(Promotion).filter(Promotion.id == progression_id).first()
            return promotion and self._educator_can_access_student(educator, promotion.student_id)
        elif resource == Resource.REPETITIONS:
            repetition = self.session.query(Repetition).filter(Repetition.id == progression_id).first()
            return repetition and self._educator_can_access_student(educator, repetition.student_id)

        return False

    def _student_can_access_academic_structure(self, student: Student, resource: Resource,
                                               structure_id: Optional[UUID]) -> bool:
        """Check if student can access academic structure they're part of"""
        if not structure_id:
            return False

        if resource == Resource.CLASSES:
            return structure_id == student.class_id
        elif resource == Resource.DEPARTMENTS:
            return structure_id == student.department_id
        elif resource == Resource.ACADEMIC_LEVELS:
            return structure_id == student.level_id

        return False

    def get_accessible_students(self, user: Union[Staff, Student, Guardian]) -> list[UUID]:
        """Get list of student IDs the user can access"""
        if user.current_role == Role.SUPERUSER or user.current_role == Role.SUPER_EDUCATOR:
            # Can access all students
            students = self.session.query(Student.id).all()
            return [s.id for s in students]

        elif user.current_role == Role.STUDENT:
            return [user.id]

        elif user.current_role == Role.GUARDIAN:
            # Can access ward records
            return [ward.id for ward in user.wards]

        elif user.current_role == Role.EDUCATOR:
            # Get students from supervised class and mentored departments
            accessible_student_ids = set()

            educator = self.session.query(Educator).filter(Educator.id == user.id).first()
            if not educator:
                return []


            if educator.supervised_class:
                class_students = self.session.query(Student.id).filter(
                    Student.class_id == educator.supervised_class.id
                ).all()
                accessible_student_ids.update([s.id for s in class_students])


            if educator.mentored_department:
                for dept in educator.mentored_department:
                    dept_students = self.session.query(Student.id).filter(
                        Student.department_id == dept.id
                    ).all()
                    accessible_student_ids.update([s.id for s in dept_students])

            return list(accessible_student_ids)

        return []



