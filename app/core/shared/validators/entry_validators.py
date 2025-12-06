from app.core.shared.exceptions import (
    EmptyFieldError,
    TextTooShortError,
    TextTooLongError,
)


class EntryValidator:
    def __init__(self):
        pass

    @staticmethod
    def validate_description(value: str, domain: str) -> str:
        value = (value or "").strip()

        if not value:
            raise EmptyFieldError(entry=value, domain=domain)
        if len(value.strip()) < 3:
            raise TextTooShortError(entry=value, domain=domain, min_length=3)
        if len(value.strip()) > 3000:
            raise TextTooLongError(entry=value, max_length=100, domain=domain)

        return value.strip().title()
