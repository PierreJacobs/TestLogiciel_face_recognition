import unittest
import logging
import shutil
import random
import numpy as np

from os import listdir
from PIL import Image

import face_recognition

from . import utils

logger = logging.getLogger()

class TestMix(unittest.TestCase):

    @classmethod
    def setUpClass(self) -> None:
        """
        Copies temp images from `../images/base`
        """
        img_src = r'../images/base'
        self.img_dest = r'./images'

        try:
            shutil.copytree(img_src, self.img_dest)
        except FileExistsError:
            shutil.rmtree(self.img_dest)
            shutil.copytree(img_src, self.img_dest)

    @classmethod
    def tearDownClass(self) -> None:
        """
        Removes the temp images
        """
        shutil.rmtree(self.img_dest)
    
    def test_random_mode_and_format(self):
        """Tests random formats and modes
        """

        logger.info("Looping over a set of images")

        for image_name in listdir(self.img_dest):
            logger.debug(f"Image: {image_name}")

            wo_ext, _ = utils.split_image_and_ext(image_name)
            new_format = random.choice(utils.IMAGE_FORMATS)
            new_mode = random.choice(utils.IMAGE_CMODES)

            image = Image.open(f"{self.img_dest}/{image_name}")
            new_image = utils.format_image_to(
                image=image,
                out_path=f'{self.img_dest}/{wo_ext}.{new_format}',
                out_format=new_format,
                out_mode=new_mode
            )

            try:
                face_locations_img = face_recognition.face_locations(np.asarray(image))
                face_locations_new_img = face_recognition.face_locations(np.asarray(new_image))
            except RuntimeError:
                logger.warning(f"Couldn't perform face recognition on: {wo_ext}.{new_format} with mode: {new_mode} using {image_name} with mode: {image.mode} as base")
                continue
            finally:
                image.close()
                new_image.close()

            utils.save_mistakes(
                logger=logger,
                image_name=image_name, tt1=f'{image.format} - {image.mode}', tt2=f'{new_image.format} - {new_image.mode}',
                fl1=face_locations_img, fl2=face_locations_new_img,
                src1=f"{self.img_dest}/{image_name}", dest1=f"../images/mistakes/Format/{image.format}/{image_name}",
                src2=f"{self.img_dest}/{wo_ext}.{new_image.format}", dest2=f"../images/mistakes/Format/{new_image.format}/{wo_ext}.{new_image.format.lower()}"
            )

            with self.subTest():
                self.assertEqual(len(face_locations_img), len(face_locations_new_img))
    
def suite() -> unittest.suite.TestSuite:
    """
    Builds a suite from the `TestColorMode` class
    :return: test suite
    :rtype: unittest.suite.TestSuite
    """

    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(TestMix))
    return test_suite

if __name__ == "__main__":
    unittest.main()
