"""
A data pipeline class that handles all ETL from the Open-Meteo API to our Postgres database
"""
from datetime import datetime
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

    def check_latest_insert(self, location_id: str):
        """
        Check the Postgres database for the time of the most recently added data
        :param location_id: The id of the location to check
        :return: None
        """
        with self.engine.connect() as conn:
            result = conn.execute(text(
                "select max(time) as time from hourly_weather where location_id = :location"
            ), location=location_id)

        timestamp = result.fetchall()[0][0]

        return timestamp

    @staticmethod
    def fetch_data(lat: str, lng: str) -> pd.DataFrame:
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

    @staticmethod
    def preprocess_data(data: pd.DataFrame, timestamp: datetime) -> pd.DataFrame:
        """
        Preprocess the fetched data
        :param data: A DataFrame of hourly weather data
        :param timestamp: A
        :return: None
        """
        # Convert time column to datetime
        data["time"] = pd.to_datetime(data["time"])

        # Filter out data that is already in the database
        return data[data["time"] > timestamp]

    @staticmethod
    def check_data(data: pd.DataFrame) -> bool:
        """
        Perform checks on data integrity
        :param data: A DataFrame of hourly weather data
        :return: A boolean value. True if the data is valid, False otherwise
        """
        # We may want to perform additional data checks here. For now I'm just
        # checking for any null values.
        return not data.isnull().values.any()

    def insert_data(self, location_id: str, data: pd.DataFrame):
        """
        Insert the processed data into the Postgres database
        :param location_id: The location id of the data
        :param data: A DataFrame of data to insert
        :return: None
        """
        # Add the location id to the DataFrame
        data["location_id"] = location_id

        # Insert the data into Postgres
        data.to_sql("hourly_weather", self.engine, if_exists="append", method="multi", index=False)

    def run_all(self):
        """
        Run the full ETL pipeline
        :return: None
        """
        locations = self.get_locations()

        for i in range(locations.shape[0]):
            location = locations.iloc[i]
            logging.info("Retrieving data for %f %f", location["latitude"], location["longitude"])

            # Fetch data for the current location
            data = self.fetch_data(location["latitude"], location["longitude"])

            # Check data integrity before continuing
            if not self.check_data(data):
                logging.critical(
                    "Data integrity problems detected. Aborting data insertion for %f %f",
                    location["latitude"], location["longitude"]
                )
                continue

            # Filter data to only rows that have not yet been inserted
            timestamp = self.check_latest_insert(location["id"])

            if timestamp is not None:
                data = self.preprocess_data(data, timestamp)

            # Insert data, if any
            if data.empty:
                logging.info("No new data available for %f %f", location["latitude"], location["longitude"])
            else:
                self.insert_data(location["id"], data)
                logging.info(
                    "Retrieved %d records for %f %f", data.shape[0],
                    location["latitude"], location["longitude"]
                )
