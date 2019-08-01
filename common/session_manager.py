from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from common.constants import Constants


class SessionManager(object):
    def __init__(self):
        self.engine = create_engine(Constants.DATABASE_URL, pool_size=1000)
        self.session_factory = sessionmaker(bind=self.engine)
        self.Session = scoped_session(self.session_factory)

    def get_icat_db_session(self):
        """
        Gets a new session in the scoped_session collection
        :return: A new session
        """

        return self.Session()


session_manager = SessionManager()
