from flask import Flask
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from migrate import *
from models import Post, Status, Tag, post_tags, tn
import migrate.changeset

Base = declarative_base()
meta = Base.metadata

count = Column('count', Integer, default=0)

def upgrade(migrate_engine):
    meta.bind = migrate_engine
    tags = Table(tn('tags'), meta, autoload=True)
    count.create(tags)

def downgrade(migrate_engine):
    meta.bind = migrate_engine
    tags = Table(tn('tags'), meta, autoload=True)
    count.drop(tags)

