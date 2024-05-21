"""fix models1

Revision ID: b2d30c78c0cc
Revises: e3e1033b76ac
Create Date: 2024-05-20 01:36:40.016043

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b2d30c78c0cc'
down_revision: Union[str, None] = 'e3e1033b76ac'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('chat_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'user', 'chat', ['chat_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.drop_column('user', 'chat_id')
    # ### end Alembic commands ###
