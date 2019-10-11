"""empty message

Revision ID: 7b537a3c7804
Revises: 64acf0eecad5
Create Date: 2017-07-23 00:10:07.076000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7b537a3c7804'
down_revision = '64acf0eecad5'
branch_labels = None
depends_on = None




def upgrade():
    # op.create_table('menuorder',
    # sa.Column('id', sa.Integer(), nullable=False),
    # sa.Column('order_id', sa.String(length = 10), nullable=False),
    # sa.Column('user_id', sa.Integer(), nullable=False),
    # sa.Column('payment_id', sa.Integer(), nullable=False),
    # sa.Column('address_id', sa.Integer(), nullable=False),
    # sa.Column('promo_code', sa.String(length = 10), nullable = True),
    # sa.Column('special_note', sa.String(length = 100), nullable = True),
    # sa.Column('ratings', sa.Integer(), nullable = True),
    # sa.ForeignKeyConstraint(['promo_code'], ['promocode.promo_code'], ),
    # sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    # sa.ForeignKeyConstraint(['payment_id'], ['payment.id']),
    # sa.ForeignKeyConstraint(['address_id'], ['users_address.id']),
    # sa.PrimaryKeyConstraint('id')
    # )

    # op.create_table('menuorderitems',
    # sa.Column('id', sa.Integer(), nullable = False),
    # sa.Column('order_no', sa.Integer(), nullable = False),
    # sa.Column('menu_item_id', sa.Integer(), nullable = False),
    # sa.Column('menu_amount', sa.Integer(), nullable = False),
    # sa.Column('choice', sa.Integer(), nullable = False),
    # sa.ForeignKeyConstraint(['order_no'],['menuorder.id']),
    # sa.ForeignKeyConstraint(['menu_item_id'], ['menuitem.id']),
    # sa.PrimaryKeyConstraint('id')
    # )
    pass


def downgrade():
	# op.drop_table('menuorder'),
	# op.drop_table('menuorderitems')
	pass
    
