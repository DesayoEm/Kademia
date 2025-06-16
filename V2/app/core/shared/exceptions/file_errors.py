from .base_error import KademiaError


class FileError(KademiaError):
    """Base exception class for entry-related exceptions."""

class EmptyFileError(FileError):
    """Raised when a required file is empty."""

    def __init__(self, entry: str):
        super().__init__()
        self.user_message = "No file found!"
        self.log_message = f"Upload attempted without file: {entry}"


class FileTooSmallError(FileError):
    """Raised when a file is smaller than accepted."""

    def __init__(self, size: int, threshold: str):
        super().__init__()
        self.user_message = f"File needs to be larger than {threshold}"
        self.log_message = f"Upload attempted with small file: {size} bytes"


class FileTooLargeError(FileError):
    """Raised when a file is larger than acceptable."""

    def __init__(self, size: int, threshold: str):
        super().__init__()
        self.user_message = f"File needs to be smaller than {threshold}"
        self.log_message = f"Upload attempted with large file: {size} bytes"


class UnsupportedFileFormatError(FileError):
    """Raised when a file is in an unsupported format."""

    def __init__(self, file_type: str, acceptable_types: str):
        super().__init__()
        self.user_message = f"File format not supported. Acceptable formats: {acceptable_types}"
        self.log_message = f"Upload attempted with unsupported file type: {file_type}"


class AbsentKeyError(FileError):
    """Raised when a S3 key is not found in the database."""

    def __init__(self, entry: str):
        super().__init__()
        self.user_message = "S3 key cannot be found!"
        self.log_message = f"S3 key cannot be found!: {entry}"

