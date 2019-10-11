"""empty message

Revision ID: a3d085b190d2
Revises: af04c707c571
Create Date: 2017-07-22 21:47:24.240000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a3d085b190d2'
down_revision = 'af04c707c571'
branch_labels = None
depends_on = None


def upgrade():

    op.create_table('payment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('payment_type', sa.String(length=2), nullable=False),
    sa.Column('transaction_id', sa.String(length = 12), nullable = False),
    sa.Column('date_time_of_payment', sa.Date(), nullable = False),
    sa.Column('amount', sa.Integer(), nullable = False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('taxes',
    sa.Column('id', sa.Integer(), nullable = False),
    sa.Column('tax_name', sa.String(length = 15), nullable = False),
    sa.Column('tax_per', sa.Integer(), nullable = False),
    sa.PrimaryKeyConstraint('id')
    )

    


def downgrade():
	op.drop_table('payment'),
	op.drop_table('taxes')
   
