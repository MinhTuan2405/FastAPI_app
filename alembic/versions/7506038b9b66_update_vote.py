"""update vote

Revision ID: 7506038b9b66
Revises: dda2536c9428
Create Date: 2024-08-08 20:42:29.790653

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7506038b9b66'
down_revision: Union[str, None] = 'dda2536c9428'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column ('votes', sa.Column ('vote_id', sa.Integer (), nullable = False))
    pass


def downgrade() -> None:
    op.drop_column ('votes', 'vote_id')
    pass
