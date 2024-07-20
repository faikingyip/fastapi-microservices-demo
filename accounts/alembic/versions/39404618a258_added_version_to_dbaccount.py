"""Added version to DbAccount

Revision ID: 39404618a258
Revises: a13d0d3253d8
Create Date: 2024-07-19 15:41:40.895046

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '39404618a258'
down_revision: Union[str, None] = 'a13d0d3253d8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'account', ['user_id', 'version'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'account', type_='unique')
    # ### end Alembic commands ###