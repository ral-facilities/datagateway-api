import json
import logging
from pathlib import Path
import sys

import requests


log = logging.getLogger()


class Config(object):
    def __init__(self):
        config_path = Path(__file__).parent.parent.parent / "config.json"
        with open(config_path) as target:

            self.config = json.load(target)
        target.close()

    def get_backend_type(self):
        try:
            return self.config["backend"]
        except:
            sys.exit("Missing config value, backend")

    def get_db_url(self):
        try:
            return self.config["DB_URL"]
        except:
            sys.exit("Missing config value, DB_URL")

    def get_icat_url(self):
        try:
            return self.config["ICAT_URL"]
        except:
            sys.exit("Missing config value, ICAT_URL")

    def get_icat_check_cert(self):
        try:
            return self.config["icat_check_cert"]
        except:
            # This could be set to true if there's no value, and log a warning
            # that no value has been found from the config - save app from
            # exiting
            sys.exit("Missing config value, icat_check_cert")

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

    def get_host(self):
        try:
            return self.config["host"]
        except:
            sys.exit("Missing config value, host")

    def get_port(self):
        try:
            return self.config["port"]
        except:
            sys.exit("Missing config value, port")

    def get_icat_properties(self):
        """
        ICAT properties can be retrieved using Python ICAT's client object, however this
        requires the client object to be authenticated which may not always be the case
        when requesting these properties, hence a HTTP request is sent as an alternative
        """
        properties_url = f"{config.get_icat_url()}/icat/properties"
        r = requests.request("GET", properties_url, verify=config.get_icat_check_cert())
        icat_properties = r.json()

        return icat_properties


config = Config()
