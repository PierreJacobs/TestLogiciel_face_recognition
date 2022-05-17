import sys
from os.path import join, abspath, dirname

import utils
from tests import test_suite
from tests.metamorphic_tests import test_color_mode

def main() -> None:
    """Runs all tests
    """
    ROOT = dirname(abspath(__file__))

    args = utils.cli_parser()
    if args.blur:
        utils.blur_images(
            src=join(ROOT, r'img_mistakes'),
            dest=join(ROOT, r'img_mistakes_blur')    
        )
        return

    suite = test_suite.TestSuite(
        test_color_mode.suite(), 
        logger_config_path=join(ROOT, r'logger_config.json')
    )
    suite.run()

if __name__ == "__main__":
    sys.exit(main())
