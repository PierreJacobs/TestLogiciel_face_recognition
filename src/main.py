import sys
from os import listdir
from os.path import join, abspath, dirname

import face_recognition
from PIL import Image

import utils

ROOT = dirname(abspath(r"./static"))
IMAGE_PATH = join(ROOT, r"static/img")
IN = r'in'
OUT = r'out'

def main() -> None:
    """Runs an example
    """

    args = utils.cli_parser()

    for image_name in listdir(join(IMAGE_PATH, IN)):

        image = face_recognition.load_image_file(join(IMAGE_PATH, IN, image_name))
        face_locations = face_recognition.face_locations(image)

        pil_image = Image.fromarray(image)

        if args.blur:
            pil_image = utils.apply_blur_mask(pil_image, face_locations)
            try:
                pil_image.save(join(IMAGE_PATH, OUT, image_name))
            except FileNotFoundError as error:
                print(error)

if __name__ == "__main__":
    sys.exit(main())
