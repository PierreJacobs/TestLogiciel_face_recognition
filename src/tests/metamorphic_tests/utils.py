import shutil
import numpy as np
from PIL import Image
from PIL.Image import Image as PILImage
from typing import Optional

IMAGE_FORMATS = ("JPEG", "BMP", "PNG")
IMAGE_CMODES = ("L", "RGB")

def format_image_to(image: PILImage, out_path: str, out_format: str, out_mode: str) -> Optional[PILImage]:
    """Changes the format of given image at `in_path`

    :param image: source image
    :type in_path: PILImage
    :param out_path: path where to save formatted image
    :type out_path: str
    :param out_format: new image format to convert image to
    :type out_format: str
    :param out_mode: new image color mode to convert image to
    :type out_mode: str
    :return: formatted image
    :rtype: Optional[PILImage]
    """
    if image.format in IMAGE_FORMATS and out_format in IMAGE_FORMATS and out_mode in IMAGE_CMODES:
        out_image = image.convert(out_mode)
        out_image.save(out_path, mode=out_mode)
        out_image = Image.open(out_path)
        return out_image

def trim_listdir(fcontent: list[str], ext: str) -> list[str]:
    """Removes every file that does not end wiht `ext`

    :param fcontent: content of folder
    :type fcontent: list[str]
    :param ext: wanted extension
    :type ext: str
    :return: fildered list
    :rtype: list[str]
    """
    return list(filter(lambda f: f.endswith(ext), fcontent))

def split_image_and_ext(image_name: str) -> tuple[str, str]:
    """Splits the image and its extension.

    :param image_name: full name of the image
    :type image_name: str
    :return: name and extension of the image, in that order
    :rtype: tuple[str, str]
    """
    splitted = image_name.split('.')
    return '.'.join(splitted[0:-1]), splitted[-1]

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
        logger.error(message)
        shutil.copy(src1, dest1)
        shutil.copy(src2, dest2)
