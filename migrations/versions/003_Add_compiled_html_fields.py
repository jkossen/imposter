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
    content_html = Column('content_html', Text, nullable=True)
    content_html.create(post)
    summary_html = Column('summary_html', Text, nullable=True)
    summary_html.create(post)

def downgrade(migrate_engine):
    meta.bind = migrate_engine
    post = Table(tn('posts'), meta, autoload=True)
    content_html = Column('content_html', Text, nullable=True)
    content_html.drop(post)
    summary_html = Column('summary_html', Text, nullable=True)
    summary_html.drop(post)
