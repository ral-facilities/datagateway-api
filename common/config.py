import json
import sys
from pathlib import Path


class Config(object):

    def __init__(self):
        with open(Path("config.json")) as target:
            self.config = json.load(target)
        target.close()

    def get_db_url(self):
        try:
            return self.config["DB_URL"]
        except:
            sys.exit("Missing config value, DB_URL")

    def get_log_level(self):
        try:
            return self.config["log_level"]
        except:
            sys.exit("Missing config value, log_level")

    def is_debug_mode(self):
        try:
            return self.config["debug_mode"]
        except:
            sys.exit("Missing config value, debug_mode")

    def is_generate_swagger(self):
        try:
            return self.config["generate_swagger"]
        except:
            sys.exit("Missing config value, generate_swagger")

config = Config()
