"""create file metadata table

Revision ID: 8de086d19461
Revises: 
Create Date: 2026-05-06 13:35:34.997243

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8de086d19461'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE file_informations(
        uuid UUID PRIMARY KEY,
        file_name TEXT NOT NULL,
        file_size_bytes BIGINT,
        download_number INTEGER NOT NULL DEFAULT 0,
        uploaded_at TIMESTAMPTZ NOT NULL DEFAULT now()
    );           
    """)

def downgrade() -> None:
    op.execute("""
               DROP TABLE IF EXISTS file_informations;
    """)
