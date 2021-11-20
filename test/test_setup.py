import unittest
from setup.setup import *

class TestSetup(unittest.TestCase):
    
    @classmethod
    def setUpClass(self) -> None:
        print("\nSetup: " ,end = '')

    def test_firstTimeSetup(self):
        #FirstTimeSetup()
        pass
