"""create population data table

Revision ID: 8866e53e286b
Revises: bff2ba2df7b3
Create Date: 2025-06-02 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8866e53e286b'
down_revision: Union[str, None] = 'bff2ba2df7b3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'population_statistics',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('administrative_code', sa.String(length=20), nullable=False),
        sa.Column('reference_date', sa.Date(), nullable=False),
        sa.Column('province', sa.String(length=20), nullable=False),
        sa.Column('city', sa.String(length=20), nullable=False),
        sa.Column('district', sa.String(length=20), nullable=False),
        # Age groups - Male
        sa.Column('age_0_9_male', sa.Integer(), nullable=False),
        sa.Column('age_10_19_male', sa.Integer(), nullable=False),
        sa.Column('age_20_29_male', sa.Integer(), nullable=False),
        sa.Column('age_30_39_male', sa.Integer(), nullable=False),
        sa.Column('age_40_49_male', sa.Integer(), nullable=False),
        sa.Column('age_50_59_male', sa.Integer(), nullable=False),
        sa.Column('age_60_69_male', sa.Integer(), nullable=False),
        sa.Column('age_70_79_male', sa.Integer(), nullable=False),
        sa.Column('age_80_89_male', sa.Integer(), nullable=False),
        sa.Column('age_90_99_male', sa.Integer(), nullable=False),
        sa.Column('age_100_plus_male', sa.Integer(), nullable=False),
        # Age groups - Female
        sa.Column('age_0_9_female', sa.Integer(), nullable=False),
        sa.Column('age_10_19_female', sa.Integer(), nullable=False),
        sa.Column('age_20_29_female', sa.Integer(), nullable=False),
        sa.Column('age_30_39_female', sa.Integer(), nullable=False),
        sa.Column('age_40_49_female', sa.Integer(), nullable=False),
        sa.Column('age_50_59_female', sa.Integer(), nullable=False),
        sa.Column('age_60_69_female', sa.Integer(), nullable=False),
        sa.Column('age_70_79_female', sa.Integer(), nullable=False),
        sa.Column('age_80_89_female', sa.Integer(), nullable=False),
        sa.Column('age_90_99_female', sa.Integer(), nullable=False),
        sa.Column('age_100_plus_female', sa.Integer(), nullable=False),
        # Totals
        sa.Column('total_population', sa.Integer(), nullable=False),
        sa.Column('total_male', sa.Integer(), nullable=False),
        sa.Column('total_female', sa.Integer(), nullable=False),
    )
    # Create index for faster queries
    op.create_index(
        'ix_population_statistics_reference_date',
        'population_statistics',
        ['reference_date']
    )
    op.create_index(
        'ix_population_statistics_administrative_code',
        'population_statistics',
        ['administrative_code']
    )


def downgrade() -> None:
    op.drop_index('ix_population_statistics_reference_date')
    op.drop_index('ix_population_statistics_administrative_code')
    op.drop_table('population_statistics')
