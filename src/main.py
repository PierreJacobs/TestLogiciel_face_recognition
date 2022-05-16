import sys
from os import listdir
from os.path import join, abspath, dirname

import face_recognition
from PIL import Image, ImageDraw, ImageFilter

ROOT = dirname(abspath(r"./static"))
IMAGE_PATH = join(ROOT, r"static/img")
IN = r'in'
OUT = r'out'

def apply_blur_mask(pil_image: Image, face_locations, /, radius=50) -> Image:
    """Applies a blur mask at given locations

    :param pil_image: PIL image
    :type pil_image: Image

    :param face_locations: locations of faces on `pil_image`
    :type face_locations: nympy[ndarray]

    :param radius: blur radius, defaults to 50
    :type radius: int, optional

    :return: blurred image
    :rtype: Image
    """
    for (top, right, bottom, left) in face_locations:
        cropped_image = pil_image.crop((left, top, right, bottom))
        c_i_size = cropped_image.size

        mask = Image.new("L", c_i_size, 0)
        draw = ImageDraw.Draw(mask)
        draw.pieslice((0, 0, c_i_size[0], c_i_size[1]), 0, 360, fill=255)

        blurred_image = cropped_image.filter(ImageFilter.GaussianBlur(radius=radius))
        cropped_image.paste(blurred_image, mask=mask)
        pil_image.paste(cropped_image, (left, top, right, bottom))

    return pil_image

def main() -> None:
    """Runs an example
    """

    for image_name in listdir(join(IMAGE_PATH, IN)):

        image = face_recognition.load_image_file(join(IMAGE_PATH, IN, image_name))
        face_locations = face_recognition.face_locations(image)

        pil_image = Image.fromarray(image)
        pil_image = apply_blur_mask(pil_image, face_locations)

        try:
            pil_image.save(join(IMAGE_PATH, OUT, image_name))
        except FileNotFoundError as error:
            print(error)

if __name__ == "__main__":
    sys.exit(main())
