import json
import unittest
import logging, logging.config

from os import chdir
from os.path import dirname, realpath

def load_logger_config(path: str) -> dict:
    """Loads the json config for the logger

    :param path: path to config
    :type path: str

    :return: loaded dict
    :rtype: dict
    """

    assert path.endswith(".json"), "Invalid config file"

    dict_config = {}

    try:
        with open(path, 'r') as f:
            dict_config = json.load(f)
    
    except json.JSONDecodeError as error:
        print(error)
        print("Using empty dict")

    except FileNotFoundError as error:
        print(error)
        print("Using empty dict")
    
    return dict_config

class TestSuite():

    def __init__(self, *suite_callbacks, logger_config_path: str, **kwargs) -> None:
        self.suite = suite_callbacks
        
        self.logger = logging.getLogger()
        chdir(dirname(realpath(__file__)))
        logging.config.dictConfig(load_logger_config(logger_config_path))

        self.logger.info("Created a new Test Suite")
        self.logger.debug(f"Using {self.suite=}")

    def run(self) -> None:
        runner=unittest.TextTestRunner()
        for test in self.suite:
            runner.run(test)
