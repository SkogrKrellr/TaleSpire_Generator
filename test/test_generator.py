import unittest
from generator.generator import Generator

class TestGenerator(unittest.TestCase):

    @classmethod
    def setUpClass(self) -> None:
        self.gen = Generator()
    
    def tearDown(self) -> None:
        return super().tearDown()
        
    def test_getElevation(self) -> None:
        self.gen.generateElevation()
