
from uuid import UUID
from typing import List
from fastapi.responses import FileResponse
from V2.app.core.shared.schemas.enums import ExportFormat
from V2.app.core.shared.schemas.shared_models import ArchiveRequest
from fastapi import Depends, APIRouter

from V2.app.core.academic_structure.schemas.classes import (
    ClassCreate, ClassUpdate, ClassFilterParams, ClassResponse, ClassAudit
)
from V2.app.core.academic_structure.services.academic_structure import AcademicStructureService
from V2.app.core.auth.services.token_service import TokenService
from V2.app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from V2.app.core.academic_structure.factories.classes import ClassFactory
from V2.app.core.auth.services.dependencies.current_user_deps import get_authenticated_factory, \
    get_authenticated_service

token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()


@router.post("/", response_model= ClassResponse, status_code=201)
def create_class(
        data:ClassCreate,
        factory: ClassFactory = Depends(get_authenticated_factory(ClassFactory))
    ):
    return factory.create_class(data)


@router.get("/", response_model=List[ClassResponse])
def get_classes(
        filters: ClassFilterParams = Depends(),
        factory: ClassFactory = Depends(get_authenticated_factory(ClassFactory))
    ):
    return factory.get_all_classes(filters)

@router.get("/{class_id}/audit", response_model=ClassAudit)
def get_class_audit(
        class_id: UUID,
        factory: ClassFactory = Depends(get_authenticated_factory(ClassFactory))
):
    return factory.get_class(class_id)


@router.get("/{class_id}", response_model=ClassResponse)
def get_class(
        class_id: UUID,
        factory: ClassFactory = Depends(get_authenticated_factory(ClassFactory))
):
    return factory.get_class(class_id)


@router.put("/{class_id}/assign-supervisor", response_model=ClassResponse)
def assign_class_supervisor(
        class_id: UUID,
        supervisor_id: UUID,
        service: AcademicStructureService = Depends(get_authenticated_service(AcademicStructureService))
    ):
    """Assign a supervisor to a class."""
    return service.assign_class_supervisor(class_id, supervisor_id)


@router.put("/{department_id}/remove-manager", response_model=ClassResponse)
def remove_class_supervisor(
        class_id: UUID,
        service: AcademicStructureService = Depends(get_authenticated_service(AcademicStructureService))
    ):
    """Remove supervisor from a class."""
    return service.assign_class_supervisor(class_id)


@router.put("/{class_id}/assign-student-rep", response_model=ClassResponse)
def assign_student_rep(
        class_id: UUID,
        student_rep_id: UUID,
        service: AcademicStructureService = Depends(get_authenticated_service(AcademicStructureService))
    ):
    """Assign a student representative to a class."""
    return service.assign_class_student_rep(class_id, student_rep_id)


@router.put("/{department_id}/remove-student-rep", response_model=ClassResponse)
def remove_student_rep(
        class_id: UUID,
        service: AcademicStructureService = Depends(get_authenticated_service(AcademicStructureService))
    ):
    """Remove student representative from a class."""
    return service.assign_class_student_rep(class_id)


@router.put("/{class_id}/assign-assist-rep", response_model=ClassResponse)
def assign_assist_rep(
        class_id: UUID,
        asst_student_rep_id: UUID,
        service: AcademicStructureService = Depends(get_authenticated_service(AcademicStructureService))
    ):
    """Assign an assistant student rep to a class."""
    return service.assign_class_assistant_rep(class_id, asst_student_rep_id)


@router.put("/{department_id}/remove-assist-rep", response_model=ClassResponse)
def remove_assist_rep(
        class_id: UUID,
        service: AcademicStructureService = Depends(get_authenticated_service(AcademicStructureService))
    ):
    """Remove student representative from a class."""
    return service.assign_class_assistant_rep(class_id)


@router.put("/{class_id}", response_model=ClassResponse)
def update_class(
        payload: ClassUpdate,
        class_id: UUID,
        factory: ClassFactory = Depends(get_authenticated_factory(ClassFactory))
):
    update_data = payload.model_dunp(exclude_unset = True)
    return factory.update_class(class_id, update_data)


@router.patch("/{class_id}",  status_code=204)
def archive_class(
        class_id: UUID,
        reason:ArchiveRequest,
        factory: ClassFactory = Depends(get_authenticated_factory(ClassFactory))
    ):
    return factory.archive_class(class_id, reason.reason)


@router.post("/{class_id}", response_class=FileResponse,  status_code=204)
def export_class(
        class_id: UUID,
        export_format: ExportFormat,
        service: AcademicStructureService = Depends(get_authenticated_service(AcademicStructureService))
    ):
    file_path= service.export_class(class_id, export_format.value)

    return FileResponse(
        path=file_path,
        filename=file_path.split("/")[-1],
        media_type="application/octet-stream"
    )

@router.delete("/{class_id}", status_code=204)
def delete_class(
        class_id: UUID,
        factory: ClassFactory = Depends(get_authenticated_factory(ClassFactory))
    ):
    return factory.delete_class(class_id)










