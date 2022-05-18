import unittest
import logging
import shutil
import face_recognition

import utils
from os import listdir
from PIL import Image

logger = logging.getLogger()

class TestColorMode(unittest.TestCase):

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
    
    def test_rgb_vs_bw(self) -> None:
        """
        Tests the difference between RGB and Black and White mode
        """
        logger.info("Looping over a set of images")

        for image_name in listdir(self.img_dest):

            logger.debug(f"Image: {image_name}")

            image_rbg = face_recognition.load_image_file(f'{self.img_dest}/{image_name}')
            face_locations_rgb = face_recognition.face_locations(image_rbg)
            
            pil_image_rgb = Image.fromarray(image_rbg)
            pil_image_rgb.convert('L').save(f'{self.img_dest}/{utils.set_image_mode(image_name, "BW")}')

            image_bw = face_recognition.load_image_file(f'{self.img_dest}/{utils.set_image_mode(image_name, "BW")}', 'L')
            face_locations_bw = face_recognition.face_locations(image_bw)

            message = f"Image: {image_name}, RGB: {len(face_locations_rgb)} faces, BW: {len(face_locations_bw)} faces"
            if len(face_locations_rgb) == len(face_locations_bw):
                logger.debug(message)
            else:
                logger.warning(message)
                shutil.copy(f"{self.img_dest}/{image_name}", f"../images/mistakes/in/{utils.set_image_mode(image_name, 'RGB')}")
                shutil.copy(f"{self.img_dest}/{utils.set_image_mode(image_name, 'BW')}", f"../images/mistakes/in/{utils.set_image_mode(image_name, 'BW')}")

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