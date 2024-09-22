"""first alembic

Revision ID: 57a6a12c39b2
Revises: 5379d73b2cd1
Create Date: 2024-09-22 06:15:02.499826

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '57a6a12c39b2'
down_revision: Union[str, None] = '5379d73b2cd1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
