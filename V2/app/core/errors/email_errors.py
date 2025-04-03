from .base_error import KademiaError

class EmailError(KademiaError):
    """Base exception for all email-related errors"""


class EmailFailedToSendError(EmailError):
    """Raised when sending an email fails."""

    def __init__(self, detail: str):
        self.user_message = f"Failed to send email!"
        self.log_message = f"Failed to send email: {detail}."

        super().__init__()