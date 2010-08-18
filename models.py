from sqlalchemy import Table, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import mapper, relation, relationship, backref
from database import DB
from helpers import tn
from time import strftime

import config as cfg

db = DB(cfg.FRONTEND_DATABASE)
Base = db.get_base()

post_tags = Table(tn('post_tags'), Base.metadata,
             Column('post_id', Integer, ForeignKey('%s.id' % tn('posts'))),
             Column('tag_id', Integer, ForeignKey('%s.id' % tn('tags')))
             )

class Status(Base):
    __tablename__ = tn('status')

    id = Column(Integer, primary_key=True)
    value = Column(String(32), unique=True)

    def __init__(self, value):
        self.value = value

    def __unicode__(self):
        return self.value

    def __repr__(self):
        return '<Status %r>' % self.value

class Format(Base):
    __tablename__ = tn('formats')
    id = Column(Integer, primary_key=True)
    value = Column(String(32), nullable=False, unique=True)

    def __init__(self, value):
        self.value = value

    def __unicode__(self):
        return self.value

    def __repr__(self):
        return '<Format %r>' % self.value

class Tag(Base):
    __tablename__ = tn('tags')

    id = Column(Integer, primary_key=True)
    value = Column(String(64), nullable=False, unique=True)

    def __init__(self, value):
        self.value = value

    def __unicode__(self):
        return self.value

    def __repr__(self):
        return '<Tag %r>' % self.value

class User(Base):
    __tablename__ = tn('users')

    id = Column(Integer, primary_key=True)
    username = Column(String(64), nullable=False, unique=True)
    password = Column(String(256), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __unicode__(self):
        return self.username

    def __repr__(self):
        return '<User %r>' % self.username

class Post(Base):
    __tablename__ = tn('posts')

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    slug = Column(String(128), nullable=False)
    content = Column(Text, nullable=False)
    status_id = Column(Integer, ForeignKey(Status.id), nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    format_id = Column(Integer, ForeignKey(Format.id), nullable=False)

    createdate = Column(DateTime, nullable=False)
    pubdate = Column(DateTime, nullable=True)
    lastmoddate = Column(DateTime, nullable=False)

    status = relationship(Status, backref='posts')
    user = relationship(User, backref='posts')
    tags = relationship('Tag', secondary=post_tags, backref='posts')
    format = relationship(Format, backref='posts')

    def __init__(self, title=None, content=None, createdate=None, pubdate=None, lastmoddate=None):
        self.title = title
        self.content = content
        self.createdate = createdate
        self.pubdate = pubdate
        self.lastmoddate = lastmoddate

    def __repr__(self):
        return '<Post %s>' % self.title
