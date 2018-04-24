"""empty message

Revision ID: 7a3d83e77e03
Revises: 
Create Date: 2018-02-17 01:34:05.862170

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7a3d83e77e03'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('cidades')
    op.add_column('imoveis', sa.Column('endereco', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('imoveis', 'endereco')
    op.create_table('cidades',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('cidade', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name=u'cidades_pkey'),
    sa.UniqueConstraint('cidade', name=u'cidades_cidade_key')
    )
    # ### end Alembic commands ###