from datetime import datetime, date
from sqlalchemy.orm import declared_attr
from uuid import UUID, uuid4

from pydantic import(
    BaseModel,
    Field,
    EmailStr,
    field_validator
)

from typing import(
    Optional
)