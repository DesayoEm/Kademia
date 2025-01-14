from sqlalchemy.orm import declared_attr
from typing import List, Optional
from uuid import uuid4
from enum import Enum
from datetime import timezone


from datetime import (
    datetime,
    date)

from sqlalchemy import (
    ForeignKey,
    PrimaryKeyConstraint,
    UniqueConstraint,
    func,
    Integer,
    Index,
    Float,
    String,
    Boolean,
    Date,
    DateTime,
    Text,
    Enum,
    DECIMAL
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship
)
from sqlalchemy.dialects.postgresql import UUID, ARRAY

class Base(DeclarativeBase):
    pass