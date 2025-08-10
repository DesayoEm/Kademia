
from uuid import UUID
from typing import List

from app.core.academic_structure.factories.classes import ClassFactory
from app.core.academic_structure.factories.department import StudentDepartmentFactory
from app.core.academic_structure.schemas.classes import ClassFilterParams, ClassResponse
from app.core.academic_structure.schemas.department import DepartmentFilterParams, DepartmentResponse
from app.core.curriculum.factories.subject_educator import SubjectEducatorFactory
from app.core.curriculum.schemas.subject_educator import SubjectEducatorFilterParams, SubjectEducatorResponse
from app.core.identity.factories.staff import StaffFactory
from app.core.shared.schemas.enums import StaffType
from app.core.identity.schemas.staff import StaffResponse, StaffFilterParams
from fastapi import Depends, APIRouter
from app.core.auth.services.token_service import TokenService
from app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from app.core.auth.services.dependencies.current_user_deps import get_authenticated_factory

token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()


@router.get("/staff/educators/", response_model=List[StaffResponse])
def get_educators(
        filters: StaffFilterParams = Depends(),
        factory: StaffFactory = Depends(get_authenticated_factory(StaffFactory))
    ):
        filters.staff_type = StaffType.EDUCATOR
        return factory.get_all_staff(filters)


@router.get("/staff/educators/{educator_id}/profile/subject-assignments", response_model=List[SubjectEducatorResponse])
def get_subject_assignments(
        educator_id: UUID,
        filters: SubjectEducatorFilterParams = Depends(),
        factory: SubjectEducatorFactory = Depends(get_authenticated_factory(SubjectEducatorFactory))
    ):
        filters.educator_id = educator_id
        return factory.get_all_subject_educators(filters)



@router.get("/staff/educators/{educator_id}/profile/mentored-departments", response_model=List[DepartmentResponse])
def get_mentored_departments(
        educator_id: UUID,
        filters: DepartmentFilterParams = Depends(),
        factory: StudentDepartmentFactory = Depends(get_authenticated_factory(StudentDepartmentFactory))
    ):
        filters.mentor_id = educator_id
        return factory.get_all_student_departments(filters)


@router.get("/staff/educators/{educator_id}/profile/supervised-classes", response_model=List[ClassResponse])
def get_supervised_classes(
        educator_id: UUID,
        filters: ClassFilterParams = Depends(),
        factory: ClassFactory = Depends(get_authenticated_factory(ClassFactory))
    ):
        filters.supervisor_id = educator_id
        return factory.get_all_classes(filters)






