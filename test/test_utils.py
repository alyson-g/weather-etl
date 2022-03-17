"""
Unit tests for utils
"""
import unittest

import utils


class TestUtils(unittest.TestCase):
    def test_build_api_url(self):
        """
        Test that the build_api_url function properly formats the URl
        :return: None
        """
        url = utils.build_api_url("50", "50")

        with self.subTest(url=url):
            self.assertIsNotNone(url)
        with self.subTest(url=url):
            self.assertIn("temperature_2m", url)
        with self.subTest(url=url):
            self.assertIn("relativehumidity_2m", url)
        with self.subTest(url=url):
            self.assertIn("dewpoint_2m", url)
        with self.subTest(url=url):
            self.assertIn("pressure_msl", url)
        with self.subTest(url=url):
            self.assertIn("cloudcover", url)
        with self.subTest(url=url):
            self.assertIn("precipitation", url)
        with self.subTest(url=url):
            self.assertIn("weathercode", url)


if __name__ == '__main__':
    unittest.main()