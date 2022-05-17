import sys
from os import listdir
from os.path import join, abspath, dirname

import face_recognition
from PIL import Image

import utils
from tests import test_suite


def main() -> None:
    """Runs all tests
    """
<<<<<<< HEAD

    args = utils.cli_parser()

    for image_name in listdir(join(IMAGE_PATH, IN)):

        utils.change_image_format(join(IMAGE_PATH, IN, image_name))

        image = face_recognition.load_image_file(join(IMAGE_PATH, IN, image_name))
        face_locations = face_recognition.face_locations(image)

        pil_image = Image.fromarray(image)

        if args.blur:
            pil_image = utils.apply_blur_mask(pil_image, face_locations)
            try:
                pil_image.save(join(IMAGE_PATH, OUT, image_name))
            except FileNotFoundError as error:
                print(error)
=======
    ROOT = dirname(abspath(r"./static"))
    _ = utils.cli_parser() # Useless for now
    suite = test_suite.TestSuite(logger_config_path=join(ROOT, r'src/logger_config.json'))
    suite.run()
>>>>>>> e402a689e8d471bb0c6beb3bb84f214518af3c1d

if __name__ == "__main__":
    sys.exit(main())
