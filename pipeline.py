"""
A data pipeline class that handles all ETL from the Open-Meteo API to our Postgres database
"""
import logging

import pandas as pd
import requests
from sqlalchemy import text

from database.engine import PgEngine
from utils import build_api_url


class Pipeline:
    def __init__(self):
        self.engine = PgEngine().get_engine()

    def get_locations(self) -> pd.DataFrame:
        """
        Get the current set of latitude/longitude coordinates
        :return: A DataFrame of latitude/longitude coordinates
        """
        with self.engine.connect() as conn:
            result = conn.execute(text(
                "select id, latitude, longitude from location"
            ))

        return pd.DataFrame(result, columns=["id", "latitude", "longitude"])

    def check_latest_insert(self):
        """
        Check the Postgres database for the time of the most recently added data
        :return: None
        """
        pass

    def fetch_data(self, lat, lng) -> pd.DataFrame:
        """
        Fetch data from the API
        :param lat: Latitude coordinate
        :param lng: Longitude coordinate
        :return: A DataFrame of weather data
        """
        url = build_api_url(lat, lng)

        # Fetch data and convert to dataframe
        r = requests.get(url)
        return pd.DataFrame(r.json()["hourly"])

    def preprocess_data(self):
        """
        Preprocess the fetched data
        :return: None
        """
        pass

    def insert_data(self):
        """
        Insert the processed data into the Postgres database
        :return: None
        """
        pass

    def run_all(self):
        """
        Run the full ETL pipeline
        :return: None
        """
        locations = self.get_locations()

        for i in range(locations.shape[0]):
            location = locations.iloc[i]

            logging.info("Retrieving data for %f %f", location["latitude"], location["longitude"])
            data = self.fetch_data(location["latitude"], location["longitude"])

            self.check_latest_insert()
            self.preprocess_data()
            self.insert_data()
