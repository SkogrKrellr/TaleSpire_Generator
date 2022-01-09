import unittest
from config.config import config as Config

class TestConfig(unittest.TestCase):

    @classmethod
    def setUpClass(self) -> None:
        print("\nConfig: ", end='')
        self.maxDiff = None

    def test_readConfig(self):
        expected = f"""Assets"""
        self.assertMultiLineEqual(
            expected,
            Config.get('tableName', 'assets')
        )
