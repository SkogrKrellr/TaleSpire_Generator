import unittest

from generator.generator import Generator
from classes.asset_manager import AssetManager

class TestGenerator(unittest.TestCase):
    
    @classmethod
    def setUpClass(self) -> None:
        print("\nGenerate: " ,end = '')
        self.generator = Generator()
     
    def tearDown(self) -> None:
        return super().tearDown()

    def setUp(self):
        self.generator.setXYZ(3,3,10)
        self.generator.setOctaves(1, 0.5)
        self.generator.setScales(1, 64)
        self.generator.setExponent(2.0)
        
    def arrayCompare(self, generated, expected, delta):
        msg = ""
        for x in range(0,3):
            for y in range(0,3):
                if abs(expected[x][y] - generated[x][y]) > delta:
                    msg += f"""({x}, {y}) dif = { 
                        round(expected[x][y] - generated[x][y], 4) 
                        } expected: { 
                            round(expected[x][y], 4) 
                        } got: {
                            round(generated[x][y], 4)
                        }\n"""
        if len(msg):
            msg = "\nSome values are not equal: \n" + msg
        return msg

    def test_setXYZ(self) -> None:
        self.generator.setXYZ(15,10,10)
        self.assertEqual(self.generator.x, 15)
        self.assertEqual(self.generator.y, 10)
        self.assertEqual(self.generator.z, 10)
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
        expected = [
            [0., 0., 0.],
            [0., 0., 0.],
            [0., 0., 0.]
        ]
        msg = self.arrayCompare(self.generator.elevation, expected, 0.01)
        self.assertTrue(len(msg)==0, msg = msg)

    def test_generateElevation(self) -> None:
        expected = [
            [0.5, 0.5, 0.5],
            [0.5, 0.5, 0.5],
            [0.5, 0.5, 0.5]
        ]
        self.generator.generateElevation()
        msg = self.arrayCompare(self.generator.elevation, expected, 0.5)
        self.assertTrue(len(msg)==0, msg = msg)

    def test_powerElevation(self) -> None:
        expected = [
            [0.25, 0.217, 0.213],
            [0.298, 0.229, 0.172],
            [0.145, 0.248, 0.095]
        ]
        self.generator.generateElevation()
        self.generator.powerElevation()
        msg = self.arrayCompare(self.generator.elevation, expected, 0.01)
        self.assertTrue(len(msg)==0, msg = msg)

    def test_scaleToZHeight(self) -> None:
        expected = [
            [5., 4.668, 4.620],
            [5.467, 4.788, 4.151],
            [3.811, 4.987, 3.096]
        ]
        self.generator.generateElevation()
        self.generator.multiplyByValue()
        msg = self.arrayCompare(self.generator.elevation, expected, 0.01)
        self.assertTrue(len(msg)==0, msg = msg)
            
    
        
