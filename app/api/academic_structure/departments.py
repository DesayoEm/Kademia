from uuid import UUID
from typing import List
from fastapi.responses import FileResponse

from app.core.identity.schemas.student import StudentFilterParams, StudentResponse
from app.core.shared.schemas.enums import ExportFormat
from app.core.shared.schemas.shared_models import ArchiveRequest
from fastapi import Depends, APIRouter

from app.core.academic_structure.services.academic_structure import (
    AcademicStructureService,
)
from app.core.academic_structure.schemas.department import (
    DepartmentCreate,
    DepartmentUpdate,
    DepartmentFilterParams,
    DepartmentResponse,
    DepartmentAudit,
)
from app.core.auth.services.token_service import TokenService
from app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from app.core.academic_structure.factories.department import StudentDepartmentFactory
from app.core.identity.factories.student import StudentFactory
from app.core.auth.services.dependencies.current_user_deps import (
    get_authenticated_factory,
    get_authenticated_service,
)


token_service = TokenService()
access = AccessTokenBearer()
router = APIRouter()


# Archive routers
@router.get("/archive/departments/", response_model=List[DepartmentResponse])
def get_archived_departments(
    filters: DepartmentFilterParams = Depends(),
    factory: StudentDepartmentFactory = Depends(
        get_authenticated_factory(StudentDepartmentFactory)
    ),
):
    return factory.get_all_archived_departments(filters)


@router.get(
    "/archive/departments/{department_id}/audit", response_model=DepartmentAudit
)
def get_archived_department_audit(
    department_id: UUID,
    factory: StudentDepartmentFactory = Depends(
        get_authenticated_factory(StudentDepartmentFactory)
    ),
):
    return factory.get_archived_department(department_id)


@router.get("/archive/departments/{department_id}", response_model=DepartmentResponse)
def get_archived_department(
    department_id: UUID,
    factory: StudentDepartmentFactory = Depends(
        get_authenticated_factory(StudentDepartmentFactory)
    ),
):
    return factory.get_archived_department(department_id)


@router.patch("/archive/departments/{department_id}", response_model=DepartmentResponse)
def restore_department(
    department_id: UUID,
    factory: StudentDepartmentFactory = Depends(
        get_authenticated_factory(StudentDepartmentFactory)
    ),
):
    return factory.restore_department(department_id)


@router.delete("/archive/departments/{department_id}", status_code=204)
def delete_archived_department(
    department_id: UUID,
    factory: StudentDepartmentFactory = Depends(
        get_authenticated_factory(StudentDepartmentFactory)
    ),
):
    return factory.delete_archived_department(department_id)


# Active routers
@router.post("/departments/", response_model=DepartmentResponse, status_code=201)
def create_department(
    payload: DepartmentCreate,
    factory: StudentDepartmentFactory = Depends(
        get_authenticated_factory(StudentDepartmentFactory)
    ),
):
    return factory.create_student_department(payload)


@router.get("/departments/", response_model=List[DepartmentResponse])
def get_departments(
    filters: DepartmentFilterParams = Depends(),
    factory: StudentDepartmentFactory = Depends(
        get_authenticated_factory(StudentDepartmentFactory)
    ),
):
    return factory.get_all_student_departments(filters)


@router.get("/departments/{department_id}", response_model=DepartmentResponse)
def get_department(
    department_id: UUID,
    factory: StudentDepartmentFactory = Depends(
        get_authenticated_factory(StudentDepartmentFactory)
    ),
):
    return factory.get_student_department(department_id)


@router.get(
    "/departments/{department_id}/students", response_model=List[StudentResponse]
)
def get_level_students(
    department_id: UUID,
    filters: StudentFilterParams = Depends(),
    factory: StudentFactory = Depends(get_authenticated_factory(StudentFactory)),
):
    filters.department_id = department_id
    return factory.get_all_students(filters)


@router.get("/departments/{department_id}/audit", response_model=DepartmentAudit)
def get_department_audit(
    department_id: UUID,
    factory: StudentDepartmentFactory = Depends(
        get_authenticated_factory(StudentDepartmentFactory)
    ),
):
    return factory.get_student_department(department_id)


@router.put(
    "/departments/{department_id}/assign-mentor", response_model=DepartmentResponse
)
def assign_department_mentor(
    department_id: UUID,
    mentor_id: UUID,
    service: AcademicStructureService = Depends(
        get_authenticated_service(AcademicStructureService)
    ),
):
    return service.assign_department_mentor(department_id, mentor_id)


@router.put(
    "/departments/{department_id}/remove-manager", response_model=DepartmentResponse
)
def remove_department_mentor(
    department_id: UUID,
    service: AcademicStructureService = Depends(
        get_authenticated_service(AcademicStructureService)
    ),
):
    return service.assign_department_mentor(department_id)


@router.put(
    "/departments/{department_id}/assign-student-rep", response_model=DepartmentResponse
)
def assign_student_rep(
    department_id: UUID,
    student_rep_id: UUID,
    service: AcademicStructureService = Depends(
        get_authenticated_service(AcademicStructureService)
    ),
):
    return service.assign_department_student_rep(department_id, student_rep_id)


@router.put(
    "/departments/{department_id}/remove-student-rep", response_model=DepartmentResponse
)
def remove_student_rep(
    department_id: UUID,
    service: AcademicStructureService = Depends(
        get_authenticated_service(AcademicStructureService)
    ),
):
    return service.assign_department_student_rep(department_id)


@router.put("/{department_id}/assign-assist-rep", response_model=DepartmentResponse)
def assign_assist_rep(
    department_id: UUID,
    asst_student_rep_id: UUID,
    service: AcademicStructureService = Depends(
        get_authenticated_service(AcademicStructureService)
    ),
):
    return service.assign_department_assistant_rep(department_id, asst_student_rep_id)


@router.put(
    "/departments/{department_id}/remove-assist-rep", response_model=DepartmentResponse
)
def remove_assist_rep(
    department_id: UUID,
    service: AcademicStructureService = Depends(
        get_authenticated_service(AcademicStructureService)
    ),
):
    return service.assign_department_assistant_rep(department_id)


@router.put("/departments/{department_id}", response_model=DepartmentResponse)
def update_department(
    payload: DepartmentUpdate,
    department_id: UUID,
    factory: StudentDepartmentFactory = Depends(
        get_authenticated_factory(StudentDepartmentFactory)
    ),
):
    update_data = payload.model_dump(exclude_unset=True)
    return factory.update_student_department(department_id, update_data)


@router.patch("/departments/{department_id}", status_code=204)
def archive_department(
    department_id: UUID,
    reason: ArchiveRequest,
    factory: StudentDepartmentFactory = Depends(
        get_authenticated_factory(StudentDepartmentFactory)
    ),
):
    return factory.archive_student_department(department_id, reason.reason)


@router.post(
    "/departments/{department_id}/audit", response_class=FileResponse, status_code=204
)
def export_department_audit(
    department_id: UUID,
    export_format: ExportFormat,
    service: AcademicStructureService = Depends(
        get_authenticated_service(AcademicStructureService)
    ),
):
    file_path = service.export_department(department_id, export_format.value)

    return FileResponse(
        path=file_path,
        filename=file_path.split("/")[-1],
        media_type="application/octet-stream",
    )


@router.delete("/departments/{department_id}", status_code=204)
def delete_department(
    department_id: UUID,
    factory: StudentDepartmentFactory = Depends(
        get_authenticated_factory(StudentDepartmentFactory)
    ),
):
    return factory.delete_student_department(department_id)
