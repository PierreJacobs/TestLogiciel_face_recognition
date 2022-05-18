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

def format_image_to(in_path, out_path, out_format):

    image_formats = ["JPEG", "GIF", "BMP", "PNG"]
    in_image = Image.open(in_path)

    if in_image.format in image_formats and out_format in image_formats:
        out_image = in_image.convert("RGB")
        out_image.save(out_path)
        out_image = Image.open(out_path)
        return out_image

def save_mistakes(*, logger, image_name: str, tt1: str, fl1: np.ndarray, tt2: str, fl2: np.ndarray, 
                    src1: str, dest1: str, src2: str, dest2: str) -> None:
    """Saves images that are considered a miss
    :param logger: logger used to save log messages
    :type logger: logging.Logger
    :param image_name: name of the image
    :type image_name: str
    :param tt1: comparison type of image  1
    :type tt1: str
    :param fl1: face locations of image 1
    :type fl1: np.ndarray
    :param tt2: comparison type of image 2
    :type tt2: str
    :param fl2: face locations of image 2
    :type fl2: np.ndarray
    :param src1: source of image 1
    :type src1: str
    :param dest1: destination of image 1
    :type dest1: str
    :param src2: source of image 2
    :type src2: str
    :param dest2: destination of image 2
    :type dest2: str
    """
    message = f"Image: {image_name}, {tt1}: {len(fl1)} faces, {tt2}: {len(fl2)} faces"
    if len(fl1) == len(fl2):
        logger.debug(message)
    else:
        logger.warning(message)
        shutil.copy(src1, dest1)
        shutil.copy(src2, dest2)
