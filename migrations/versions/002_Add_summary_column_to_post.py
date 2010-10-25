from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from migrate import *
from models import tn
import migrate.changeset

Base = declarative_base()
meta = Base.metadata

def upgrade(migrate_engine):
    meta.bind = migrate_engine
    post = Table(tn('posts'), meta, autoload=True)
    summary = Column('summary', Text, nullable=True)
    summary.create(post)

def downgrade(migrate_engine):
    meta.bind = migrate_engine
    post = Table(tn('posts'), meta, autoload=True)
    summary = Column('summary', Text, nullable=True)
    summary.drop(post)

