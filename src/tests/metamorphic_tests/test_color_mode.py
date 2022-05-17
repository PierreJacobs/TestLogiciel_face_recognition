import unittest
import logging
import shutil
import face_recognition

from os import listdir
from PIL import Image

logger = logging.getLogger()

class TestColorMode(unittest.TestCase):

    @classmethod
    def setUpClass(self) -> None:
        """
        Sets the needs up before running the tests
        """
        img_src = r'../images'
        img_dest = r'./images'

        try:
            shutil.copytree(img_src, img_dest)
        except FileExistsError:
            shutil.rmtree(img_dest)
            shutil.copytree(img_src, img_dest)

    @classmethod
    def tearDownClass(self) -> None:
        """
        Tears the needs down after the tests 
        """
        img_dest = r'./images'
        shutil.rmtree(img_dest)

    
    def test_rgb_vs_bw(self) -> None:
        """
        Tests the difference between RGB and Black and White mode
        """
        logger.info("Looping over a set of images")

        for image_name in listdir(r'./images'):

            logger.debug(f"Image: {image_name}")

            image_rbg = face_recognition.load_image_file(f'./images/{image_name}')
            face_locations_rgb = face_recognition.face_locations(image_rbg)
            
            pil_image_rgb = Image.fromarray(image_rbg)
            pil_image_rgb.convert('L').save(f'./images/BW_{image_name}')

            image_bw = face_recognition.load_image_file(f'./images/BW_{image_name}', 'L')
            face_locations_bw = face_recognition.face_locations(image_bw)

            message = f"Image: {image_name}, RGB: {len(face_locations_rgb)} faces, BW: {len(face_locations_bw)} faces"
            if len(face_locations_rgb) == len(face_locations_bw):
                logger.debug(message)
            else:
                logger.warning(message)
                shutil.copy(f"./images/{image_name}", f"../img_mistakes/RGB_{image_name}")
                shutil.copy(f"./images/BW_{image_name}", f"../img_mistakes/BW_{image_name}")

def suite() -> unittest.suite.TestSuite:
    """
    Builds a suite from the `TestTest` class
    :return: test suite
    :rtype: unittest.suite.TestSuite
    """

    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(TestColorMode))
    return test_suite

if __name__ == "__main__":
    unittest.main()