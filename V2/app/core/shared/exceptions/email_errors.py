from .base_error import KademiaError

class EmailError(KademiaError):
    """Base exception for all email_service-related exceptions"""


class EmailFailedToSendError(EmailError):
    """Raised when sending an email_service fails."""

    def __init__(self, detail: str):
        self.user_message = f"Failed to send email_service!"
        self.log_message = f"Failed to send email_service: {detail}."

        super().__init__()