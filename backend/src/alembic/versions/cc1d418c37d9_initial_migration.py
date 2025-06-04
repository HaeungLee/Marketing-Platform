"""initial migration

Revision ID: cc1d418c37d9
Revises: 
Create Date: 2025-05-31 15:04:11.746008

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'cc1d418c37d9'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('uuid', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('id', sa.String(length=36), unique=True, nullable=False),
        sa.Column('email', sa.String(), unique=True, nullable=False, index=True),
        sa.Column('username', sa.String(length=50), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('user_type', sa.Enum('PERSONAL', 'BUSINESS', name='usertype'), nullable=False),
        sa.Column('phone', sa.String(length=20), nullable=True),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('created_at', sa.DateTime(), default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), default=sa.func.now(), onupdate=sa.func.now()),
        sa.Column('social_provider', sa.String(), nullable=True),
        sa.Column('social_id', sa.String(), nullable=True),
    )
    op.create_table(
        'email_verifications',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('code', sa.String(), nullable=False),
        sa.Column('verified', sa.Boolean(), nullable=True),
        sa.Column('verified_at', sa.DateTime(), nullable=True),
        sa.Column('expires_at', sa.DateTime(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_email_verifications_email'), 'email_verifications', ['email'], unique=False)
    op.create_table(
        'password_resets',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('users_id', sa.String(length=36), nullable=False),
        sa.Column('token', sa.String(), nullable=False),
        sa.Column('used', sa.Boolean(), nullable=True),
        sa.Column('used_at', sa.DateTime(), nullable=True),
        sa.Column('expires_at', sa.DateTime(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['users_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('token')
    )


def downgrade() -> None:
    op.drop_table('password_resets')
    op.drop_index(op.f('ix_email_verifications_email'), table_name='email_verifications')
    op.drop_table('email_verifications')
    op.drop_table('users')
