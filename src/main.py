import sys
from os import listdir
from os.path import join, abspath, dirname

import face_recognition
from PIL import Image

import utils
from tests import test_suite

ROOT = dirname(abspath(r"./static"))
IMAGE_PATH = join(ROOT, r"static/img")
IN = r'in'
OUT = r'out'

def main() -> None:
    """Runs all tests
    """

    _ = utils.cli_parser() # Useless for now
    suite = test_suite.TestSuite(logger_config_path=join(ROOT, r'src/logger_config.json'))
    suite.run()

if __name__ == "__main__":
    sys.exit(main())
