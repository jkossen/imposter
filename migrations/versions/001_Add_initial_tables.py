from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from migrate import *
from models import tn

Base = declarative_base()
meta = Base.metadata

# post_tags = Table(tn('post_tags'), meta,
#                   Column('post_id', Integer, ForeignKey('%s.id' % tn('posts'))),
#                   Column('tag_id', Integer, ForeignKey('%s.id' % tn('tags'))),
#                   )

# users = Table(tn('users'), meta,
#              Column('id', Integer, primary_key=True),
#              Column('username', String(64), nullable=False, unique=True),
#              Column('password', String(256), nullable=False)
#              )

# posts = Table(tn('posts'), meta,
#               Column('id', Integer, primary_key=True),
#               Column('title', String(200), unique=True, nullable=False),
#               Column('content', Text, nullable=False),
#               Column('status_id', Integer, ForeignKey('%s.id' % tn('status')), nullable=False),
#               Column('user_id', Integer, ForeignKey('%s.id' % tn('users')), nullable=False),
#               Column('format_id', Integer, ForeignKey('%s.id' % tn('formats')), nullable=False),
#               Column('createdate', DateTime, nullable=False),
#               Column('pubdate', DateTime, nullable=True),
#               Column('lastmoddate', DateTime, nullable=False),
#               )

# status = Table(tn('status'), meta,
#                Column('id', Integer, primary_key=True),
#                Column('value', String(32), unique=True),
#                )

# tags = Table(tn('tags'), meta,
#                Column('id', Integer, primary_key=True),
#                Column('value', String(64), unique=True),
#                )

# formats = Table(tn('format'), meta,
#                Column('id', Integer, primary_key=True),
#                Column('value', String(32), unique=True),
#                )

class Status(Base):
    __tablename__ = tn('status')

    id = Column(Integer, primary_key=True)
    value = Column(String(32), unique=True)

class Format(Base):
    __tablename__ = tn('formats')
    id = Column(Integer, primary_key=True)
    value = Column(String(32), nullable=False, unique=True)

class Tag(Base):
    __tablename__ = tn('tags')

    id = Column(Integer, primary_key=True)
    value = Column(String(64), nullable=False, unique=True)

class User(Base):
    __tablename__ = tn('users')

    id = Column(Integer, primary_key=True)
    username = Column(String(64), nullable=False, unique=True)
    password = Column(String(256), nullable=False)

class Post(Base):
    __tablename__ = tn('posts')

    id = Column(Integer, primary_key=True)
    title = Column(String(200), unique=True, nullable=False)
    slug = Column(String(128), unique=True, nullable=False)
    content = Column(Text, nullable=False)
    status_id = Column(Integer, ForeignKey(Status.id), nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    format_id = Column(Integer, ForeignKey(Format.id), nullable=False)

    createdate = Column(DateTime, nullable=False)
    pubdate = Column(DateTime, nullable=True)
    lastmoddate = Column(DateTime, nullable=False)

post_tags = Table(tn('post_tags'), meta,
                  Column('post_id', Integer, ForeignKey(Post.id)),
                  Column('tag_id', Integer, ForeignKey(Tag.id)),
                  )

def upgrade(migrate_engine):
    meta.bind = migrate_engine
    # Upgrade operations go here. Don't create your own engine; bind migrate_engine
    # to your metadata

    Status.__table__.create()
    Format.__table__.create()
    Tag.__table__.create()
    User.__table__.create()
    Post.__table__.create()
    post_tags.create()

    # status.create()
    # formats.create()
    # tags.create()
    # users.create()
    # post_tags.create()

def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    meta.bind = migrate_engine
    # post_tags.drop()
    # users.drop()
    # status.drop()
    # formats.drop()
    # tags.drop()

    post_tags.drop()
    Post.__table__.drop()
    User.__table__.drop()
    Tag.__table__.drop()
    Format.__table__.drop()
    Status.__table__.drop()
