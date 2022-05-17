import argparse

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
