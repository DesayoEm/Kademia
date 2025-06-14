import magic

from sqlalchemy.orm import Session
from sqlalchemy import func, Integer
from V2.app.core.identity.models.student import Student
from V2.app.core.shared.exceptions.entry_validation_errors import EmptyFileError, FileTooSmallError, \
    UnsupportedFileFormatError
from V2.app.core.shared.services.upload_service.upload import S3Upload
from V2.app.infra.settings import config




class IdentityService:
    def __init__(self, session: Session, current_user = None):
        self.session = session
        self.upload = S3Upload()
        self.current_user = current_user


    def upload_profile_picture(self, file, user):

        kb = 1024
        mb  = 1024 * kb

        supported_file_types = {
            'image/png': 'png',
            'image/jpeg': 'jpg'
        }

        if not file:
            raise EmptyFileError(entry=file)

        contents = file.file.read()
        size = len(contents)

        if not 0 < size <= 1 * mb:
            raise FileTooSmallError(size = size, threshold = "1 MB")

        file_type = magic.from_buffer(buffer=contents, mime = True)

        if file_type not in supported_file_types:
            raise UnsupportedFileFormatError(file_type=file_type, acceptable_types="JPEG or PNG")

        profile_folder = config.PROFILE_PICTURES_FOLDER
        file_name = f"{profile_folder}{user.user_type.value}_{user.first_name}_{user.last_name}_profile_photo.{supported_file_types[file_type]}"
        self.upload.s3_upload(contents = contents, key = file_name)

        return {
            "filename": file_name,
            "size": len(contents),
            "file_type": file_type
        }


    def generate_student_id(self, start_year: int):
        school_code = 'SCH'
        year_code = str(start_year)[2:]
        prefix = f"{school_code}-{year_code}-"
        pattern = f"{prefix}%"

        result = self.session.query(
            func.max(
                func.cast(
                    func.substring(Student.student_id, len(prefix) + 1),Integer
                )
            )
        ).filter(
            Student.student_id.like(pattern),
            Student.session_start_year == start_year
        ).scalar()

        next_serial = 1 if result is None else result + 1
        formatted_serial = f"{next_serial:05d}"
        student_id = f"{school_code}-{year_code}-{formatted_serial}"
        return student_id