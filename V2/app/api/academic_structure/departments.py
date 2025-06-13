
from uuid import UUID
from fastapi.responses import FileResponse
from V2.app.core.shared.schemas.enums import ExportFormat
from V2.app.core.shared.schemas.shared_models import ArchiveRequest
from fastapi import Depends, APIRouter

from V2.app.core.academic_structure.schemas.department import(
    DepartmentCreate, DepartmentUpdate, DepartmentFilterParams, DepartmentResponse
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
        data:DepartmentCreate,
        factory: StudentDepartmentFactory = Depends(get_authenticated_factory(StudentDepartmentFactory))
    ):
    return factory.create_department(data)


@router.get("/", response_model=list[DepartmentResponse])
def get_departments(
        filters: DepartmentFilterParams = Depends(),
        factory: StudentDepartmentFactory = Depends(get_authenticated_factory(StudentDepartmentFactory))
    ):
    return factory.get_all_departments(filters)


@router.get("/{department_id}", response_model=DepartmentResponse)
def get_department(
        department_id: UUID,
        factory: StudentDepartmentFactory = Depends(get_authenticated_factory(StudentDepartmentFactory))
    ):
    return factory.get_department(department_id)


@router.put("/{department_id}", response_model=DepartmentResponse)
def update_department(
        data: DepartmentUpdate,
        department_id: UUID,
        factory: StudentDepartmentFactory = Depends(get_authenticated_factory(StudentDepartmentFactory))
    ):
    return factory.update_department(department_id, data)


@router.patch("/{department_id}",  status_code=204)
def archive_department(
        department_id: UUID, reason:ArchiveRequest,
        factory: StudentDepartmentFactory = Depends(get_authenticated_factory(StudentDepartmentFactory))
    ):
    return factory.archive_department(department_id, reason.reason)


@router.post("/{department_id}", response_class=FileResponse,  status_code=204)
def export_department(
        department_id: UUID,
        export_format: ExportFormat,
        factory: StudentDepartmentFactory = Depends(get_authenticated_factory(StudentDepartmentFactory))
    ):
    file_path= factory.export_department(department_id, export_format.value)

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
    return factory.delete_department(department_id)










