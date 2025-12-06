from uuid import UUID
from typing import List
from fastapi import Depends, APIRouter
from fastapi.responses import FileResponse
from fastapi import UploadFile, File

from app.core.assessment.factories.grade import GradeFactory
from app.core.assessment.factories.total_grade import TotalGradeFactory
from app.core.assessment.schemas.grade import GradeResponse, GradeFilterParams
from app.core.assessment.schemas.total_grade import (
    TotalGradeFilterParams,
    TotalGradeResponse,
)
from app.core.curriculum.factories.student_subject import StudentSubjectFactory
from app.core.curriculum.schemas.student_subject import (
    StudentSubjectFilterParams,
    StudentSubjectResponse,
)
from app.core.documents.factories.award_factory import AwardFactory
from app.core.documents.factories.document_factory import DocumentFactory
from app.core.documents.schemas.student_award import AwardResponse, AwardFilterParams
from app.core.documents.schemas.student_document import (
    DocumentResponse,
    DocumentFilterParams,
)
from app.core.identity.factories.student import StudentFactory
from app.core.progression.factories.promotion import PromotionFactory
from app.core.progression.factories.repetition import RepetitionFactory
from app.core.progression.schemas.promotion import (
    PromotionResponse,
    PromotionFilterParams,
)
from app.core.progression.schemas.repetition import (
    RepetitionResponse,
    RepetitionFilterParams,
)
from app.core.shared.services.file_storage.s3_upload import S3Upload
from app.core.identity.services.student_service import StudentService
from app.core.shared.schemas.enums import ExportFormat, ArchiveReason

from app.core.identity.schemas.student import (
    StudentCreate,
    StudentUpdate,
    StudentResponse,
    StudentFilterParams,
    StudentAudit,
)
from app.core.identity.services.profile_picture_service import ProfilePictureService
from app.core.shared.schemas.shared_models import ArchiveRequest, UploadResponse
from app.core.auth.services.token_service import TokenService
from app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from app.core.auth.services.dependencies.current_user_deps import (
    get_authenticated_factory,
    get_authenticated_service,
)
from app.core.transfer.factories.transfer import TransferFactory
from app.core.transfer.schemas.department_transfer import (
    DepartmentTransferFilterParams,
    DepartmentTransferResponse,
)

token_service = TokenService()
access = AccessTokenBearer()
router = APIRouter()


# Archive routers
@router.get("/archive/students", response_model=List[StudentResponse])
def get_archived_students(
    filters: StudentFilterParams = Depends(),
    factory: StudentFactory = Depends(get_authenticated_factory(StudentFactory)),
):
    return factory.get_all_archived_students(filters)


@router.get("/archive/students/{student_id}/audit", response_model=StudentAudit)
def get_archived_student_audit(
    student_id: UUID,
    factory: StudentFactory = Depends(get_authenticated_factory(StudentFactory)),
):
    return factory.get_archived_student(student_id)


@router.get("/archive/students/{student_id}", response_model=StudentResponse)
def get_archived_student(
    student_id: UUID,
    factory: StudentFactory = Depends(get_authenticated_factory(StudentFactory)),
):
    return factory.get_archived_student(student_id)


@router.patch("/archive/students/{student_id}", response_model=StudentResponse)
def restore_student(
    student_id: UUID,
    factory: StudentFactory = Depends(get_authenticated_factory(StudentFactory)),
):
    return factory.restore_student(student_id)


@router.delete("/archive/students/{student_id}", status_code=204)
def delete_archived_student(
    student_id: UUID,
    factory: StudentFactory = Depends(get_authenticated_factory(StudentFactory)),
):
    return factory.delete_archived_student(student_id)


