import unittest
from classes.database import Database
from classes.config import config as Config

class TestGenerator(unittest.TestCase):

    @classmethod
    def setUpClass(self) -> None:
        self.database = Database()
    
    @classmethod
    def tearDownClass(self) -> None:
        self.database.close()

