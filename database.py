from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, class_mapper
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class DB(object):
    engine = None
    db_session = None

    def __init__(self, dbstring):
        self.engine = create_engine(dbstring, convert_unicode=True)
        self.db_session = scoped_session(sessionmaker(autocommit=False,
                                                 autoflush=False,
                                                 bind=self.engine))
        Base.query = self.db_session.query_property()

    def get_session(self):
        return self.db_session

class ImposterBase(object):
    """ Mixin class to provide additional generic functions for the sqlalchemy models """

    def to_dict(obj):
        """Return dict containing all object data"""
        return dict((col.name, unicode(getattr(obj, col.name)))
                    for col in class_mapper(obj.__class__).mapped_table.c)

    def get_public_dict(obj):
        """Return dict containing only public object data"""
        return dict((col.name, unicode(getattr(obj, col.name)))
                    for col in obj.__class__.__public_columns__)
