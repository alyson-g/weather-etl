from datetime import datetime
import unittest
from unittest.mock import patch

import pandas as pd
import pandas.testing as pd_testing

from pipeline import Pipeline


class TestPipeline(unittest.TestCase):
    def test_get_locations(self):
        """
        Test the get_locations function
        :return: None
        """
        with patch.object(Pipeline, 'get_locations', return_value=None) as mock_method:
            pipeline = Pipeline()
            pipeline.get_locations()

        mock_method.assert_called()

    def test_check_latest_insert(self):
        """
        Test the check_latest_insert function
        :return: None
        """
        with patch.object(Pipeline, 'check_latest_insert', return_value=None) as mock_method:
            pipeline = Pipeline()
            pipeline.check_latest_insert("1")

        mock_method.assert_called_once_with("1")

    def test_fetch_data(self):
        """
        Test the fetch_data function
        :return: None
        """
        with patch.object(Pipeline, 'fetch_data', return_value=None) as mock_method:
            pipeline = Pipeline()
            pipeline.fetch_data("123", "123")

        mock_method.assert_called_once_with("123", "123")

    def test_preprocess_data(self):
        """
        Test the preprocess_data function
        :return: None
        """
        pipeline = Pipeline()

        # Create test data and timestamp
        data = pd.read_csv("./test/test_data/clean_data.csv")
        data = data.drop(["location_id"], axis=1)
        timestamp = datetime(2022, 3, 18)

        # Preprocess the data
        proc_data = pipeline.preprocess_data(data, timestamp)

        pd_testing.assert_frame_equal(proc_data, data[data["time"] > timestamp])

    def test_check_data(self):
        """
        Test the check_data function
        :return: None
        """
        pipeline = Pipeline()

        with self.subTest(pipeline=pipeline):
            # Test clean data set
            clean_data = pd.read_csv("./test/test_data/clean_data.csv")
            clean_data = clean_data.drop(["location_id"], axis=1)

            self.assertTrue(pipeline.check_data(clean_data))

        with self.subTest(pipeline=pipeline):
            # Test data set with missing data
            bad_data = pd.read_csv("./test/test_data/bad_data.csv")
            bad_data = bad_data.drop(["location_id"], axis=1)
            self.assertFalse(pipeline.check_data(bad_data))

    def test_insert_data(self):
        """
        Test the insert_data function
        :return: None
        """
        data = pd.read_csv("./test/test_data/clean_data.csv")
        data = data.drop(["location_id"], axis=1)

        with patch.object(Pipeline, 'insert_data', return_value=None) as mock_method:
            pipeline = Pipeline()

            pipeline.insert_data("1", data)

        mock_method.assert_called_once_with("1", data)

    def test_run_all(self):
        """
        Test the run_all function
        :return: None
        """
        with patch.object(Pipeline, 'run_all', return_value=None) as mock_method:
            pipeline = Pipeline()
            pipeline.run_all()

        mock_method.run_all()


if __name__ == '__main__':
    unittest.main()
