from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import config as cfg

class DB(object):
    engine = None
    db_session = None
    Base = declarative_base()

    def __init__(self, dbstring):
        self.engine = create_engine(dbstring, convert_unicode=True)
        self.db_session = scoped_session(sessionmaker(autocommit=False,
                                                 autoflush=False,
                                                 bind=self.engine))
        self.Base.query = self.db_session.query_property()

    def get_session(self):
        return self.db_session

    def get_base(self):
        return self.Base
