from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "4c5581bb3c72"           # <- usa el del nombre del archivo
down_revision = "9e5dfda8a6f1"       # <- la última aplicada (de paso 1)
branch_labels = None
depends_on = None

def upgrade():
    op.create_unique_constraint(
        "uq_plan_day_user_fecha",
        "plan_day",
        ["user_id", "fecha"]
    )

def downgrade():
    op.drop_constraint(
        "uq_plan_day_user_fecha",
        "plan_day",
        type_="unique"
    )
