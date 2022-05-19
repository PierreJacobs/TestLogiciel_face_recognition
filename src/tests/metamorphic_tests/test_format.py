import unittest
import shutil
import logging
import numpy as np

from os import listdir
from PIL import Image

import face_recognition

from . import utils

logger = logging.getLogger()

class TestFormat(unittest.TestCase):

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

    def test_png_vs_jpg(self):
        """Tests the difference between png and jpg formats
        """
        logger.info("Looping over a set of images")

        for image_name in utils.trim_listdir(listdir(self.img_dest), '.png'):
                        
            png_image = Image.open(f"{self.img_dest}/{image_name}")
            wo_ext, _ = utils.split_image_and_ext(image_name)

            jpg_image = utils.format_image_to(
                image=png_image,
                out_path=f"{self.img_dest}/{wo_ext}.jpg",
                out_format='JPEG',
                out_mode='RGB'
            )

            face_locations_png = face_recognition.face_locations(np.asarray(png_image))
            face_locations_jpg = face_recognition.face_locations(np.asarray(jpg_image))

            png_image.close()
            jpg_image.close()

            utils.save_mistakes(
                logger=logger,
                image_name=image_name, tt1='PNG', tt2='JPEG',
                fl1=face_locations_png, fl2=face_locations_jpg,
                src1=f"{self.img_dest}/{image_name}", dest1=f"../images/mistakes/Format/PNG/{image_name}",
                src2=f"{self.img_dest}/{wo_ext}.jpg", dest2=f"../images/mistakes/Format/JPEG/{wo_ext}.jpg"
            )

            with self.subTest():
                self.assertEqual(len(face_locations_png), len(face_locations_jpg))

    def test_bmp_vs_jpg(self):
        """Tests the difference between bmp and jpg formats
        """
        logger.info("Looping over a set of images")

        for image_name in utils.trim_listdir(listdir(self.img_dest), '.bmp'):

            bmp_image = Image.open(f"{self.img_dest}/{image_name}")
            wo_ext, _ = utils.split_image_and_ext(image_name)

            jpg_image = utils.format_image_to(
                image=bmp_image,
                out_path=f"{self.img_dest}/{wo_ext}.jpg",
                out_format='JPEG',
                out_mode='RGB'
            )

            face_locations_bmp = face_recognition.face_locations(np.asarray(bmp_image))
            face_locations_jpg = face_recognition.face_locations(np.asarray(jpg_image))

            bmp_image.close()
            jpg_image.close()

            utils.save_mistakes(
                logger=logger,
                image_name=image_name, tt1='BMP', tt2='JPEG',
                fl1=face_locations_bmp, fl2=face_locations_jpg,
                src1=f"{self.img_dest}/{image_name}", dest1=f"../images/mistakes/Format/BMP/{image_name}",
                src2=f"{self.img_dest}/{wo_ext}.jpg", dest2=f"../images/mistakes/Format/JPEG/{wo_ext}.jpg"
            )

            with self.subTest():
                self.assertEqual(len(face_locations_bmp), len(face_locations_jpg))

    def test_bmp_vs_png(self):
        """Tests the difference between bmp and png formats
        """
        logger.info("Looping over a set of images")

        for image_name in utils.trim_listdir(listdir(self.img_dest), '.bmp'):
            bmp_image = Image.open(f"{self.img_dest}/{image_name}")
            wo_ext, _ = utils.split_image_and_ext(image_name)

            png_image = utils.format_image_to(
                image=bmp_image,
                out_path=f"{self.img_dest}/{wo_ext}.png",
                out_format='PNG',
                out_mode='RGB'
            )

            face_locations_bmp = face_recognition.face_locations(np.asarray(bmp_image))
            face_locations_png = face_recognition.face_locations(np.asarray(png_image))

            bmp_image.close()
            png_image.close()

            utils.save_mistakes(
                logger=logger,
                image_name=image_name, tt1='BMP', tt2='PNG',
                fl1=face_locations_bmp, fl2=face_locations_png,
                src1=f"{self.img_dest}/{image_name}", dest1=f"../images/mistakes/Format/BMP/{image_name}",
                src2=f"{self.img_dest}/{wo_ext}.png", dest2=f"../images/mistakes/Format/PNG/{wo_ext}.png"
            )

            with self.subTest():
                self.assertEqual(len(face_locations_bmp), len(face_locations_png))

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