# Active routers
@router.post(
    "/students/{student_id}/profile/profile-picture",
    response_model=UploadResponse,
    status_code=201,
)
def upload_profile_pic(
    student_id: UUID,
    file: UploadFile = File(...),
    service: ProfilePictureService = Depends(
        get_authenticated_service(ProfilePictureService)
    ),
    factory: StudentFactory = Depends(get_authenticated_factory(StudentFactory)),
):
    student = factory.get_student(student_id)
    result = service.upload_profile_picture(file, student)

    return UploadResponse(**result)


@router.delete("/students/{student_id}/profile/profile-picture", status_code=204)
def remove_profile_pic(
    student_id: UUID,
    service: ProfilePictureService = Depends(
        get_authenticated_service(ProfilePictureService)
    ),
    factory: StudentFactory = Depends(get_authenticated_factory(StudentFactory)),
):
    student = factory.get_student(student_id)
    return service.remove_profile_pic(student)


@router.get("/students/{student_id}/profile/profile-picture")
def get_student_profile_pic(
    student_id: UUID,
    service: S3Upload = Depends(get_authenticated_service(S3Upload)),
    factory: StudentFactory = Depends(get_authenticated_factory(StudentFactory)),
):
    student = factory.get_student(student_id)
    key = student.profile_s3_key
    return service.generate_presigned_url(key)


@router.post("/students/", response_model=StudentResponse, status_code=201)
def create_student(
    payload: StudentCreate,
    factory: StudentFactory = Depends(get_authenticated_factory(StudentFactory)),
):
    return factory.create_student(payload)


@router.get("/students/{student_id}/audit", response_model=StudentAudit)
def get_student_audit(
    student_id: UUID,
    factory: StudentFactory = Depends(get_authenticated_factory(StudentFactory)),
):
    return factory.get_student(student_id)


@router.get("/students/{student_id}/enrollments", response_model=StudentSubjectResponse)
def get_student_subjects(
    student_id: UUID,
    filters: StudentSubjectFilterParams = Depends(),
    factory: StudentSubjectFactory = Depends(
        get_authenticated_factory(StudentSubjectFactory)
    ),
):
    filters.student_id = student_id
    return factory.get_all_student_subjects(filters)


@router.get("/students/{student_id}/documents", response_model=List[DocumentResponse])
def get_student_documents(
    student_id: UUID,
    filters: DocumentFilterParams = Depends(),
    factory: DocumentFactory = Depends(get_authenticated_factory(DocumentFactory)),
):
    filters.student_id = student_id
    return factory.get_all_documents(filters)


@router.get("/", response_model=List[AwardResponse])
def get_student_awards(
    student_id: UUID,
    filters: AwardFilterParams = Depends(),
    factory: AwardFactory = Depends(get_authenticated_factory(AwardFactory)),
):
    filters.student_id = student_id
    return factory.get_all_awards(filters)


@router.get("/students/{student_id}/grades", response_model=GradeResponse)
def get_student_grades(
    student_id: UUID,
    filters: GradeFilterParams = Depends(),
    factory: GradeFactory = Depends(get_authenticated_factory(GradeFactory)),
):
    filters.student_id = student_id
    return factory.get_all_grades(filters)


@router.get("/students/{student_id}/total-grades", response_model=TotalGradeResponse)
def get_student_total_grades(
    student_id: UUID,
    filters: TotalGradeFilterParams = Depends(),
    factory: TotalGradeFactory = Depends(get_authenticated_factory(TotalGradeFactory)),
):
    filters.student_id = student_id
    return factory.get_all_total_grades(filters)


@router.get(
    "/students/{student_id}/transfers/", response_model=List[DepartmentTransferResponse]
)
def get_student_transfers(
    student_id: UUID,
    filters: DepartmentTransferFilterParams = Depends(),
    factory: TransferFactory = Depends(get_authenticated_factory(TransferFactory)),
):
    filters.student_id = student_id
    return factory.get_all_transfers(filters)


@router.get("/students/{student_id}/transfers/", response_model=List[PromotionResponse])
def get_student_promotions(
    student_id: UUID,
    filters: PromotionFilterParams = Depends(),
    factory: PromotionFactory = Depends(get_authenticated_factory(PromotionFactory)),
):
    filters.student_id = student_id
    return factory.get_all_promotions(filters)


