import json
import sys
import unittest
import logging, logging.config

from os import chdir, getcwd
from os.path import dirname, join, realpath

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

def main() -> None:
    """Creates and runs a test suite
    """
    chdir(dirname(realpath(__file__)))

    logger = logging.getLogger()
    logging.config.dictConfig(
        load_logger_config(r'logger_config.json')
    )
    logger.debug("Hello world!")

if __name__ == "__main__":
    sys.exit(main())