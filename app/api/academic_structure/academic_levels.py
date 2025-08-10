
from uuid import UUID
from typing import List
from fastapi.responses import FileResponse

from app.core.academic_structure.factories.classes import ClassFactory
from app.core.academic_structure.schemas.classes import ClassResponse, ClassFilterParams, ClassAudit
from app.core.academic_structure.services.academic_structure import AcademicStructureService
from app.core.curriculum.factories.academic_level_subject import AcademicLevelSubjectFactory
from app.core.curriculum.schemas.academic_level_subject import AcademicLevelSubjectResponse
from app.core.identity.factories.student import StudentFactory
from app.core.identity.schemas.student import StudentResponse, StudentFilterParams
from app.core.shared.schemas.enums import ExportFormat
from app.core.shared.schemas.shared_models import ArchiveRequest
from fastapi import Depends, APIRouter
from app.core.auth.services.dependencies.current_user_deps import get_authenticated_factory, \
    get_authenticated_service
from app.core.academic_structure.factories.academic_level import AcademicLevelFactory
from app.core.academic_structure.schemas.academic_level import(
    AcademicLevelCreate, AcademicLevelUpdate, AcademicLevelFilterParams, AcademicLevelResponse,
    AcademicLevelAudit
)
from app.core.auth.services.token_service import TokenService
from app.core.auth.services.dependencies.token_deps import AccessTokenBearer


token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()


#Archive routers
@router.get("/archive/levels/", response_model=List[AcademicLevelResponse])
def get_archived_levels(
        filters: AcademicLevelFilterParams = Depends(),
        factory: AcademicLevelFactory = Depends(get_authenticated_factory(AcademicLevelFactory))
):
    return factory.get_all_archived_academic_levels(filters)


@router.get("/archive/levels/{level_id}/audit", response_model=AcademicLevelAudit)
def get_archived_level_audit(
        level_id: UUID,
        factory: AcademicLevelFactory = Depends(get_authenticated_factory(AcademicLevelFactory))
    ):
    return factory.get_archived_academic_level(level_id)


@router.get("/archive/levels/{level_id}", response_model=AcademicLevelResponse)
def get_archived_level(
        level_id: UUID,
        factory: AcademicLevelFactory = Depends(get_authenticated_factory(AcademicLevelFactory))
    ):
    return factory.get_archived_academic_level(level_id)


@router.patch("/archive/levels/{level_id}", response_model=AcademicLevelResponse)
def restore_level(
        level_id: UUID,
        factory: AcademicLevelFactory = Depends(get_authenticated_factory(AcademicLevelFactory))
    ):
    return factory.restore_academic_level(level_id)


@router.delete("/archive/levels/{level_id}", status_code=204)
def delete_archived_level(
        level_id: UUID,
        factory: AcademicLevelFactory = Depends(get_authenticated_factory(AcademicLevelFactory))
    ):
    return factory.delete_archived_academic_level(level_id)


#Active routers

@router.post("levels/", response_model= AcademicLevelResponse, status_code=201)
def create_level(
        payload:AcademicLevelCreate,
        factory: AcademicLevelFactory = Depends(get_authenticated_factory(AcademicLevelFactory))
    ):
    return factory.create_academic_level(payload)



@router.get("levels/{level_id}/audit", response_model=AcademicLevelAudit)
def get_level_audit(
        level_id: UUID,
        factory: AcademicLevelFactory = Depends(get_authenticated_factory(AcademicLevelFactory))
    ):
    return factory.get_academic_level(level_id)


@router.get("levels/", response_model=List[AcademicLevelResponse])
def get_levels(
        filters: AcademicLevelFilterParams = Depends(),
        factory: AcademicLevelFactory = Depends(get_authenticated_factory(AcademicLevelFactory))
    ):
    return factory.get_all_academic_levels(filters)


@router.get("/levels/{level_id}/students", response_model=List[StudentResponse])
def get_level_students(
        level_id: UUID,
        filters: StudentFilterParams = Depends(),
        factory: StudentFactory = Depends(get_authenticated_factory(StudentFactory))
    ):
        filters.level_id = level_id
        return factory.get_all_students(filters)


@router.get("/levels/{level_id}/classes", response_model=List[ClassResponse])
def get_level_classes(
        level_id: UUID,
        filters: ClassFilterParams = Depends(),
        factory: ClassFactory = Depends(get_authenticated_factory(ClassFactory))
    ):
        filters.level_id = level_id
        return factory.get_all_classes(filters)


@router.get("/levels/{level_id}/subjects", response_model=List[AcademicLevelSubjectResponse])
def get_level_classes(
        level_subject_id: UUID,
        filters: ClassFilterParams = Depends(),
        factory: AcademicLevelSubjectFactory = Depends(get_authenticated_factory(AcademicLevelSubjectFactory))
    ):
        filters.level_id = level_subject_id
        return factory.get_all_academic_level_subjects(filters)


@router.get("levels/{level_id}", response_model=AcademicLevelResponse)
def get_level(
        level_id: UUID, 
        factory: AcademicLevelFactory = Depends(get_authenticated_factory(AcademicLevelFactory))
    ):
    return factory.get_academic_level(level_id)


@router.put("levels/{level_id}", response_model=AcademicLevelResponse)
def update_level(
        payload: AcademicLevelUpdate, level_id: UUID,
        factory: AcademicLevelFactory = Depends(get_authenticated_factory(AcademicLevelFactory))
    ):
    update_data = payload.model_dump(exclude_unset=True)
    return factory.update_academic_level(level_id, update_data)


@router.patch("levels/{level_id}",  status_code=204)
def archive_level(
        level_id: UUID, reason:ArchiveRequest,
        factory: AcademicLevelFactory = Depends(get_authenticated_factory(AcademicLevelFactory))
    ):
    return factory.archive_academic_level(level_id, reason.reason)


@router.post("levels/{level_id}", response_class=FileResponse,  status_code=204)
def export_level_audit(
        level_id: UUID, 
        export_format: ExportFormat, 
        service: AcademicStructureService = Depends(get_authenticated_service(AcademicStructureService))
    ):
    file_path= service.export_academic_level(level_id, export_format.value)

    return FileResponse(
        path=file_path,
        filename=file_path.split("/")[-1],
        media_type="application/octet-stream"
    )

@router.delete("levels/{level_id}", status_code=204)
def delete_level(
        level_id: UUID, 
        factory: AcademicLevelFactory = Depends(get_authenticated_factory(AcademicLevelFactory))
    ):
    return factory.delete_academic_level(level_id)










