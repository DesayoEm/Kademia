from base import *
from validators import UserType

class Users(Base):
    __tablename__ = 'users'

    id: Mapped[UUID]  = mapped_column(UUID(as_uuid = True), primary_key= True, default = uuid4)
    password_hash: Mapped[str] = mapped_column(String(300), nullable = False)
    user_type: Mapped[UserType] = mapped_column(Enum(UserType), nullable=False)
    user_id: Mapped[UUID]
    is_active: Mapped[bool] = mapped_column(Boolean, default = True)
    last_login: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    created_by: Mapped[UUID] = mapped_column(ForeignKey('staff.id'), nullable= False)
    updated_at: Mapped[datetime] = mapped_column(DateTime,default=func.now(),onupdate=func.now(), nullable=False)
    updated_by: Mapped[UUID] = mapped_column(ForeignKey('staff.id'))


class Roles(Base):
    __tablename__ = 'roles'
    id: Mapped[UUID]  = mapped_column(UUID(as_uuid = True), primary_key= True, default = uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable = False, unique=True)
    description: Mapped[str] = mapped_column(String(500), nullable = False, unique=True)


class UserRoles(Base):
    __tablename__ = 'user_roles'
    user_id: Mapped[UUID]
    role_id: Mapped[UUID] = mapped_column(ForeignKey='roles.id', nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    created_by: Mapped[UUID] = mapped_column(ForeignKey('staff.id'), nullable= False)


class Permissions(Base):
    __tablename__ = 'permissions'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable = False, unique=True)
    description: Mapped[str] = mapped_column(String(500), nullable = False, unique=True)


class RolePermissions(Base):
    __tablename__ = 'role_permissions'
    role_id: Mapped[UUID] = mapped_column(ForeignKey='roles.id', nullable=False)
    permisssion_id: Mapped[UUID] = mapped_column(ForeignKey='roles.id', nullable=False)