@router.get(
    "/students/{student_id}/repetitions/", response_model=List[RepetitionResponse]
)
def get_student_repetitions(
    student_id: UUID,
    filters: RepetitionFilterParams = Depends(),
    factory: RepetitionFactory = Depends(get_authenticated_factory(RepetitionFactory)),
):
    filters.student_id = student_id
    return factory.get_all_repetitions(filters)


@router.get("/students/{student_id}", response_model=StudentResponse)
def get_student(
    student_id: UUID,
    factory: StudentFactory = Depends(get_authenticated_factory(StudentFactory)),
):
    return factory.get_student(student_id)


@router.get("/students", response_model=List[StudentResponse])
def get_students(
    filters: StudentFilterParams = Depends(),
    factory: StudentFactory = Depends(get_authenticated_factory(StudentFactory)),
):
    return factory.get_all_students(filters)


@router.put("/students/{student_id}", response_model=StudentResponse)
def update_student(
    payload: StudentUpdate,
    student_id: UUID,
    factory: StudentFactory = Depends(get_authenticated_factory(StudentFactory)),
):
    payload = payload.model_dump(exclude_unset=True)
    return factory.update_student(student_id, payload)


@router.patch("/students/{student_id}/deep_archive", status_code=204)
def cascade_archive_student(
    student_id: UUID,
    reason: ArchiveReason,
    service: StudentService = Depends(get_authenticated_service(StudentService)),
):
    return service.cascade_archive_student(student_id, reason)


@router.patch("/students/{student_id}/archive", status_code=200)
def archive_student(
    student_id: UUID,
    reason: ArchiveRequest,
    factory: StudentFactory = Depends(get_authenticated_factory(StudentFactory)),
):
    factory.archive_student(student_id, reason)
    return "Archive successful"


@router.patch("/students/{student_id}/guardian", response_model=StudentResponse)
def change_guardian(
    student_id: UUID,
    guardian_id: UUID,
    service: StudentService = Depends(get_authenticated_service(StudentService)),
):
    return service.change_guardian(student_id, guardian_id)


@router.patch(
    "/students/{student_id}/department/assign", response_model=StudentResponse
)
def assign_department(
    student_id: UUID,
    department_id: UUID,
    service: StudentService = Depends(get_authenticated_service(StudentService)),
):
    return service.assign_department(student_id, department_id)


@router.patch(
    "/students/{student_id}/department/remove", response_model=StudentResponse
)
def remove_department(
    student_id: UUID,
    service: StudentService = Depends(get_authenticated_service(StudentService)),
):
    return service.assign_department(student_id)


@router.patch("/students/{student_id}/class/assign", response_model=StudentResponse)
def assign_class(
    student_id: UUID,
    class_id: UUID,
    service: StudentService = Depends(get_authenticated_service(StudentService)),
):
    return service.assign_class(student_id, class_id)


@router.patch("/students/{student_id}/class/remove", response_model=StudentResponse)
def remove_class(
    student_id: UUID,
    service: StudentService = Depends(get_authenticated_service(StudentService)),
):
    return service.assign_class(student_id)


@router.post(
    "/students/{student_id}/export", response_class=FileResponse, status_code=204
)
def export_student(
    student_id: UUID,
    export_format: ExportFormat,
    service: StudentService = Depends(get_authenticated_service(StudentService)),
):
    file_path = service.export_student_audit(student_id, export_format.value)

    return FileResponse(
        path=file_path,
        filename=file_path.split("/")[-1],
        media_type="application/octet-stream",
    )


@router.delete("/students/{student_id}", status_code=204)
def delete_student(
    student_id: UUID,
    factory: StudentFactory = Depends(get_authenticated_factory(StudentFactory)),
):
    return factory.delete_student(student_id)
