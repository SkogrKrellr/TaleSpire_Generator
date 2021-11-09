from typing import Generator
import unittest
import generator.generator as Generator

class TestGenerator(unittest.TestCase):

    def setUp(self) -> None:
        self.generator = Generator()
    
    def tearDown(self) -> None:
        return super().tearDown()
        
