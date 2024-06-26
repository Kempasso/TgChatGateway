"""fix models1

Revision ID: 57de6c033255
Revises: edf0019ea105
Create Date: 2024-05-19 17:04:05.662099

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '57de6c033255'
down_revision: Union[str, None] = 'edf0019ea105'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("ALTER TABLE chat ALTER COLUMN chat_id TYPE INTEGER USING chat_id::integer")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('chat', 'chat_id',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(),
               existing_nullable=True)
    # ### end Alembic commands ###
