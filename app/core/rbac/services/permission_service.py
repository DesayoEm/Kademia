from sqlalchemy.orm import Session
from sqlalchemy import select
from uuid import UUID
from typing import Union, Optional
from app.core.identity.models.staff import Staff, Educator
from app.core.identity.models.student import Student
from app.core.identity.models.guardian import Guardian
from app.core.rbac.factories.role import RoleFactory
from app.core.rbac.models import Role
from app.core.rbac.services.contextual_permission_config import RESOURCE_TO_MODEL
from app.core.rbac.services.role_service import RBACService
from app.core.shared.exceptions.rbac_errors import AccessDenied
from app.core.shared.models.enums import Resource, Action, UserType

from app.core.assessment.models.assessment import Grade
from app.core.documents.models.documents import StudentDocument, StudentAward
from app.core.progression.models.progression import Promotion, Repetition
from app.core.transfer.models.transfer import DepartmentTransfer
from app.core.curriculum.models.curriculum import StudentSubject
from app.core.shared.log_service.logger import logger


class PermissionService:
    def __init__(self, session: Session, current_user=None):
        self.session = session
        self.current_user = current_user
        self.role_factory = RoleFactory(session)
        self.role_service = RBACService(session)

    def check_permission(
        self, user, resource: Resource, action: Action, resource_id: UUID | None = None
    ) -> bool:
        role_id = user.current_role_id
        user_id = user.id

        permission_strs = self.role_service.get_role_permission_strs(role_id)
        permission_str = f"{resource.value}+{action.value}"

        if not permission_str in permission_strs:
            raise AccessDenied(user_id, resource_id, permission_str)

        if user.user_type == UserType.STUDENT:
            return self.check_student_contextual_access(
                permission_str, resource, resource_id
            )

        if user.user_type == UserType.GUARDIAN:
            return self.check_guardian_contextual_access(
                permission_str, resource, resource_id
            )

    def check_student_contextual_access(
        self, permission_str: str, resource: Resource, resource_id: Optional[UUID]
    ) -> bool:
        """Check if student can access own records"""
        active_student_id = self.current_user.id

        if resource == Resource.STUDENT:
            return resource_id == active_student_id

        model_class = RESOURCE_TO_MODEL.get(resource)

        if not model_class:
            logger.error(f"No model found for {resource}")
            return False

        stmt = select(model_class).where(model_class.id == resource_id)
        obj = self.session.execute(stmt).scalar()

        if obj and hasattr(obj, "student_id") and obj.student_id == active_student_id:
            return True

        else:
            raise AccessDenied(active_student_id, resource_id, permission_str)

    def check_guardian_contextual_access(
        self, permission_str, resource: Resource, resource_id: Optional[UUID]
    ) -> bool:
        """Check if guardian can access their ward's records"""
        active_guardian_id = self.current_user.id

        if resource == Resource.GUARDIAN:
            return resource_id == active_guardian_id

        model_class = RESOURCE_TO_MODEL.get(resource)

        if not model_class:
            logger.error(f"No model class found for {resource}")
            return False
        stmt = (
            select(model_class)
            .join(Guardian.wards)
            .where(
                Guardian.id == active_guardian_id,
                model_class.id == resource_id,
                model_class.student_id == Student.id,
            )
        )

        obj = self.session.execute(stmt).scalar_one_or_none()
        if obj:
            return True

        raise AccessDenied(active_guardian_id, resource_id, permission_str)

    def check_educator_contextual_access(
        self, educator: Staff, resource: Resource, resource_id: Optional[UUID]
    ) -> bool:
        """Check if educator can access specific resource based on their assignments"""

        if not isinstance(educator, Educator):

            educator_record = (
                self.session.query(Educator).filter(Educator.id == educator.id).first()
            )
            if not educator_record:
                return False
            educator = educator_record

        if resource == Resource.STUDENT:
            return self.educator_can_access_student(educator, resource_id)
        elif resource == Resource.GRADE:
            return self.educator_can_access_grade(educator, resource_id)
        elif resource == Resource.DOCUMENT:
            return self.educator_can_access_document(educator, resource_id)
        elif resource == Resource.AWARD:
            return self.educator_can_access_award(educator, resource_id)
        elif resource in [Resource.TRANSFER, Resource.PROMOTION, Resource.REPETITION]:
            return self.educator_can_access_progression(educator, resource, resource_id)

        return False

    # Educator access helpers
    def educator_can_access_student(
        self, educator: Educator, student_id: Optional[UUID]
    ) -> bool:
        """Check if educator can access specific student"""

        if not student_id:
            return False

        student = self.session.query(Student).filter(Student.id == student_id).first()
        if not student:
            return False

        if (
            educator.supervised_class
            and student.class_id == educator.supervised_class.id
        ):
            return True

        if educator.mentored_department:
            for dept in educator.mentored_department:
                if student.department_id == dept.id:
                    return True

        student_subjects = (
            self.session.query(StudentSubject)
            .filter(
                StudentSubject.student_id == student_id,
                StudentSubject.is_active == True,
            )
            .all()
        )

        educator_subject_ids = [
            se.academic_level_subject_id
            for se in educator.subject_assignments
            if se.is_active
        ]

        for ss in student_subjects:
            if ss.academic_level_subject_id in educator_subject_ids:
                return True

        return False

    def educator_can_access_grade(
        self, educator: Educator, grade_id: Optional[UUID]
    ) -> bool:
        """Check if educator can access specific grade"""
        if not grade_id:
            return False

        grade = self.session.query(Grade).filter(Grade.id == grade_id).first()
        if not grade:
            return False

        # Check if the grade belongs to a student they can access
        return self.educator_can_access_student(educator, grade.student_id)

    def _educator_can_access_document(
        self, educator: Educator, document_id: Optional[UUID]
    ) -> bool:
        """Check if educator can access specific document"""
        if not document_id:
            return False

        document = (
            self.session.query(StudentDocument)
            .filter(StudentDocument.id == document_id)
            .first()
        )
        if not document:
            return False

        return self.educator_can_access_student(educator, document.student_id)

    def _educator_can_access_award(
        self, educator: Educator, award_id: Optional[UUID]
    ) -> bool:
        """Check if educator can access specific award"""
        if not award_id:
            return False

        award = (
            self.session.query(StudentAward).filter(StudentAward.id == award_id).first()
        )
        if not award:
            return False

        return self.educator_can_access_student(educator, award.student_id)

    def _educator_can_access_progression(
        self, educator: Educator, resource: Resource, progression_id: Optional[UUID]
    ) -> bool:
        """Check if educator can access progression records (transfers, promotions, repetitions)"""
        if not progression_id:
            return False

        if resource == Resource.TRANSFER:
            transfer = (
                self.session.query(DepartmentTransfer)
                .filter(DepartmentTransfer.id == progression_id)
                .first()
            )
            return transfer and self.educator_can_access_student(
                educator, transfer.student_id
            )
        elif resource == Resource.PROMOTION:
            promotion = (
                self.session.query(Promotion)
                .filter(Promotion.id == progression_id)
                .first()
            )
            return promotion and self.educator_can_access_student(
                educator, promotion.student_id
            )
        elif resource == Resource.REPETITION:
            repetition = (
                self.session.query(Repetition)
                .filter(Repetition.id == progression_id)
                .first()
            )
            return repetition and self.educator_can_access_student(
                educator, repetition.student_id
            )

        return False

    def get_accessible_students(
        self, user: Union[Staff, Student, Guardian]
    ) -> list[UUID]:
        """Get list of student IDs the user can access"""
        if (
            user.current_role == Role.SUPERUSER
            or user.current_role == Role.SUPER_EDUCATOR
        ):
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

            educator = (
                self.session.query(Educator).filter(Educator.id == user.id).first()
            )
            if not educator:
                return []

            if educator.supervised_class:
                class_students = (
                    self.session.query(Student.id)
                    .filter(Student.class_id == educator.supervised_class.id)
                    .all()
                )
                accessible_student_ids.update([s.id for s in class_students])

            if educator.mentored_department:
                for dept in educator.mentored_department:
                    dept_students = (
                        self.session.query(Student.id)
                        .filter(Student.department_id == dept.id)
                        .all()
                    )
                    accessible_student_ids.update([s.id for s in dept_students])

            return list(accessible_student_ids)

        return []
