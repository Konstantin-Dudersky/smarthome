"""entity_table

Revision ID: 24ae55f84c58
Revises: 
Create Date: 2022-10-18 20:24:33.403976

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "24ae55f84c58"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "entity",
        sa.Column("entity_id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("entity_id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("entity")
    # ### end Alembic commands ###
