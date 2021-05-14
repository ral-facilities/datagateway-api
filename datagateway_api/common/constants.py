from datetime import datetime

from dateutil.tz import tzlocal


class Constants:
    PYTHON_ICAT_DISTNCT_CONDITION = "!= null"
    TEST_MOD_CREATE_DATETIME = datetime(2000, 1, 1, tzinfo=tzlocal())
