from datetime import datetime

from datagateway_api.common.config import config


class Constants:
    DATABASE_URL = config.get_db_url()
    PYTHON_ICAT_DISTNCT_CONDITION = "!= null"
    ICAT_PROPERTIES = config.get_icat_properties()
    TEST_MOD_CREATE_DATETIME = datetime(2000, 1, 1)
