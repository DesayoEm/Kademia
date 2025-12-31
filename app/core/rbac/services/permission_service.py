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
    """
    Service for checking user permissions and contextual access rights.

    Implements a two-layer authorization model:
    1. Role-based permissions: Does the user's role grant the required permission?
    2. Contextual access: Can the user access this specific resource instance?

    Contextual access rules vary by user type:
    - Students: Can only access their own records.
    - Guardians: Can only access their wards' records.
    - Educators: Can access records of students in their class, department, or subjects.
    - Superusers: Can access all records.

    Attributes:
        session: SQLAlchemy database session.
        current_user: The authenticated user for contextual checks.
        role_factory: RoleFactory instance for role operations.
        role_service: RBACService instance for permission lookups.

    Example:
        service = PermissionService(session, current_user=teacher)
        service.check_permission(teacher, Resource.GRADE, Action.UPDATE, grade_id)
    """
    def __init__(self, session: Session, current_user=None):
        """
        Initialize the PermissionService.

        Args:
            session: SQLAlchemy database session for database operations.
            current_user: The authenticated user performing the action. Used for
                contextual access checks (e.g., "is this the student's own record?").
        """
        self.session = session
        self.current_user = current_user
        self.role_factory = RoleFactory(session)
        self.role_service = RBACService(session)

    def check_permission(
        self, user, resource: Resource, action: Action, resource_id: UUID | None = None
    ) -> bool:
        """
        Verify a user has permission to perform an action on a resource.

        First checks role-based permissions, then applies contextual access rules
        based on user type. Students and guardians have restricted access to only
        their own or their wards' records respectively.

        Args:
            user: The user model instance (Staff, Student, or Guardian).
            resource: The Resource enum value being accessed.
            action: The Action enum value being performed.
            resource_id: Optional UUID of the specific resource instance. Required
                for contextual access checks on students and guardians.

        Returns:
            bool: True if access is granted.

        Raises:
            AccessDenied: If the user's role lacks the required permission, or if
                contextual access checks fail.

        Note:
            Staff users (non-student, non-guardian) currently pass after role check
            without contextual verification. Educator contextual checks must be
            called separately via check_educator_contextual_access().
        """
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
        """
        Verify a student can access a specific resource instance.

        Students can only access:
        - Their own Student record (when resource_id matches their ID).
        - Records that have a student_id field matching their ID (grades, documents, etc.).

        Args:
            permission_str: The permission string for error reporting.
            resource: The Resource enum value being accessed.
            resource_id: UUID of the specific resource instance.

        Returns:
            bool: True if the student owns or is associated with the resource.

        Raises:
            AccessDenied: If the resource doesn't belong to the student.
        """
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
        """
        Verify a guardian can access a specific resource instance.

        Guardians can only access:
        - Their own Guardian record.
        - Records belonging to their wards (students linked via Guardian.wards).

        Args:
            permission_str: The permission string for error reporting.
            resource: The Resource enum value being accessed.
            resource_id: UUID of the specific resource instance.

        Returns:
            bool: True if the resource belongs to one of the guardian's wards.

        Raises:
            AccessDenied: If the resource doesn't belong to any of the guardian's wards.
        """
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
        """
        Verify an educator can access a specific resource based on their assignments.

        Educators can access resources related to students they're responsible for:
        - Students in their supervised class.
        - Students in their mentored departments.
        - Students enrolled in subjects they teach.

        Args:
            educator: The Staff or Educator model instance.
            resource: The Resource enum value being accessed.
            resource_id: UUID of the specific resource instance.

        Returns:
            bool: True if the educator has a valid relationship to the resource.
                False if the resource type isn't supported or access is denied.

        Note:
            If passed a Staff instance, will attempt to fetch the corresponding
            Educator record. Returns False if no Educator record exists.
        """

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
        """
        Check if an educator has access to a specific student.

        Access is granted if the student is:
        - In the educator's supervised class.
        - In one of the educator's mentored departments.
        - Enrolled in a subject the educator teaches.

        Args:
            educator: The Educator model instance.
            student_id: UUID of the student to check access for.

        Returns:
            bool: True if the educator can access this student, False otherwise.
        """

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
        """
        Check if an educator can access a specific grade record.

        Access is granted if the educator can access the student who owns the grade.

        Args:
            educator: The Educator model instance.
            grade_id: UUID of the grade record.

        Returns:
            bool: True if accessible, False otherwise.
        """
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
        """
        Check if an educator can access a specific student document.

        Access is granted if the educator can access the student who owns the document.

        Args:
            educator: The Educator model instance.
            document_id: UUID of the StudentDocument record.

        Returns:
            bool: True if accessible, False otherwise.

        Note:
            Prefixed with underscore—intended as internal helper.
        """
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
        """
        Check if an educator can access a specific student award.

        Access is granted if the educator can access the student who owns the award.

        Args:
            educator: The Educator model instance.
            award_id: UUID of the StudentAward record.

        Returns:
            bool: True if accessible, False otherwise.

        Note:
            Prefixed with underscore—intended as internal helper.
        """
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
        """
        Check if an educator can access progression records.

        Handles transfers, promotions, and repetitions. Access is granted if
        the educator can access the affected student.

        Args:
            educator: The Educator model instance.
            resource: The Resource enum (TRANSFER, PROMOTION, or REPETITION).
            progression_id: UUID of the progression record.

        Returns:
            bool: True if accessible, False otherwise.

        Note:
            Prefixed with underscore—intended as internal helper.
        """
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

