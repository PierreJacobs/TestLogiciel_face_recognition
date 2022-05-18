import unittest
import shutil
import logging
import numpy as np

from os import listdir
from PIL import Image

import face_recognition
import utils

logger = logging.getLogger()

class TestFormat(unittest.TestCase):
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

    def test_png_vs_jpg(self):
        """Tests the difference between png and jpg formats
        """
        logger.info("Looping over a set of images")

        for image_name in listdir(self.img_dest):
                        
            png_image = Image.open(f"{self.img_dest}/{image_name}")
            if png_image.format != "PNG":
                continue
            
            # Avoid RGBA
            png_image = png_image.convert("RGB")
            # Get image name and remove extension
            wo_ext = "".join(image_name.split('.')[0:-1])

            jpg_image = png_image.convert("RGB")
            # Needs to be saved otherwise format is None
            jpg_image.save(f"{self.img_dest}/{wo_ext}.jpg")
            jpg_image = Image.open(f"{self.img_dest}/{wo_ext}.jpg")

            face_locations_png = face_recognition.face_locations(np.asarray(png_image))
            face_locations_jpg = face_recognition.face_locations(np.asarray(jpg_image))

            utils.save_mistakes(
                logger=logger,
                image_name=image_name, tt1='PNG', tt2='JPG',
                fl1=face_locations_png, fl2=face_locations_jpg,
                src1=f"{self.img_dest}/{image_name}", dest1=f"../images/mistakes/Format/PNG/{image_name}",
                src2=f"{self.img_dest}/{wo_ext}.jpg", dest2=f"../images/mistakes/Format/JPG/{wo_ext}.jpg"
            )

            with self.subTest():
                self.assertEqual(len(face_locations_png), len(face_locations_jpg))

    def test_bmp_vs_jpg(self):
        """Tests the difference between bmp and jpg formats
        """
        logger.info("Looping over a set of images")

        for image_name in listdir(self.img_dest):
            bmp_image = Image.open(f"{self.img_dest}/{image_name}")
            if bmp_image.format != "BMP":
                continue

            # Get image name and remove extension
            wo_ext = "".join(image_name.split('.')[0:-1])

            jpg_image = bmp_image.convert("RGB")
            # Needs to be saved otherwise format is None
            jpg_image.save(f"{self.img_dest}/{wo_ext}.jpg")
            jpg_image = Image.open(f"{self.img_dest}/{wo_ext}.jpg")

            face_locations_bmp = face_recognition.face_locations(np.asarray(bmp_image))
            face_locations_jpg = face_recognition.face_locations(np.asarray(jpg_image))

            utils.save_mistakes(
                logger=logger,
                image_name=image_name, tt1='BMP', tt2='JPG',
                fl1=face_locations_bmp, fl2=face_locations_jpg,
                src1=f"{self.img_dest}/{image_name}", dest1=f"../images/mistakes/Format/BMP/{image_name}",
                src2=f"{self.img_dest}/{wo_ext}.jpg", dest2=f"../images/mistakes/Format/JPG/{wo_ext}.jpg"
            )

            with self.subTest():
                self.assertEqual(len(face_locations_bmp), len(face_locations_jpg))

def suite() -> unittest.suite.TestSuite:
    """
    Builds a suite from the `TestFormat` class
    :return: test suite
    :rtype: unittest.suite.TestSuite
    """

    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(TestFormat))
    return test_suite

if __name__ == "__main__":
    unittest.main()