import unittest
from classes.quad import Quad

class TestQuad(unittest.TestCase):
    
    @classmethod
    def setUpClass(self) -> None:
        print("\nQuad: " ,end = '')
        self.quad = Quad(0,0.25,0.5,1)

    def test_str(self):
        self.assertEqual(self.quad.__str__(), "x: 0 y: 0.25 z: 0.5 w: 1")