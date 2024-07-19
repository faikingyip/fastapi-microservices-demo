"""Added transaction status field

Revision ID: 262737e8685f
Revises: 266b5707860f
Create Date: 2024-07-19 09:03:39.926639

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '262737e8685f'
down_revision: Union[str, None] = '266b5707860f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transaction', sa.Column('status', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('transaction', 'status')
    # ### end Alembic commands ###