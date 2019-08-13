from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import QueuePool

from common.constants import Constants

engine = create_engine(Constants.DATABASE_URL, poolclass=QueuePool, pool_size=100, max_overflow=0)
session_factory = sessionmaker(engine)


class SessionManager(object):

    def __init__(self):
        self.Session = scoped_session(session_factory)

    def get_icat_db_session(self):
        """
        Gets a new session in the scoped_session collection
        :return: A new session
        """

        return self.Session()


session_manager = SessionManager()
