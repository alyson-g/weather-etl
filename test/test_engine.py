import os
import unittest

from dotenv import load_dotenv

from database.engine import PgEngine


class TestPgEngine(unittest.TestCase):
    def setUp(self):
        """
        Set up environment variables for running the test
        :return: None
        """
        load_dotenv()

    def test_get_db_str(self):
        host = os.getenv("PGHOST")
        user = os.getenv("PGUSER")
        database = os.getenv("PGDATABASE")
        password = os.getenv("PGPASSWORD")
        port = os.getenv("PGPORT")

        db_str = PgEngine().get_db_str()

        with self.subTest(db_str=str, host=host):
            self.assertIn(host, db_str)
        with self.subTest(db_str=str, user=user):
            self.assertIn(user, db_str)
        with self.subTest(db_str=str, database=database):
            self.assertIn(database, db_str)
        with self.subTest(db_str=str, password=password):
            self.assertIn(password, db_str)
        with self.subTest(db_str=str, port=port):
            self.assertIn(port, db_str)

    def test_create_engine(self):
        """
        Test the create_engine function
        :return: None
        """
        eng = PgEngine()
        engine = eng.create_engine()

        self.assertIsNotNone(engine)

    def test_get_engine(self):
        """
        Test the get_engine function
        :return: None
        """
        eng = PgEngine()
        engine = eng.get_engine()

        self.assertIsNotNone(engine)


if __name__ == '__main__':
    unittest.main()
