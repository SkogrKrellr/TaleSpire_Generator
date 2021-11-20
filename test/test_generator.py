import unittest
import numpy
from generator.generator import Generator

class TestGenerator(unittest.TestCase):
    
    @classmethod
    def setUpClass(self) -> None:
        print("\nGenerate: " ,end = '')
        self.generator = Generator()
     
    def tearDown(self) -> None:
        return super().tearDown()

    def prep(self):
        self.generator.setXYZ(3,3,10)
        self.generator.setOctaves(1, 0.5)
        self.generator.setScales(1, 64)
        self.generator.setExponent(2.0)
        
    def test_setXYZ(self) -> None:
        self.generator.setXYZ(15,10,5)
        self.assertEqual(self.generator.x, 15)
        self.assertEqual(self.generator.y, 10)
        self.assertEqual(self.generator.z, 5)
        self.assertEqual(self.generator.max_size, 15)

    def test_setOctaves(self) -> None:
        self.generator.setOctaves(1, 0.75, 0.5)
        self.assertEqual(self.generator.octaves[0], 1)
        self.assertEqual(self.generator.octaves[1], 0.75)
        self.assertEqual(self.generator.octaves[2], 0.5)

    def test_setScales(self) -> None:
        self.generator.setScales(1, 4, 16)
        self.assertEqual(self.generator.scales[0], 1)
        self.assertEqual(self.generator.scales[1], 4)
        self.assertEqual(self.generator.scales[2], 16)

    def test_setExponent(self) -> None:
        self.generator.setExponent(0.78)
        self.assertEqual(self.generator.exponent, 0.78)

    def test_noiseXY(self) -> None:
        self.generator.setExponent(123456789)
        self.assertEqual(self.generator.noiseXY(643, 234), -0.4651744574140941)

    def test_setEmptyArray(self) -> None:
        self.prep()
        self.assertEqual(
            self.generator.prettyPrintElevation(), 
            "[[0. 0. 0.]\n [0. 0. 0.]\n [0. 0. 0.]]"
        )

    def test_generateElevation(self) -> None:
        self.prep()
        self.generator.generateElevation()
        self.assertEqual(
            self.generator.prettyPrintElevation(), 
            "[[0.5 0.546 0.381]\n [0.466 0.478 0.498]\n [0.462 0.415 0.309]]"
        )

    def test_powerElevation(self) -> None:
        self.prep()
        self.generator.generateElevation()
        self.generator.powerElevation()
        self.assertEqual(
            self.generator.prettyPrintElevation(), 
            "[[0.25 0.298116 0.145161]\n [0.217156 0.228484 0.248004]\n [0.213444 0.172225 0.095481]]"
        )

    def test_scaleToZHeight(self) -> None:
        self.prep()
        self.generator.generateElevation()
        self.generator.scaleToZHeight()
        self.assertEqual(
            self.generator.prettyPrintElevation(), 
            "[[5. 5.46 3.81]\n [4.66 4.78 4.98]\n [4.62 4.15 3.09]]"
        )




