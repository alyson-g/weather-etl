"""
Main worker script
"""
import logging
import os

from dotenv import load_dotenv

from pipeline import Pipeline
from database.manage import setup_database, seed_locations

if __name__ == '__main__':
    load_dotenv()

    log_level = os.getenv("LOGLEVEL", "ERROR")
    logging.basicConfig(
        format='%(asctime)s %(levelname)s:%(message)s', filename='app.log',
        level=log_level
    )

    setup_database()
    seed_locations()

    pipe = Pipeline()
    pipe.run_all()
