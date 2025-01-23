"""Added access level and user type and their default values to Students, Parents and Staff

Revision ID: df2fb13209bb
Revises: 85043605e3a7
Create Date: 2025-01-23 22:01:55.461712

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from V2.app.database.models.common_imports import Base


# revision identifiers, used by Alembic.
revision: str = 'df2fb13209bb'
down_revision: Union[str, None] = '85043605e3a7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.alter_column('students', 'access_level',
                    existing_type=sa.Enum('Inactive', 'User', 'Admin', 'Superuser', 'System', name='accesslevel'),
                    server_default='User')
    op.alter_column('students', 'user_type',
                    existing_type=sa.Enum('Student', 'Parent', 'Staff', 'System', name='usertype'),
                    server_default='Student')

    op.alter_column('parents', 'access_level',
                    existing_type=sa.Enum('Inactive', 'User', 'Admin', 'Superuser', 'System', name='accesslevel'),
                    server_default='User')
    op.alter_column('parents', 'user_type',
                    existing_type=sa.Enum('Student', 'Parent', 'Staff', 'System', name='usertype'),
                    server_default='Parent')

    op.alter_column('staff', 'access_level',
                    existing_type=sa.Enum('Inactive', 'User', 'Admin', 'Superuser', 'System', name='accesslevel'),
                    server_default='Admin')
    op.alter_column('staff', 'user_type',
                    existing_type=sa.Enum('Student', 'Parent', 'Staff', 'System', name='usertype'),
                    server_default='Staff')


def downgrade() -> None:
    op.alter_column('students', 'access_level',
                    existing_type=sa.Enum('Inactive', 'User', 'Admin', 'Superuser', 'System', name='accesslevel'),
                    server_default=None)
    op.alter_column('students', 'user_type',
                    existing_type=sa.Enum('Student', 'Parent', 'Staff', 'System', name='usertype'),
                    server_default=None)

    op.alter_column('parents', 'access_level',
                    existing_type=sa.Enum('Inactive', 'User', 'Admin', 'Superuser', 'System', name='accesslevel'),
                    server_default=None)
    op.alter_column('parents', 'user_type',
                    existing_type=sa.Enum('Student', 'Parent', 'Staff', 'System', name='usertype'),
                    server_default=None)

    op.alter_column('staff', 'access_level',
                    existing_type=sa.Enum('Inactive', 'User', 'Admin', 'Superuser', 'System', name='accesslevel'),
                    server_default=None)
    op.alter_column('staff', 'user_type',
                    existing_type=sa.Enum('Student', 'Parent', 'Staff', 'System', name='usertype'),
                    server_default=None)