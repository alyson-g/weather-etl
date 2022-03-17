"""
A data pipeline class that handles all ETL from the Open-Meteo API to our Postgres database
"""
import pandas as pd
import psycopg2
import requests

from utils import build_api_url


class Pipeline:
    def __init__(self):
        pass

    def get_locations(self) -> pd.DataFrame:
        """
        Get the current set of latitude/longitude coordinates
        :return: A DataFrame of latitude/longitude coordinates
        """
        # TODO - create a database table to hold these values instead
        return pd.read_csv("data.csv")

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

            data = self.fetch_data(location["lat"], location["lng"])

            self.check_latest_insert()
            self.preprocess_data()
            self.insert_data()
