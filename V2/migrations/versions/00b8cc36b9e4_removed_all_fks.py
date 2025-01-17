"""Removed all FKs

Revision ID: 00b8cc36b9e4
Revises: 065c752e0225
Create Date: 2025-01-17 22:31:59.051651

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from app.database.models.common_imports import Base


# revision identifiers, used by Alembic.
revision: str = '00b8cc36b9e4'
down_revision: Union[str, None] = '065c752e0225'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('access_level_changes_profile_id_fkey', 'access_level_changes', type_='foreignkey')
    op.drop_constraint('access_level_changes_changed_by_fkey', 'access_level_changes', type_='foreignkey')
    op.drop_constraint('admin_id_fkey', 'admin', type_='foreignkey')
    op.alter_column('classes', 'mentor_id',
               existing_type=sa.UUID(),
               nullable=False)
    op.alter_column('classes', 'created_by',
               existing_type=sa.UUID(),
               nullable=False)
    op.alter_column('classes', 'last_modified_by',
               existing_type=sa.UUID(),
               nullable=False)
    op.alter_column('classes', 'soft_deleted_by',
               existing_type=sa.UUID(),
               nullable=False)
    op.drop_constraint('classes_mentor_id_fkey', 'classes', type_='foreignkey')
    op.drop_constraint('classes_created_by_fkey', 'classes', type_='foreignkey')
    op.drop_constraint('classes_soft_deleted_by_fkey', 'classes', type_='foreignkey')
    op.drop_constraint('classes_last_modified_by_fkey', 'classes', type_='foreignkey')
    op.drop_constraint('commercial_id_fkey', 'commercial', type_='foreignkey')
    op.alter_column('departments', 'mentor_id',
               existing_type=sa.UUID(),
               nullable=False)
    op.alter_column('departments', 'created_by',
               existing_type=sa.UUID(),
               nullable=False)
    op.alter_column('departments', 'last_modified_by',
               existing_type=sa.UUID(),
               nullable=False)
    op.alter_column('departments', 'soft_deleted_by',
               existing_type=sa.UUID(),
               nullable=False)
    op.drop_constraint('departments_last_modified_by_fkey', 'departments', type_='foreignkey')
    op.drop_constraint('departments_mentor_id_fkey', 'departments', type_='foreignkey')
    op.drop_constraint('departments_created_by_fkey', 'departments', type_='foreignkey')
    op.drop_constraint('departments_soft_deleted_by_fkey', 'departments', type_='foreignkey')
    op.drop_constraint('educator_id_fkey', 'educator', type_='foreignkey')
    op.alter_column('educator_subjects', 'subject_id',
               existing_type=sa.UUID(),
               nullable=False)
    op.alter_column('educator_subjects', 'created_by',
               existing_type=sa.UUID(),
               nullable=False)
    op.alter_column('educator_subjects', 'last_modified_by',
               existing_type=sa.UUID(),
               nullable=False)
    op.alter_column('educator_subjects', 'soft_deleted_by',
               existing_type=sa.UUID(),
               nullable=False)
    op.drop_constraint('educator_subjects_created_by_fkey', 'educator_subjects', type_='foreignkey')
    op.drop_constraint('educator_subjects_last_modified_by_fkey', 'educator_subjects', type_='foreignkey')
    op.drop_constraint('educator_subjects_educator_id_fkey', 'educator_subjects', type_='foreignkey')
    op.drop_constraint('educator_subjects_soft_deleted_by_fkey', 'educator_subjects', type_='foreignkey')
    op.drop_constraint('educator_subjects_subject_id_fkey', 'educator_subjects', type_='foreignkey')
    op.alter_column('grades', 'subject_id',
               existing_type=sa.UUID(),
               nullable=False)
    op.alter_column('grades', 'department_id',
               existing_type=sa.UUID(),
               nullable=False)
    op.alter_column('grades', 'created_by',
               existing_type=sa.UUID(),
               nullable=False)
    op.alter_column('grades', 'last_modified_by',
               existing_type=sa.UUID(),
               nullable=False)
    op.alter_column('grades', 'soft_deleted_by',
               existing_type=sa.UUID(),
               nullable=False)
    op.drop_constraint('grades_last_modified_by_fkey', 'grades', type_='foreignkey')
    op.drop_constraint('grades_subject_id_fkey', 'grades', type_='foreignkey')
    op.drop_constraint('grades_graded_by_fkey', 'grades', type_='foreignkey')
    op.drop_constraint('grades_soft_deleted_by_fkey', 'grades', type_='foreignkey')
    op.drop_constraint('grades_created_by_fkey', 'grades', type_='foreignkey')
    op.drop_constraint('grades_department_id_fkey', 'grades', type_='foreignkey')
    op.drop_constraint('grades_student_id_fkey', 'grades', type_='foreignkey')
    op.drop_constraint('management_id_fkey', 'management', type_='foreignkey')
    op.alter_column('parents', 'created_by',
               existing_type=sa.UUID(),
               nullable=False)
    op.alter_column('parents', 'last_modified_by',
               existing_type=sa.UUID(),
               nullable=False)
    op.alter_column('parents', 'soft_deleted_by',
               existing_type=sa.UUID(),
               nullable=False)
    op.drop_constraint('parents_profile_id_key', 'parents', type_='unique')
    op.drop_constraint('parents_soft_deleted_by_fkey', 'parents', type_='foreignkey')
    op.drop_constraint('parents_profile_id_fkey', 'parents', type_='foreignkey')
    op.drop_constraint('parents_created_by_fkey', 'parents', type_='foreignkey')
    op.drop_constraint('parents_last_modified_by_fkey', 'parents', type_='foreignkey')
    op.alter_column('repetitions', 'from_class_id',
               existing_type=sa.UUID(),
               nullable=False)
    op.alter_column('repetitions', 'to_class_id',
               existing_type=sa.UUID(),
               nullable=False)
    op.alter_column('repetitions', 'status_updated_by',
               existing_type=sa.UUID(),
               nullable=False)
    op.alter_column('repetitions', 'created_by',
               existing_type=sa.UUID(),
               nullable=False)
    op.alter_column('repetitions', 'last_modified_by',
               existing_type=sa.UUID(),
               nullable=False)
    op.alter_column('repetitions', 'soft_deleted_by',
               existing_type=sa.UUID(),
               nullable=False)
    op.drop_constraint('repetitions_last_modified_by_fkey', 'repetitions', type_='foreignkey')
    op.drop_constraint('repetitions_student_id_fkey', 'repetitions', type_='foreignkey')
    op.drop_constraint('repetitions_soft_deleted_by_fkey', 'repetitions', type_='foreignkey')
    op.drop_constraint('repetitions_to_class_id_fkey', 'repetitions', type_='foreignkey')
    op.drop_constraint('repetitions_created_by_fkey', 'repetitions', type_='foreignkey')
    op.drop_constraint('repetitions_status_updated_by_fkey', 'repetitions', type_='foreignkey')
    op.drop_constraint('repetitions_from_class_id_fkey', 'repetitions', type_='foreignkey')
    op.alter_column('staff', 'created_by',
               existing_type=sa.UUID(),
               nullable=False)
    op.alter_column('staff', 'last_modified_by',
               existing_type=sa.UUID(),
               nullable=False)
    op.alter_column('staff', 'soft_deleted_by',
               existing_type=sa.UUID(),
               nullable=False)
    op.drop_constraint('staff_profile_id_key', 'staff', type_='unique')
    op.drop_constraint('staff_last_modified_by_fkey', 'staff', type_='foreignkey')
    op.drop_constraint('staff_soft_deleted_by_fkey', 'staff', type_='foreignkey')
    op.drop_constraint('staff_created_by_fkey', 'staff', type_='foreignkey')
    op.drop_constraint('staff_department_id_fkey', 'staff', type_='foreignkey')
    op.drop_constraint('staff_profile_id_fkey', 'staff', type_='foreignkey')
    op.drop_constraint('staff_role_id_fkey', 'staff', type_='foreignkey')
    op.alter_column('staff_departments', 'manager_id',
               existing_type=sa.UUID(),
               nullable=False)
    op.alter_column('staff_departments', 'created_by',
               existing_type=sa.UUID(),
               nullable=False)
    op.alter_column('staff_departments', 'last_modified_by',
               existing_type=sa.UUID(),
               nullable=False)
    op.alter_column('staff_departments', 'soft_deleted_by',
               existing_type=sa.UUID(),
               nullable=False)
    op.drop_constraint('staff_departments_last_modified_by_fkey', 'staff_departments', type_='foreignkey')
    op.drop_constraint('staff_departments_created_by_fkey', 'staff_departments', type_='foreignkey')
    op.drop_constraint('staff_departments_soft_deleted_by_fkey', 'staff_departments', type_='foreignkey')
    op.drop_constraint('staff_departments_manager_id_fkey', 'staff_departments', type_='foreignkey')
    op.alter_column('staff_roles', 'created_by',
               existing_type=sa.UUID(),
               nullable=False)
    op.alter_column('staff_roles', 'last_modified_by',
               existing_type=sa.UUID(),
               nullable=False)
    op.alter_column('staff_roles', 'soft_deleted_by',
               existing_type=sa.UUID(),
               nullable=False)
    op.drop_constraint('staff_roles_soft_deleted_by_fkey', 'staff_roles', type_='foreignkey')
    op.drop_constraint('staff_roles_created_by_fkey', 'staff_roles', type_='foreignkey')
    op.drop_constraint('staff_roles_last_modified_by_fkey', 'staff_roles', type_='foreignkey')
    op.alter_column('student_documents', 'created_by',
               existing_type=sa.UUID(),
               nullable=False)
    op.alter_column('student_documents', 'last_modified_by',
               existing_type=sa.UUID(),
               nullable=False)
    op.alter_column('student_documents', 'soft_deleted_by',
               existing_type=sa.UUID(),
               nullable=False)
    op.drop_constraint('student_documents_soft_deleted_by_fkey', 'student_documents', type_='foreignkey')
    op.drop_constraint('student_documents_last_modified_by_fkey', 'student_documents', type_='foreignkey')
    op.drop_constraint('student_documents_created_by_fkey', 'student_documents', type_='foreignkey')
    op.drop_constraint('student_documents_owner_id_fkey', 'student_documents', type_='foreignkey')
    op.alter_column('student_subjects', 'created_by',
               existing_type=sa.UUID(),
               nullable=False)
    op.alter_column('student_subjects', 'last_modified_by',
               existing_type=sa.UUID(),
               nullable=False)
    op.alter_column('student_subjects', 'soft_deleted_by',
               existing_type=sa.UUID(),
               nullable=False)
    op.drop_constraint('student_subjects_subject_id_fkey', 'student_subjects', type_='foreignkey')
    op.drop_constraint('student_subjects_soft_deleted_by_fkey', 'student_subjects', type_='foreignkey')
    op.drop_constraint('student_subjects_student_id_fkey', 'student_subjects', type_='foreignkey')
    op.drop_constraint('student_subjects_created_by_fkey', 'student_subjects', type_='foreignkey')
    op.drop_constraint('student_subjects_last_modified_by_fkey', 'student_subjects', type_='foreignkey')
    op.alter_column('student_transfers', 'created_by',
               existing_type=sa.UUID(),
               nullable=False)
    op.alter_column('student_transfers', 'last_modified_by',
               existing_type=sa.UUID(),
               nullable=False)
    op.alter_column('student_transfers', 'soft_deleted_by',
               existing_type=sa.UUID(),
               nullable=False)
    op.drop_constraint('student_transfers_created_by_fkey', 'student_transfers', type_='foreignkey')
    op.drop_constraint('student_transfers_student_id_fkey', 'student_transfers', type_='foreignkey')
    op.drop_constraint('student_transfers_status_updated_by_fkey', 'student_transfers', type_='foreignkey')
    op.drop_constraint('student_transfers_soft_deleted_by_fkey', 'student_transfers', type_='foreignkey')
    op.drop_constraint('student_transfers_last_modified_by_fkey', 'student_transfers', type_='foreignkey')
    op.alter_column('students', 'created_by',
               existing_type=sa.UUID(),
               nullable=False)
    op.alter_column('students', 'last_modified_by',
               existing_type=sa.UUID(),
               nullable=False)
    op.alter_column('students', 'soft_deleted_by',
               existing_type=sa.UUID(),
               nullable=False)
    op.drop_index('idx_students_profile_id', table_name='students')
    op.drop_index('idx_students_soft_deleted_at', table_name='students')
    op.drop_constraint('students_profile_id_key', 'students', type_='unique')
    op.drop_constraint('students_parent_id_fkey', 'students', type_='foreignkey')
    op.drop_constraint('students_department_id_fkey', 'students', type_='foreignkey')
    op.drop_constraint('students_soft_deleted_by_fkey', 'students', type_='foreignkey')
    op.drop_constraint('students_last_modified_by_fkey', 'students', type_='foreignkey')
    op.drop_constraint('students_created_by_fkey', 'students', type_='foreignkey')
    op.drop_constraint('students_profile_id_fkey', 'students', type_='foreignkey')
    op.drop_constraint('students_class_id_fkey', 'students', type_='foreignkey')
    op.alter_column('subjects', 'created_by',
               existing_type=sa.UUID(),
               nullable=False)
    op.alter_column('subjects', 'last_modified_by',
               existing_type=sa.UUID(),
               nullable=False)
    op.alter_column('subjects', 'soft_deleted_by',
               existing_type=sa.UUID(),
               nullable=False)
    op.drop_constraint('subjects_soft_deleted_by_fkey', 'subjects', type_='foreignkey')
    op.drop_constraint('subjects_last_modified_by_fkey', 'subjects', type_='foreignkey')
    op.drop_constraint('subjects_created_by_fkey', 'subjects', type_='foreignkey')
    op.drop_constraint('support_id_fkey', 'support', type_='foreignkey')
    op.alter_column('total_grades', 'created_by',
               existing_type=sa.UUID(),
               nullable=False)
    op.alter_column('total_grades', 'last_modified_by',
               existing_type=sa.UUID(),
               nullable=False)
    op.alter_column('total_grades', 'soft_deleted_by',
               existing_type=sa.UUID(),
               nullable=False)
    op.drop_constraint('total_grades_subject_id_fkey', 'total_grades', type_='foreignkey')
    op.drop_constraint('total_grades_last_modified_by_fkey', 'total_grades', type_='foreignkey')
    op.drop_constraint('total_grades_student_id_fkey', 'total_grades', type_='foreignkey')
    op.drop_constraint('total_grades_created_by_fkey', 'total_grades', type_='foreignkey')
    op.drop_constraint('total_grades_soft_deleted_by_fkey', 'total_grades', type_='foreignkey')
    op.alter_column('users', 'created_by',
               existing_type=sa.UUID(),
               nullable=False)
    op.alter_column('users', 'last_modified_by',
               existing_type=sa.UUID(),
               nullable=False)
    op.alter_column('users', 'soft_deleted_by',
               existing_type=sa.UUID(),
               nullable=False)
    op.drop_constraint('users_created_by_fkey', 'users', type_='foreignkey')
    op.drop_constraint('users_last_modified_by_fkey', 'users', type_='foreignkey')
    op.drop_constraint('users_soft_deleted_by_fkey', 'users', type_='foreignkey')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key('users_soft_deleted_by_fkey', 'users', 'staff', ['soft_deleted_by'], ['id'], ondelete='SET NULL')
    op.create_foreign_key('users_last_modified_by_fkey', 'users', 'staff', ['last_modified_by'], ['id'], ondelete='SET NULL')
    op.create_foreign_key('users_created_by_fkey', 'users', 'staff', ['created_by'], ['id'], ondelete='SET NULL')
    op.alter_column('users', 'soft_deleted_by',
               existing_type=sa.UUID(),
               nullable=True)
    op.alter_column('users', 'last_modified_by',
               existing_type=sa.UUID(),
               nullable=True)
    op.alter_column('users', 'created_by',
               existing_type=sa.UUID(),
               nullable=True)
    op.create_foreign_key('total_grades_soft_deleted_by_fkey', 'total_grades', 'staff', ['soft_deleted_by'], ['id'], ondelete='SET NULL')
    op.create_foreign_key('total_grades_created_by_fkey', 'total_grades', 'staff', ['created_by'], ['id'], ondelete='SET NULL')
    op.create_foreign_key('total_grades_student_id_fkey', 'total_grades', 'students', ['student_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('total_grades_last_modified_by_fkey', 'total_grades', 'staff', ['last_modified_by'], ['id'], ondelete='SET NULL')
    op.create_foreign_key('total_grades_subject_id_fkey', 'total_grades', 'subjects', ['subject_id'], ['id'], ondelete='SET NULL')
    op.alter_column('total_grades', 'soft_deleted_by',
               existing_type=sa.UUID(),
               nullable=True)
    op.alter_column('total_grades', 'last_modified_by',
               existing_type=sa.UUID(),
               nullable=True)
    op.alter_column('total_grades', 'created_by',
               existing_type=sa.UUID(),
               nullable=True)
    op.create_foreign_key('support_id_fkey', 'support', 'staff', ['id'], ['id'])
    op.create_foreign_key('subjects_created_by_fkey', 'subjects', 'staff', ['created_by'], ['id'], ondelete='SET NULL')
    op.create_foreign_key('subjects_last_modified_by_fkey', 'subjects', 'staff', ['last_modified_by'], ['id'], ondelete='SET NULL')
    op.create_foreign_key('subjects_soft_deleted_by_fkey', 'subjects', 'staff', ['soft_deleted_by'], ['id'], ondelete='SET NULL')
    op.alter_column('subjects', 'soft_deleted_by',
               existing_type=sa.UUID(),
               nullable=True)
    op.alter_column('subjects', 'last_modified_by',
               existing_type=sa.UUID(),
               nullable=True)
    op.alter_column('subjects', 'created_by',
               existing_type=sa.UUID(),
               nullable=True)
    op.create_foreign_key('students_class_id_fkey', 'students', 'classes', ['class_id'], ['id'], ondelete='RESTRICT')
    op.create_foreign_key('students_profile_id_fkey', 'students', 'users', ['profile_id'], ['profile_id'], ondelete='RESTRICT')
    op.create_foreign_key('students_created_by_fkey', 'students', 'staff', ['created_by'], ['id'], ondelete='SET NULL')
    op.create_foreign_key('students_last_modified_by_fkey', 'students', 'staff', ['last_modified_by'], ['id'], ondelete='SET NULL')
    op.create_foreign_key('students_soft_deleted_by_fkey', 'students', 'staff', ['soft_deleted_by'], ['id'], ondelete='SET NULL')
    op.create_foreign_key('students_department_id_fkey', 'students', 'departments', ['department_id'], ['id'], ondelete='RESTRICT')
    op.create_foreign_key('students_parent_id_fkey', 'students', 'parents', ['parent_id'], ['id'], ondelete='RESTRICT')
    op.create_unique_constraint('students_profile_id_key', 'students', ['profile_id'])
    op.create_index('idx_students_soft_deleted_at', 'students', ['soft_deleted_at'], unique=False)
    op.create_index('idx_students_profile_id', 'students', ['profile_id'], unique=False)
    op.alter_column('students', 'soft_deleted_by',
               existing_type=sa.UUID(),
               nullable=True)
    op.alter_column('students', 'last_modified_by',
               existing_type=sa.UUID(),
               nullable=True)
    op.alter_column('students', 'created_by',
               existing_type=sa.UUID(),
               nullable=True)
    op.create_foreign_key('student_transfers_last_modified_by_fkey', 'student_transfers', 'staff', ['last_modified_by'], ['id'], ondelete='SET NULL')
    op.create_foreign_key('student_transfers_soft_deleted_by_fkey', 'student_transfers', 'staff', ['soft_deleted_by'], ['id'], ondelete='SET NULL')
    op.create_foreign_key('student_transfers_status_updated_by_fkey', 'student_transfers', 'staff', ['status_updated_by'], ['id'], ondelete='SET NULL')
    op.create_foreign_key('student_transfers_student_id_fkey', 'student_transfers', 'students', ['student_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('student_transfers_created_by_fkey', 'student_transfers', 'staff', ['created_by'], ['id'], ondelete='SET NULL')
    op.alter_column('student_transfers', 'soft_deleted_by',
               existing_type=sa.UUID(),
               nullable=True)
    op.alter_column('student_transfers', 'last_modified_by',
               existing_type=sa.UUID(),
               nullable=True)
    op.alter_column('student_transfers', 'created_by',
               existing_type=sa.UUID(),
               nullable=True)
    op.create_foreign_key('student_subjects_last_modified_by_fkey', 'student_subjects', 'staff', ['last_modified_by'], ['id'], ondelete='SET NULL')
    op.create_foreign_key('student_subjects_created_by_fkey', 'student_subjects', 'staff', ['created_by'], ['id'], ondelete='SET NULL')
    op.create_foreign_key('student_subjects_student_id_fkey', 'student_subjects', 'students', ['student_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('student_subjects_soft_deleted_by_fkey', 'student_subjects', 'staff', ['soft_deleted_by'], ['id'], ondelete='SET NULL')
    op.create_foreign_key('student_subjects_subject_id_fkey', 'student_subjects', 'subjects', ['subject_id'], ['id'], ondelete='SET NULL')
    op.alter_column('student_subjects', 'soft_deleted_by',
               existing_type=sa.UUID(),
               nullable=True)
    op.alter_column('student_subjects', 'last_modified_by',
               existing_type=sa.UUID(),
               nullable=True)
    op.alter_column('student_subjects', 'created_by',
               existing_type=sa.UUID(),
               nullable=True)
    op.create_foreign_key('student_documents_owner_id_fkey', 'student_documents', 'students', ['owner_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('student_documents_created_by_fkey', 'student_documents', 'staff', ['created_by'], ['id'], ondelete='SET NULL')
    op.create_foreign_key('student_documents_last_modified_by_fkey', 'student_documents', 'staff', ['last_modified_by'], ['id'], ondelete='SET NULL')
    op.create_foreign_key('student_documents_soft_deleted_by_fkey', 'student_documents', 'staff', ['soft_deleted_by'], ['id'], ondelete='SET NULL')
    op.alter_column('student_documents', 'soft_deleted_by',
               existing_type=sa.UUID(),
               nullable=True)
    op.alter_column('student_documents', 'last_modified_by',
               existing_type=sa.UUID(),
               nullable=True)
    op.alter_column('student_documents', 'created_by',
               existing_type=sa.UUID(),
               nullable=True)
    op.create_foreign_key('staff_roles_last_modified_by_fkey', 'staff_roles', 'staff', ['last_modified_by'], ['id'], ondelete='SET NULL')
    op.create_foreign_key('staff_roles_created_by_fkey', 'staff_roles', 'staff', ['created_by'], ['id'], ondelete='SET NULL')
    op.create_foreign_key('staff_roles_soft_deleted_by_fkey', 'staff_roles', 'staff', ['soft_deleted_by'], ['id'], ondelete='SET NULL')
    op.alter_column('staff_roles', 'soft_deleted_by',
               existing_type=sa.UUID(),
               nullable=True)
    op.alter_column('staff_roles', 'last_modified_by',
               existing_type=sa.UUID(),
               nullable=True)
    op.alter_column('staff_roles', 'created_by',
               existing_type=sa.UUID(),
               nullable=True)
    op.create_foreign_key('staff_departments_manager_id_fkey', 'staff_departments', 'staff', ['manager_id'], ['id'], ondelete='SET NULL')
    op.create_foreign_key('staff_departments_soft_deleted_by_fkey', 'staff_departments', 'staff', ['soft_deleted_by'], ['id'], ondelete='SET NULL')
    op.create_foreign_key('staff_departments_created_by_fkey', 'staff_departments', 'staff', ['created_by'], ['id'], ondelete='SET NULL')
    op.create_foreign_key('staff_departments_last_modified_by_fkey', 'staff_departments', 'staff', ['last_modified_by'], ['id'], ondelete='SET NULL')
    op.alter_column('staff_departments', 'soft_deleted_by',
               existing_type=sa.UUID(),
               nullable=True)
    op.alter_column('staff_departments', 'last_modified_by',
               existing_type=sa.UUID(),
               nullable=True)
    op.alter_column('staff_departments', 'created_by',
               existing_type=sa.UUID(),
               nullable=True)
    op.alter_column('staff_departments', 'manager_id',
               existing_type=sa.UUID(),
               nullable=True)
    op.create_foreign_key('staff_role_id_fkey', 'staff', 'staff_roles', ['role_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('staff_profile_id_fkey', 'staff', 'users', ['profile_id'], ['profile_id'], ondelete='RESTRICT')
    op.create_foreign_key('staff_department_id_fkey', 'staff', 'staff_departments', ['department_id'], ['id'], ondelete='RESTRICT')
    op.create_foreign_key('staff_created_by_fkey', 'staff', 'staff', ['created_by'], ['id'], ondelete='SET NULL')
    op.create_foreign_key('staff_soft_deleted_by_fkey', 'staff', 'staff', ['soft_deleted_by'], ['id'], ondelete='SET NULL')
    op.create_foreign_key('staff_last_modified_by_fkey', 'staff', 'staff', ['last_modified_by'], ['id'], ondelete='SET NULL')
    op.create_unique_constraint('staff_profile_id_key', 'staff', ['profile_id'])
    op.alter_column('staff', 'soft_deleted_by',
               existing_type=sa.UUID(),
               nullable=True)
    op.alter_column('staff', 'last_modified_by',
               existing_type=sa.UUID(),
               nullable=True)
    op.alter_column('staff', 'created_by',
               existing_type=sa.UUID(),
               nullable=True)
    op.create_foreign_key('repetitions_from_class_id_fkey', 'repetitions', 'classes', ['from_class_id'], ['id'], ondelete='SET NULL')
    op.create_foreign_key('repetitions_status_updated_by_fkey', 'repetitions', 'staff', ['status_updated_by'], ['id'], ondelete='SET NULL')
    op.create_foreign_key('repetitions_created_by_fkey', 'repetitions', 'staff', ['created_by'], ['id'], ondelete='SET NULL')
    op.create_foreign_key('repetitions_to_class_id_fkey', 'repetitions', 'classes', ['to_class_id'], ['id'], ondelete='SET NULL')
    op.create_foreign_key('repetitions_soft_deleted_by_fkey', 'repetitions', 'staff', ['soft_deleted_by'], ['id'], ondelete='SET NULL')
    op.create_foreign_key('repetitions_student_id_fkey', 'repetitions', 'students', ['student_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('repetitions_last_modified_by_fkey', 'repetitions', 'staff', ['last_modified_by'], ['id'], ondelete='SET NULL')
    op.alter_column('repetitions', 'soft_deleted_by',
               existing_type=sa.UUID(),
               nullable=True)
    op.alter_column('repetitions', 'last_modified_by',
               existing_type=sa.UUID(),
               nullable=True)
    op.alter_column('repetitions', 'created_by',
               existing_type=sa.UUID(),
               nullable=True)
    op.alter_column('repetitions', 'status_updated_by',
               existing_type=sa.UUID(),
               nullable=True)
    op.alter_column('repetitions', 'to_class_id',
               existing_type=sa.UUID(),
               nullable=True)
    op.alter_column('repetitions', 'from_class_id',
               existing_type=sa.UUID(),
               nullable=True)
    op.create_foreign_key('parents_last_modified_by_fkey', 'parents', 'staff', ['last_modified_by'], ['id'], ondelete='SET NULL')
    op.create_foreign_key('parents_created_by_fkey', 'parents', 'staff', ['created_by'], ['id'], ondelete='SET NULL')
    op.create_foreign_key('parents_profile_id_fkey', 'parents', 'users', ['profile_id'], ['profile_id'], ondelete='RESTRICT')
    op.create_foreign_key('parents_soft_deleted_by_fkey', 'parents', 'staff', ['soft_deleted_by'], ['id'], ondelete='SET NULL')
    op.create_unique_constraint('parents_profile_id_key', 'parents', ['profile_id'])
    op.alter_column('parents', 'soft_deleted_by',
               existing_type=sa.UUID(),
               nullable=True)
    op.alter_column('parents', 'last_modified_by',
               existing_type=sa.UUID(),
               nullable=True)
    op.alter_column('parents', 'created_by',
               existing_type=sa.UUID(),
               nullable=True)
    op.create_foreign_key('management_id_fkey', 'management', 'staff', ['id'], ['id'])
    op.create_foreign_key('grades_student_id_fkey', 'grades', 'students', ['student_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('grades_department_id_fkey', 'grades', 'departments', ['department_id'], ['id'], ondelete='SET NULL')
    op.create_foreign_key('grades_created_by_fkey', 'grades', 'staff', ['created_by'], ['id'], ondelete='SET NULL')
    op.create_foreign_key('grades_soft_deleted_by_fkey', 'grades', 'staff', ['soft_deleted_by'], ['id'], ondelete='SET NULL')
    op.create_foreign_key('grades_graded_by_fkey', 'grades', 'staff', ['graded_by'], ['id'], ondelete='SET NULL')
    op.create_foreign_key('grades_subject_id_fkey', 'grades', 'subjects', ['subject_id'], ['id'], ondelete='SET NULL')
    op.create_foreign_key('grades_last_modified_by_fkey', 'grades', 'staff', ['last_modified_by'], ['id'], ondelete='SET NULL')
    op.alter_column('grades', 'soft_deleted_by',
               existing_type=sa.UUID(),
               nullable=True)
    op.alter_column('grades', 'last_modified_by',
               existing_type=sa.UUID(),
               nullable=True)
    op.alter_column('grades', 'created_by',
               existing_type=sa.UUID(),
               nullable=True)
    op.alter_column('grades', 'department_id',
               existing_type=sa.UUID(),
               nullable=True)
    op.alter_column('grades', 'subject_id',
               existing_type=sa.UUID(),
               nullable=True)
    op.create_foreign_key('educator_subjects_subject_id_fkey', 'educator_subjects', 'subjects', ['subject_id'], ['id'], ondelete='SET NULL')
    op.create_foreign_key('educator_subjects_soft_deleted_by_fkey', 'educator_subjects', 'staff', ['soft_deleted_by'], ['id'], ondelete='SET NULL')
    op.create_foreign_key('educator_subjects_educator_id_fkey', 'educator_subjects', 'educator', ['educator_id'], ['id'], ondelete='SET NULL')
    op.create_foreign_key('educator_subjects_last_modified_by_fkey', 'educator_subjects', 'staff', ['last_modified_by'], ['id'], ondelete='SET NULL')
    op.create_foreign_key('educator_subjects_created_by_fkey', 'educator_subjects', 'staff', ['created_by'], ['id'], ondelete='SET NULL')
    op.alter_column('educator_subjects', 'soft_deleted_by',
               existing_type=sa.UUID(),
               nullable=True)
    op.alter_column('educator_subjects', 'last_modified_by',
               existing_type=sa.UUID(),
               nullable=True)
    op.alter_column('educator_subjects', 'created_by',
               existing_type=sa.UUID(),
               nullable=True)
    op.alter_column('educator_subjects', 'subject_id',
               existing_type=sa.UUID(),
               nullable=True)
    op.create_foreign_key('educator_id_fkey', 'educator', 'staff', ['id'], ['id'])
    op.create_foreign_key('departments_soft_deleted_by_fkey', 'departments', 'staff', ['soft_deleted_by'], ['id'], ondelete='SET NULL')
    op.create_foreign_key('departments_created_by_fkey', 'departments', 'staff', ['created_by'], ['id'], ondelete='SET NULL')
    op.create_foreign_key('departments_mentor_id_fkey', 'departments', 'educator', ['mentor_id'], ['id'], ondelete='SET NULL')
    op.create_foreign_key('departments_last_modified_by_fkey', 'departments', 'staff', ['last_modified_by'], ['id'], ondelete='SET NULL')
    op.alter_column('departments', 'soft_deleted_by',
               existing_type=sa.UUID(),
               nullable=True)
    op.alter_column('departments', 'last_modified_by',
               existing_type=sa.UUID(),
               nullable=True)
    op.alter_column('departments', 'created_by',
               existing_type=sa.UUID(),
               nullable=True)
    op.alter_column('departments', 'mentor_id',
               existing_type=sa.UUID(),
               nullable=True)
    op.create_foreign_key('commercial_id_fkey', 'commercial', 'staff', ['id'], ['id'])
    op.create_foreign_key('classes_last_modified_by_fkey', 'classes', 'staff', ['last_modified_by'], ['id'], ondelete='SET NULL')
    op.create_foreign_key('classes_soft_deleted_by_fkey', 'classes', 'staff', ['soft_deleted_by'], ['id'], ondelete='SET NULL')
    op.create_foreign_key('classes_created_by_fkey', 'classes', 'staff', ['created_by'], ['id'], ondelete='SET NULL')
    op.create_foreign_key('classes_mentor_id_fkey', 'classes', 'educator', ['mentor_id'], ['id'], ondelete='SET NULL')
    op.alter_column('classes', 'soft_deleted_by',
               existing_type=sa.UUID(),
               nullable=True)
    op.alter_column('classes', 'last_modified_by',
               existing_type=sa.UUID(),
               nullable=True)
    op.alter_column('classes', 'created_by',
               existing_type=sa.UUID(),
               nullable=True)
    op.alter_column('classes', 'mentor_id',
               existing_type=sa.UUID(),
               nullable=True)
    op.create_foreign_key('admin_id_fkey', 'admin', 'staff', ['id'], ['id'])
    op.create_foreign_key('access_level_changes_changed_by_fkey', 'access_level_changes', 'staff', ['changed_by'], ['id'], ondelete='SET NULL')
    op.create_foreign_key('access_level_changes_profile_id_fkey', 'access_level_changes', 'users', ['profile_id'], ['profile_id'], ondelete='CASCADE')
    # ### end Alembic commands ###
