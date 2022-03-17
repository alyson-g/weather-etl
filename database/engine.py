"""
Singleton SQLAlchemy engine class
"""
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


class PgEngine:
    """
    Engine to connect to the Postgres database
    """
    def __init__(self):
        self.engine = self.create_engine()

    @staticmethod
    def get_db_str() -> str:
        """
        Get the database connection string
        :return: A database connection string
        """
        # Get variables from local .env
        load_dotenv()

        host = os.getenv("PGHOST")
        user = os.getenv("PGUSER")
        database = os.getenv("PGDATABASE")
        password = os.getenv("PGPASSWORD")
        port = os.getenv("PGPORT")

        return f"postgresql://{user}:{password}@{host}:{port}/{database}"

    def create_engine(self):
        """
        Create a SQLAlchemy engine
        :return: None
        """
        db_str = self.get_db_str()
        return create_engine(db_str)

    def get_engine(self) -> Engine:
        """
        Get the SQLAlchemy engine object
        :return: The engine object
        """
        if self.engine is None:
            self.engine = create_engine

        return self.engine
