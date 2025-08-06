
from uuid import UUID
from typing import List
from fastapi import Depends, APIRouter
from fastapi.responses import FileResponse
from fastapi import UploadFile, File

from app.core.identity.factories.student import StudentFactory
from app.core.shared.services.file_storage.s3_upload import S3Upload
from app.core.identity.services.student_service import StudentService
from app.core.shared.schemas.enums import ExportFormat, ArchiveReason

from app.core.identity.schemas.student import StudentCreate, StudentUpdate, StudentResponse, StudentFilterParams, \
    StudentAudit
from app.core.identity.services.profile_picture_service import ProfilePictureService
from app.core.shared.schemas.shared_models import ArchiveRequest, UploadResponse
from app.core.auth.services.token_service import TokenService
from app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from app.core.auth.services.dependencies.current_user_deps import get_authenticated_factory, \
    get_authenticated_service

token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()

#Archive routers
@router.get("/", response_model=List[StudentResponse])
def get_archived_students(
        filters: StudentFilterParams = Depends(),
        factory: StudentFactory = Depends(get_authenticated_factory(StudentFactory))
    ):
    return factory.get_all_archived_students(filters)


@router.get("/archive/students/student_id}/audit", response_model=StudentAudit)
def get_archived_student_audit(
        student_id: UUID,
        factory: StudentFactory = Depends(get_authenticated_factory(StudentFactory))
    ):
    return factory.get_archived_student(student_id)


@router.get("/archive/students/student_id}", response_model=StudentResponse)
def get_archived_student(
        student_id: UUID,
        factory: StudentFactory = Depends(get_authenticated_factory(StudentFactory))
    ):
    return factory.get_archived_student(student_id)


@router.patch("/archive/students/student_id}", response_model=StudentResponse)
def restore_student(
        student_id: UUID,
        factory: StudentFactory = Depends(get_authenticated_factory(StudentFactory))
):
    return factory.restore_student(student_id)


@router.delete("/archive/students/student_id}", status_code=204)
def delete_archived_student(
        student_id: UUID,
        factory: StudentFactory = Depends(get_authenticated_factory(StudentFactory))
):
    return factory.delete_archived_student(student_id)


#Active routers
@router.post("/students/{student_id}/profile/profile-picture", response_model= UploadResponse,
             status_code=201)
def upload_profile_pic(
        student_id: UUID,
        file: UploadFile = File(...),
        service: ProfilePictureService = Depends(get_authenticated_service(ProfilePictureService)),
        factory: StudentFactory = Depends(get_authenticated_factory(StudentFactory))
):
    student = factory.get_student(student_id)
    result = service.upload_profile_picture(file, student)

    return UploadResponse(**result)


@router.delete("/students/{student_id}/profile/profile-picture", status_code=204)
def remove_profile_pic(
        student_id: UUID,
        service: ProfilePictureService = Depends(get_authenticated_service(ProfilePictureService)),
        factory: StudentFactory = Depends(get_authenticated_factory(StudentFactory))
    ):
        student = factory.get_student(student_id)
        return service.remove_profile_pic(student)


@router.get("/students/{student_id}/profile/profile-picture")
def get_student_profile_pic(
        student_id: UUID,
        service: S3Upload = Depends(get_authenticated_service(S3Upload)),
        factory: StudentFactory = Depends(get_authenticated_factory(StudentFactory))
    ):
        student = factory.get_student(student_id)
        key = student.profile_s3_key
        return service.generate_presigned_url(key)


@router.post("/students", response_model= StudentResponse, status_code=201)
def create_student(
        payload:StudentCreate,
        factory: StudentFactory = Depends(get_authenticated_factory(StudentFactory))
    ):
        return factory.create_student(payload)


@router.get("/students", response_model=List[StudentResponse])
def get_students(
        filters: StudentFilterParams = Depends(),
        factory: StudentFactory = Depends(get_authenticated_factory(StudentFactory))
    ):
        return factory.get_all_students(filters)


@router.get("/students/{student_id}/audit", response_model=StudentAudit)
def get_student_audit(
        student_id: UUID,
        factory: StudentFactory = Depends(get_authenticated_factory(StudentFactory))
    ):
        return factory.get_student(student_id)


@router.get("/students/{student_id}", response_model=StudentResponse)
def get_student(
        student_id: UUID,
        factory: StudentFactory = Depends(get_authenticated_factory(StudentFactory))
    ):
        return factory.get_student(student_id)


@router.put("/students/{student_id}", response_model=StudentResponse)
def update_student(
        payload: StudentUpdate,
        student_id: UUID,
        factory: StudentFactory = Depends(get_authenticated_factory(StudentFactory))
    ):
        payload = payload.model_dump(exclude_unset=True)
        return factory.update_student(student_id, payload)


@router.patch("/students/{student_id}/deep_archive", status_code=204)
def cascade_archive_student(
        student_id: UUID,
        reason:ArchiveReason,
        service: StudentService = Depends(get_authenticated_service(StudentService)),
):
    return service.cascade_student_archive(student_id, reason.value)


@router.patch("/students/{student_id}/archive", status_code=204)
def archive_student(
        student_id: UUID,
        reason:ArchiveRequest,
        factory: StudentFactory = Depends(get_authenticated_factory(StudentFactory))
    ):
        return factory.archive_student(student_id, reason.reason)


@router.patch("/students/{student_id}/guardian", response_model=StudentResponse)
def change_guardian(
        student_id: UUID,
        guardian_id:UUID,
        service: StudentService = Depends(get_authenticated_service(StudentService))
    ):
        return service.change_guardian(student_id, guardian_id)

@router.patch("/students/{student_id}/department/assign", response_model=StudentResponse)
def assign_department(
        student_id: UUID,
        department_id:UUID,
        service: StudentService = Depends(get_authenticated_service(StudentService))
    ):
        return service.assign_department(student_id, department_id)


@router.patch("/students/{student_id}/department/remove", response_model=StudentResponse)
def remove_department(
        student_id: UUID,
        service: StudentService = Depends(get_authenticated_service(StudentService))
    ):
        return service.assign_department(student_id)


@router.patch("/students/{student_id}/class/assign",response_model=StudentResponse)
def assign_class(
        student_id: UUID,
        class_id:UUID,
        service: StudentService = Depends(get_authenticated_service(StudentService))
    ):
        return service.assign_class(student_id, class_id)


@router.patch("/students/{student_id}/class/remove", response_model=StudentResponse)
def remove_class(
        student_id: UUID,
        service: StudentService = Depends(get_authenticated_service(StudentService))
    ):
        return service.assign_class(student_id)


@router.post("/students/{student_id}/export", response_class=FileResponse,  status_code=204)
def export_student(
        student_id: UUID,
        export_format: ExportFormat,
        service: StudentService = Depends(get_authenticated_service(StudentService))
    ):
    file_path= service.export_student_audit(student_id, export_format.value)

    return FileResponse(
        path=file_path,
        filename=file_path.split("/")[-1],
        media_type="application/octet-stream"
    )


@router.delete("/students/{student_id}", status_code=204)
def delete_student(
        student_id: UUID,
        factory: StudentFactory = Depends(get_authenticated_factory(StudentFactory))
    ):
        return factory.delete_student(student_id)











