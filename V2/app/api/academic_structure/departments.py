
from uuid import UUID
from typing import List
from fastapi.responses import FileResponse
from V2.app.core.shared.schemas.enums import ExportFormat
from V2.app.core.shared.schemas.shared_models import ArchiveRequest
from fastapi import Depends, APIRouter

from V2.app.core.academic_structure.services import AcademicStructureService
from V2.app.core.academic_structure.schemas.department import(
    DepartmentCreate, DepartmentUpdate, DepartmentFilterParams, DepartmentResponse, DepartmentAudit
)
from V2.app.core.auth.services.token_service import TokenService
from V2.app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from V2.app.core.academic_structure.factories.department import StudentDepartmentFactory
from V2.app.core.auth.services.dependencies.current_user_deps import get_authenticated_factory, \
    get_authenticated_service


token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()


@router.post("/", response_model= DepartmentResponse, status_code=201)
def create_department(
        payload:DepartmentCreate,
        factory: StudentDepartmentFactory = Depends(get_authenticated_factory(StudentDepartmentFactory))
    ):
    return factory.create_student_department(payload)


@router.get("/", response_model=List[DepartmentResponse])
def get_departments(
        filters: DepartmentFilterParams = Depends(),
        factory: StudentDepartmentFactory = Depends(get_authenticated_factory(StudentDepartmentFactory))
    ):
    return factory.get_all_student_departments(filters)


@router.get("/{department_id}", response_model=DepartmentResponse)
def get_department(
        department_id: UUID,
        factory: StudentDepartmentFactory = Depends(get_authenticated_factory(StudentDepartmentFactory))
    ):
    return factory.get_student_department(department_id)


@router.get("/{department_id}/audit", response_model=DepartmentAudit)
def get_department_audit(
        department_id: UUID,
        factory: StudentDepartmentFactory = Depends(get_authenticated_factory(StudentDepartmentFactory))
    ):
    return factory.get_student_department(department_id)


@router.put("/{department_id}/assign-mentor", response_model=DepartmentResponse)
def assign_department_mentor(
        department_id: UUID,
        mentor_id: UUID,
        service: AcademicStructureService = Depends(get_authenticated_service(AcademicStructureService))
    ):
    """Assign a mentor to a department."""
    return service.assign_department_mentor(department_id, mentor_id)


@router.put("/{department_id}/remove-manager", response_model=DepartmentResponse)
def remove_department_mentor(
        department_id: UUID,
        service: AcademicStructureService = Depends(get_authenticated_service(AcademicStructureService))
    ):
    """Remove mentor from a department."""
    return service.assign_department_mentor(department_id)


@router.put("/{department_id}/assign-student-rep", response_model=DepartmentResponse)
def assign_student_rep(
        department_id: UUID,
        student_rep_id: UUID,
        service: AcademicStructureService = Depends(get_authenticated_service(AcademicStructureService))
    ):
    """Assign a student representative to a department."""
    return service.assign_department_student_rep(department_id, student_rep_id)


@router.put("/{department_id}/remove-student-rep", response_model=DepartmentResponse)
def remove_student_rep(
        department_id: UUID,
        service: AcademicStructureService = Depends(get_authenticated_service(AcademicStructureService))
    ):
    """Remove student representative from a department."""
    return service.assign_department_student_rep(department_id)


@router.put("/{department_id}/assign-assist-rep", response_model=DepartmentResponse)
def assign_assist_rep(
        department_id: UUID,
        asst_student_rep_id: UUID,
        service: AcademicStructureService = Depends(get_authenticated_service(AcademicStructureService))
    ):
    """Assign an assistant student rep to a department."""
    return service.assign_department_assistant_rep(department_id, asst_student_rep_id)


@router.put("/{department_id}/remove-assist-rep", response_model=DepartmentResponse)
def remove_assist_rep(
        department_id: UUID,
        service: AcademicStructureService = Depends(get_authenticated_service(AcademicStructureService))
    ):
    """Remove student representative from a department."""
    return service.assign_department_assistant_rep(department_id)


@router.put("/{department_id}", response_model=DepartmentResponse)
def update_department(
        payload: DepartmentUpdate,
        department_id: UUID,
        factory: StudentDepartmentFactory = Depends(get_authenticated_factory(StudentDepartmentFactory))
    ):
    update_data = payload.model_dump(exclude_unset=True)
    return factory.update_student_department(department_id, update_data)


@router.patch("/{department_id}",  status_code=204)
def archive_department(
        department_id: UUID, reason:ArchiveRequest,
        factory: StudentDepartmentFactory = Depends(get_authenticated_factory(StudentDepartmentFactory))
    ):
    return factory.archive_student_department(department_id, reason.reason)


@router.post("/{department_id}", response_class=FileResponse,  status_code=204)
def export_department(
        department_id: UUID,
        export_format: ExportFormat,
        service: AcademicStructureService = Depends(get_authenticated_service(AcademicStructureService))
    ):
    file_path= service.export_department(department_id, export_format.value)

    return FileResponse(
        path=file_path,
        filename=file_path.split("/")[-1],
        media_type="application/octet-stream"
    )

@router.delete("/{department_id}", status_code=204)
def delete_department(
        department_id: UUID,
        factory: StudentDepartmentFactory = Depends(get_authenticated_factory(StudentDepartmentFactory))
    ):
    return factory.delete_student_department(department_id)










