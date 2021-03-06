from sqlalchemy import Table, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import mapper, relation, relationship, backref
from database import Base, ImposterBase
from time import strftime
from config import TABLEPREFIX
from flaskjk import markup_to_html, multi_replace

def tn(tablename):
    """ shortcut to get tablename with prefix """
    return '%s%s' % (TABLEPREFIX, tablename)

post_tags = Table(tn('post_tags'), Base.metadata,
             Column('post_id', Integer, ForeignKey('%s.id' % tn('posts'))),
             Column('tag_id', Integer, ForeignKey('%s.id' % tn('tags')))
             )

class Status(Base,ImposterBase):
    __tablename__ = tn('status')

    id = Column(Integer, primary_key=True)
    value = Column(String(32), unique=True)

    __public_columns__ = [ value ]

    def __init__(self, value):
        self.value = value

    def __unicode__(self):
        return self.value

    def __repr__(self):
        return '<Status %r>' % self.value

class Format(Base,ImposterBase):
    __tablename__ = tn('formats')
    id = Column(Integer, primary_key=True)
    value = Column(String(32), nullable=False, unique=True)

    __public_columns__ = [ value ]

    def __init__(self, value):
        self.value = value

    def __unicode__(self):
        return self.value

    def __repr__(self):
        return '<Format %r>' % self.value

class Tag(Base,ImposterBase):
    __tablename__ = tn('tags')

    id = Column(Integer, primary_key=True)
    value = Column(String(64), nullable=False, unique=True)
    count = Column(Integer, default=0)

    __public_columns__ = [ value, count ]

    def __init__(self, value):
        self.value = value

    def __unicode__(self):
        return self.value

    def __repr__(self):
        return '<Tag %r>' % self.value

class User(Base,ImposterBase):
    __tablename__ = tn('users')

    id = Column(Integer, primary_key=True)
    username = Column(String(64), nullable=False, unique=True)
    password = Column(String(256), nullable=False)

    __public_columns__ = [ username ]

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __unicode__(self):
        return self.username

    def __repr__(self):
        return '<User %r>' % self.username

class Post(Base,ImposterBase):
    __tablename__ = tn('posts')

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    slug = Column(String(128), nullable=False)
    summary = Column(Text, nullable=True)
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

    summary_html = Column(Text, nullable=True)
    content_html = Column(Text, nullable=True)

    __public_columns__ = [ title, slug, summary_html, content_html, pubdate, lastmoddate, tags ]

    def __init__(self, title=None, summary=None, content=None, createdate=None, pubdate=None, lastmoddate=None):
        self.title = title
        self.summary = summary
        self.content = content
        self.createdate = createdate
        self.pubdate = pubdate
        self.lastmoddate = lastmoddate

    def compile(self, repl=None):
        input_summary = self.summary
        input_content = self.content
        if repl is not None:
            input_summary = multi_replace(input_summary, repl)
            input_content = multi_replace(input_content, repl)

        self.summary_html = markup_to_html(self.format, input_summary)
        self.content_html = markup_to_html(self.format, input_content)

    def __repr__(self):
        return '<Post %s>' % self.title

    @property
    def year(self):
        return self.pubdate.year

    @property
    def month(self):
        return '%02d' % self.pubdate.month

    @property
    def day(self):
        return '%02d' % self.pubdate.day

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

    status = relationship(Status, backref='pages')
    user = relationship(User, backref='pages')
    format = relationship(Format, backref='pages')

    __public_columns__ = [ title, slug, content_html, pubdate, lastmoddate ]

    def __init__(self, title=None, content=None, createdate=None, pubdate=None, lastmoddate=None):
        self.title = title
        self.content = content
        self.createdate = createdate
        self.pubdate = pubdate
        self.lastmoddate = lastmoddate

    def compile(self, repl=None):
        input_content = self.content
        if repl is not None:
            input_content = multi_replace(input_content, repl)

        self.content_html = markup_to_html(self.format, input_content)

    def __repr__(self):
        return '<Page %s>' % self.title

