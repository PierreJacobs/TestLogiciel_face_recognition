import argparse
import shutil
import numpy as np
from os import listdir
from os.path import join

import face_recognition
from PIL import Image, ImageDraw, ImageFilter

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

def blur_images(*, src: str) -> None:
    folders = [join(src, subfolder, folder) for subfolder in listdir(src) for folder in listdir(join(src, subfolder))]

    for folder in folders:
        for image_name in listdir(folder):

            if image_name == "empty":
                continue
            
            mode = 'L' if folder == 'BW' else 'RGB'
            image = face_recognition.load_image_file(join(folder, image_name), mode=mode)
            face_locations = face_recognition.face_locations(image)

            pil_image = Image.fromarray(image)
            pil_image = apply_blur_mask(pil_image, face_locations)

            try:
                pil_image.save(join(folder, image_name))
            except FileNotFoundError as error:
                print(error)

def cli_parser() -> argparse.Namespace:
    """Returns a parsed version of parameters given to the script

    :return: parsed arguments
    :rtype: argparse.Namespace
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--blur', help="blur the output images", action="store_true")
    return parser.parse_args()

def change_image_format(image_path):

    image_formats = ["JPEG", "TIFF", "GIF", "BMP", "PNG"]

    image = Image.open(image_path)

    if image.format in image_formats:
        for format in image_formats:
            if image.format != format:
                image.save("%s%s.%s"%(image.filename, format, format))

def save_mistakes(*, logger, image_name: str, tt1: str, fl1: np.ndarray, tt2: str, fl2: np.ndarray, 
                    src1: str, dest1: str, src2: str, dest2: str) -> None:
    message = f"Image: {image_name}, {tt1}: {len(fl1)} faces, {tt2}: {len(fl2)} faces"
    if len(fl1) == len(fl2):
        logger.debug(message)
    else:
        logger.warning(message)
        shutil.copy(src1, dest1)
        shutil.copy(src2, dest2)