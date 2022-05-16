import face_recognition
from PIL import Image, ImageDraw, ImageFilter

from os import listdir
from os.path import join

STATIC = r'../static'
IMAGE_PATH = join(STATIC, "img")
IN = r'in'
OUT = r'out'


def apply_blur_mask(pil_image: Image, face_locations, /, radius=50) -> Image:
    for (top, right, bottom, left) in face_locations:
        # Creating a blur mask
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

    for image_name in listdir(join(IMAGE_PATH, IN)):

        image = face_recognition.load_image_file(join(IMAGE_PATH, IN, image_name))
        face_locations = face_recognition.face_locations(image)

        pil_image = Image.fromarray(image)
        pil_image = apply_blur_mask(pil_image, face_locations)

        try:
            pil_image.save(join(IMAGE_PATH, OUT, image_name))
        except FileNotFoundError as e:
            print(e)

if __name__ == "__main__":
    exit(main())
