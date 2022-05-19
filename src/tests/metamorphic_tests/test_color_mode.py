import unittest
import shutil
import logging
import numpy as np

from os import listdir
from PIL import Image

import face_recognition

from . import utils

logger = logging.getLogger()

class TestColorMode(unittest.TestCase):

    def setUp(self) -> None:
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

    def tearDown(self) -> None:
        """
        Removes the temp images
        """
        shutil.rmtree(self.img_dest)
    
    def test_rgb_vs_bw(self) -> None:
        """
        Tests the difference between RGB and Black and White mode
        """
        logger.info("Looping over a set of images")

        for image_name in listdir(self.img_dest):

            logger.debug(f"Image: {image_name}")

            image_rgb = Image.open(f'{self.img_dest}/{image_name}')
            image_bw = utils.format_image_to(
                image=image_rgb,
                out_path=f'{self.img_dest}/BW_{image_name}',
                out_format=image_rgb.format,
                out_mode='L'
            )

            face_locations_rgb = face_recognition.face_locations(np.asarray(image_rgb))
            face_locations_bw = face_recognition.face_locations(np.asarray(image_bw))

            image_rgb.close()
            image_bw.close()

            utils.save_mistakes(
                logger=logger,
                image_name=image_name, tt1='RGB', tt2='BW',
                fl1=face_locations_rgb, fl2=face_locations_bw,
                src1=f"{self.img_dest}/{image_name}", dest1=f"../images/mistakes/Mode/RGB/{image_name}",
                src2=f"{self.img_dest}/BW_{image_name}", dest2=f"../images/mistakes/Mode/BW/{image_name}"
            )

            with self.subTest():
                self.assertEqual(len(face_locations_rgb), len(face_locations_bw))

def suite() -> unittest.suite.TestSuite:
    """
    Builds a suite from the `TestColorMode` class
    :return: test suite
    :rtype: unittest.suite.TestSuite
    """

    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(TestColorMode))
    return test_suite

if __name__ == "__main__":
    unittest.main()
