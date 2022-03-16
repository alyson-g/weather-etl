"""
A data pipeline class that handles all ETL from the Open-Meteo API to our Postgres database
"""
import pandas as pd
import psycopg2
import requests


class Pipeline:
    def __init__(self):
        pass

    def check_latest_insert(self):
        """
        Check the Postgres database for the time of the most recently added data
        :return: None
        """
        pass

    def fetch_data(self):
        """
        Fetch data from the API
        :return: None
        """
        pass

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
        self.check_latest_insert()
        self.fetch_data()
        self.preprocess_data()
        self.insert_data()
