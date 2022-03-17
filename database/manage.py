import logging

import pandas as pd
from sqlalchemy import text
from sqlalchemy_utils.functions import database_exists, create_database

from database.engine import PgEngine
from database.models import meta


def setup_database():
    """
    Set up the database, if not already set up
    :return: None
    """
    db_str = PgEngine.get_db_str()

    # Create the database, if it does not already exist
    if not database_exists(db_str):
        logging.info("Database does not exist. Creating...")
        create_database(db_str)
        logging.info("Database created")

    # Set up tables, if they do not already exist
    eng = PgEngine()
    engine = eng.get_engine()
    meta.create_all(engine, checkfirst=True)
    logging.info("All required tables exist")


def seed_locations():
    """
    Seed the location information from a CSV file
    :return: None
    """
    # Check if seed data is already present
    eng = PgEngine()
    engine = eng.get_engine()

    with engine.connect() as conn:
        result = conn.execute(text("select count(1) from location"))
        count = result.one()[0]

    # If seed data is not present, add it
    if count == 0:
        logging.info("location table is empty. Seeding...")

        # Read data from CSV file and format
        seed_data = pd.read_csv("data.csv")
        seed_data = seed_data.rename(columns={"lat": "latitude", "lng": "longitude"})

        # Insert seed data into Postgres
        seed_data.to_sql("location", engine, if_exists="append", method="multi", index=False)

        logging.info("location table successfully seeded")
    else:
        logging.info("location table already contains data")
