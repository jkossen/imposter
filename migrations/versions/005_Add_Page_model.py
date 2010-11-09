from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from migrate import *
from models import tn

Base = declarative_base()
meta = Base.metadata

class Status(Base):
    __tablename__ = tn('status')

    id = Column(Integer, primary_key=True)
    value = Column(String(32), unique=True)

class Format(Base):
    __tablename__ = tn('formats')
    id = Column(Integer, primary_key=True)
    value = Column(String(32), nullable=False, unique=True)

class User(Base):
    __tablename__ = tn('users')

    id = Column(Integer, primary_key=True)
    username = Column(String(64), nullable=False, unique=True)
    password = Column(String(256), nullable=False)

class Page(Base):
    __tablename__ = tn('pages')

    id = Column(Integer, primary_key=True)
    title = Column(String(200), unique=True, nullable=False)
    slug = Column(String(128), unique=True, nullable=False)
    content = Column(Text, nullable=False)
    status_id = Column(Integer, ForeignKey(Status.id), nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    format_id = Column(Integer, ForeignKey(Format.id), nullable=False)
    content_html = Column(Text, nullable=True)

    createdate = Column(DateTime, nullable=False)
    pubdate = Column(DateTime, nullable=True)
    lastmoddate = Column(DateTime, nullable=False)

def upgrade(migrate_engine):
    meta.bind = migrate_engine
    # Upgrade operations go here. Don't create your own engine; bind migrate_engine
    # to your metadata

    Page.__table__.create()

def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    meta.bind = migrate_engine

    Page.__table__.drop()
