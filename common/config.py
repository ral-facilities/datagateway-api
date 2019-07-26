import json


class Config(object):

    def __init__(self):
        with open("../config.json") as target:
            self.config = json.load(target)
        target.close()

    def get_db_url(self):
        return self.config["DB_URL"]

    def get_log_level(self):
        return self.config["log_level"]

    def is_debug_mode(self):
        return self.config["debug_mode"]


config = Config()
