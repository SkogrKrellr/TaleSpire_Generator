import json
import unittest
import matplotlib.pyplot as plt
import numpy
import pyperclip as pc
from objects.visualizer import Visualizer
import pandas as pd

from generator.generator import Generator
from objects.assetManager import AssetManager
from converter.conversionManager import ConversionManager
import settings

class TestGenerator(unittest.TestCase):
    
    @classmethod
    def setUpClass(self) -> None:
        print("\nGenerate: " ,end = '')
        self.maxDiff = None
     
    def tearDown(self) -> None:
        return super().tearDown()

    def setUp(self):
        self.generator = Generator()
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

        # Valid XYZ
        self.generator.setXYZ(15,10,10)
        self.assertEqual(self.generator.x, 15)
        self.assertEqual(self.generator.y, 10)
        self.assertEqual(self.generator.z, 10)
        self.assertEqual(self.generator.elevation.tolist(), numpy.zeros((15,10)).tolist())
        self.assertEqual(self.generator.placeObjectZ.tolist(), numpy.zeros((15,10)).tolist())

        # Invalid XYZ
        self.generator.setXYZ(-3,0,-123.2)
        self.assertEqual(self.generator.x, 1)
        self.assertEqual(self.generator.y, 1)
        self.assertEqual(self.generator.z, 1)
        self.assertEqual(self.generator.elevation.tolist(), numpy.zeros((1,1)).tolist())
        self.assertEqual(self.generator.placeObjectZ.tolist(), numpy.zeros((1,1)).tolist())

    def test_setOctaves(self) -> None:
        self.generator.setOctaves(1, 0.75, 0.5)
        self.assertEqual(self.generator.noise.octaves[0], 1)
        self.assertEqual(self.generator.noise.octaves[1], 0.75)
        self.assertEqual(self.generator.noise.octaves[2], 0.5)

    def test_setScales(self) -> None:
        self.generator.setScales(1, 4, 16)
        self.assertEqual(self.generator.noise.scales[0], 1)
        self.assertEqual(self.generator.noise.scales[1], 4)
        self.assertEqual(self.generator.noise.scales[2], 16)

    def test_setExponent(self) -> None:
        self.generator.setExponent(0.78)
        self.assertEqual(self.generator.exponent, 0.78)

    def test_setSeed(self) -> None:
        self.assertEqual(self.generator.noise.noiseXY(0, 0), 0.0)
        self.assertEqual(self.generator.noise.noiseXY(-5, -17), -0.5234590815895944)
        self.assertEqual(self.generator.noise.noiseXY(5, 17), 0.392517558040669)

        self.generator.setSeed(123456789)
        self.assertEqual(self.generator.noise.noiseXY(0, 0), 0.0)
        self.assertEqual(self.generator.noise.noiseXY(-5, -17), -0.7200741622627534)
        self.assertEqual(self.generator.noise.noiseXY(5, 17), -0.79179780448877)
    
    def test_setTileSize(self) -> None:
        self.assertEqual(self.generator.tileSize, 0)
        self.generator.setTileSize(2)
        self.assertEqual(self.generator.tileSize, 2.0)
        self.generator.setTileSize(-3)
        self.assertEqual(self.generator.tileSize, 0)

    def test_noiseXY(self) -> None:
        self.generator.setSeed(123456)
        self.assertEqual(self.generator.noise.noiseXY(0, 0), 0.0)
        self.assertEqual(self.generator.noise.noiseXY(-643, -234), -0.27525423557961687)
        self.assertEqual(self.generator.noise.noiseXY(643, 234), 0.2521903471662688)

    def test_setEmptyArray(self) -> None:
        expected = [
            [0., 0., 0.],
            [0., 0., 0.],
            [0., 0., 0.]
        ]
        msg = self.arrayCompare(self.generator.elevation, expected, 0.01)
        self.assertTrue(len(msg)==0, msg = msg)

    def test_generateElevation(self) -> None:
        # We expect it to give values between 0 and 1, se we check if the values are 0.5 with the tolerance of 0..
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
            [0.25, 0.222, 0.1643],
            [0.4141, 0.264, 0.2642],
            [0.1688, 0.163, 0.1657]
        ]
        self.generator.generateElevation()
        self.generator.powerElevation()
        msg = self.arrayCompare(self.generator.elevation, expected, 0.01)
        self.assertTrue(len(msg)==0, msg = msg)

    def test_scaleToZHeight(self) -> None:
        expected = [
            [5.0, 4.71186769, 4.05318311],
            [6.43531149, 5.13811443, 5.13961945],
            [4.10843619, 4.03712311, 4.0710484 ]
        ]
        self.generator.generateElevation()
        self.generator.multiplyByValue()
        msg = self.arrayCompare(self.generator.elevation, expected, 0.01)
        self.assertTrue(len(msg)==0, msg = msg)

    def test_terrainGenerationNoPreciseNoRidge(self):
        expected = """```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```"""

        self.generator.setXYZ(20,20,50)
        self.generator.setOctaves(1, 0.5, 0.25)
        self.generator.setScales(1, 2, 4)
        self.generator.setExponent(1.5)
        self.generator.setUsePreciseHeight(False)
        self.generator.setUseRidgeNoise(False)
        
        groundAssets = Generator.createObjectList([
            {"asset" : "3911d10d-142b-4f33-9fea-5d3a10c53781"},
        ])
        output = self.generator.generate(groundAssets)[0]["output"]
        self.assertEqual( expected, output, msg = "Output strings are different!")

    def test_terrainGenerationPreciseNoRidge(self):
        expected = """```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```"""

        self.generator.setXYZ(20,20,50)
        self.generator.setOctaves(1, 0.5, 0.25)
        self.generator.setScales(1, 2, 4)
        self.generator.setExponent(1.5)
        self.generator.setUsePreciseHeight(True)
        self.generator.setUseRidgeNoise(False)
        
        groundAssets = Generator.createObjectList([
            {"asset" : "3911d10d-142b-4f33-9fea-5d3a10c53781"}
        ])
        output = self.generator.generate(groundAssets)[0]["output"]
        self.assertEqual( expected, output, msg = "Output strings are different!")

    def test_terrainGenerationNoPreciseRidge(self):
        expected = """```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```"""

        self.generator.setXYZ(20,20,20)
        self.generator.setOctaves(1, 0.5, 0.25)
        self.generator.setScales(1, 2, 4)
        self.generator.setExponent(1.5)
        self.generator.setUsePreciseHeight(False)
        self.generator.setUseRidgeNoise(True)
        
        groundAssets = Generator.createObjectList([
            {"asset" : "3911d10d-142b-4f33-9fea-5d3a10c53781"}
        ])
        output = self.generator.generate(groundAssets)[0]["output"]
        self.assertEqual( expected, output, msg = "Output strings are different!")

    def test_terrainGenerationPreciseRidge(self):
        expected = """```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```"""

        self.generator.setXYZ(20,20,20)
        self.generator.setOctaves(1, 0.5, 0.25)
        self.generator.setScales(1, 2, 4)
        self.generator.setExponent(1.5)
        self.generator.setUsePreciseHeight(True)
        self.generator.setUseRidgeNoise(True)
        
        groundAssets = Generator.createObjectList([
            {"asset" : "3911d10d-142b-4f33-9fea-5d3a10c53781"}
        ])
        output = self.generator.generate(groundAssets)[0]["output"]
        self.assertEqual( expected, output, msg = "Output strings are different!")

    def test_terrainGenerationPlaceObject(self):
        expected = """```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```"""

        self.generator.setXYZ(20,20,20)
        self.generator.setOctaves(1, 0.5, 0.25)
        self.generator.setScales(1, 2, 4)
        self.generator.setExponent(1.5)
        self.generator.setUsePreciseHeight(True)
        self.generator.setUseRidgeNoise(False)
        
        groundAssets = Generator.createObjectList([
            {"asset" : "3911d10d-142b-4f33-9fea-5d3a10c53781"}
        ])

        treeUUID = AssetManager.addCustomAsset(
            "Tree_4",
            "```H4sIAAAAAAAACzv369xFJgZmBgYGV8sOe+Zcb6+FuwOFhA/vvMUIFGP54+9t4qri2XJlvvU8595GJqDYnexlT8+YiztvObZwR4/xpJcgdYwMEmxACmiOAIsBQwMjEwMHUwADBEBoAGi/N01oAAAA```"
        )

        placeObjects = Generator.createObjectList([
            {"asset" : treeUUID}
        ], True)
        output = self.generator.generate(groundAssets, placeObjects)[0]["output"]
        self.assertEqual( expected, output, msg = "Output strings are different!")


    def test_terrainGenerationPlaceObject(self):
        expected = """```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```"""

        self.generator.setXYZ(20,20,20)
        self.generator.setOctaves(1, 0.5, 0.25)
        self.generator.setScales(1, 2, 4)
        self.generator.setExponent(1.5)
        self.generator.setUsePreciseHeight(True)
        self.generator.setUseRidgeNoise(False)
        
        groundAssets = Generator.createObjectList([
            {"asset" : "3911d10d-142b-4f33-9fea-5d3a10c53781"}
        ])
        placeObjects = Generator.createObjectList([
            {"asset" : AssetManager.addCustomAsset(
                "Tree_4",
                "```H4sIAAAAAAAACzv369xFJgZmBgYGV8sOe+Zcb6+FuwOFhA/vvMUIFGP54+9t4qri2XJlvvU8595GJqDYnexlT8+YiztvObZwR4/xpJcgdYwMEmxACmiOAIsBQwMjEwMHUwADBEBoAGi/N01oAAAA```"
            )}
        ], True)
        output = self.generator.generate(groundAssets, placeObjects)[0]["output"]
        self.assertEqual( expected, output, msg = "Output strings are different!")


    def test_terrainGenerationPlaceObject(self):
        expected = """```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```"""

        self.generator.setXYZ(20,20,20)
        self.generator.setOctaves(1, 0.5, 0.25)
        self.generator.setScales(1, 2, 4)
        self.generator.setExponent(1.5)
        self.generator.setUsePreciseHeight(True)
        self.generator.setUseRidgeNoise(False)
        
        groundAssets = Generator.createObjectList([
            {"asset" : "3911d10d-142b-4f33-9fea-5d3a10c53781"}
        ])

        placeObjects = Generator.createObjectList([
            {"asset" : AssetManager.addCustomAsset(
                "Tree_4",
                "```H4sIAAAAAAAACzv369xFJgZmBgYGV8sOe+Zcb6+FuwOFhA/vvMUIFGP54+9t4qri2XJlvvU8595GJqDYnexlT8+YiztvObZwR4/xpJcgdYwMEmxACmiOAIsBQwMjEwMHUwADBEBoAGi/N01oAAAA```"
            )}
        ], True)

        output = self.generator.generate(groundAssets, placeObjects)[0]["output"]
        self.assertEqual( expected, output, msg = "Output strings are different!")

    def test_rotation(self):
        expected = """```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```"""

        placeObject = AssetManager.getAsset(
            AssetManager.addCustomAsset(
                "Crypt",
                "```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```"
        ))

        self.generator.output = {
            "unique_asset_count": 0,
            "asset_data": {}
        }

        self.generator.place(placeObject, 0, 0, 0, 0)
        self.generator.place(placeObject, 0, 0, 10, 90)
        self.generator.place(placeObject, 0, 0, 20, 180)
        self.generator.place(placeObject, 0, 0, 30, 270)
        self.generator.place(placeObject, 0, 0, 40, 360)
        
        output = ConversionManager.encode(
                json.dumps(self.generator.output)
            ).decode("utf-8")
        self.assertEqual( expected, output, msg = "Output strings are different!")

    def test_fullOnePieceSmallTile(self):
        expected = """```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```"""

        self.generator.setXYZ(20,20,30)
        self.generator.setOctaves(1, 0.5, 0.25)
        self.generator.setScales(1, 2, 4)
        self.generator.setExponent(1.5)
        self.generator.setUsePreciseHeight(False)
        self.generator.setUseRidgeNoise(False)
        
        groundAssets = Generator.createObjectList([
            {"asset" : "cf6063bb-5c6e-4107-b3e9-9c0c5ac75768"}
        ])
        placeObjects = Generator.createObjectList([
            { "asset" : AssetManager.addCustomAsset(
                "Tree_3",
                "```H4sIAAAAAAAACzv369xFJgYWBgYGJ8kbgpNqqpxbpJeV8cZNqGMEirladtgz53p7LdwdKCR8eOctkBjLH39vE1cVz5Yr863nOfc2gsTuZC97esZc3HnLsYU7eownvQSJMTMIsAQAaTYGCTYgxcDIwMG0gQECIDQAM1rOhHwAAAA=```"),
                "density" : 10,
                "clumping" : 32,
                "randomNoiseWeight" : 0.8,
                "randomNudgeEnabled" : True,
                "randomRotationEnabled" : True,
                "heightBasedMultiplier" : 0.5,
                "heightBasedOffset" : 0
            },
            { "asset" : AssetManager.addCustomAsset(
                "Tree_2",
                "```H4sIAAAAAAAACzv369xFJgZmBgYGV8sOe+Zcb6+FuwOFhA/vvMUIFGP54+9t4qri2XJlvvU8595GkNid7GVPz5iLO285tnBHj/GklyAxLgYBFgYw4GBSYGRgBokpgAgGAJmdG+RgAAAA```"),
                "density" : 16,
                "clumping" : 16,
                "randomNoiseWeight" : 0.8,
                "randomNudgeEnabled" : True,
                "randomRotationEnabled" : True,
                "heightBasedMultiplier" : 0.5,
                "heightBasedOffset" : 0
            },
            { "asset" : AssetManager.addCustomAsset(
                "Tree_1",
                "```H4sIAAAAAAAACzv369xFJgYmBgYGV8sOe+Zcb6+FuwOFhA/vvMUIFLuTvezpGXNx5y3HFu7oMZ70EiTGz8ABUg4GE8AkAIf2hGVEAAAA```"),
                "density" : 10,
                "clumping" : 1,
                "randomNoiseWeight" : 0.8,
                "randomNudgeEnabled" : True,
                "randomRotationEnabled" : True,
                "heightBasedMultiplier" : 1,
                "heightBasedOffset" : 0
            },
            { "asset" : "98259887-53c2-41d4-a54f-6140b6acf020",
                "density" : 50,
                "clumping" : 3,
                "randomNoiseWeight" : 0.8,
                "randomNudgeEnabled" : False,
                "randomRotationEnabled" : True,
                "heightBasedMultiplier" : 1,
                "heightBasedOffset" : -10
            },
            { "asset" : "6ba81f8e-9a9c-4745-990f-2cb27bb29cfc",
                "density" : 20,
                "clumping" : 16,
                "randomNoiseWeight" : 1.0,
                "randomNudgeEnabled" : True,
                "randomRotationEnabled" : False,
                "heightBasedMultiplier" : 1,
                "heightBasedOffset" : -5
            }
        ], True)
        output = self.generator.generate(groundAssets, placeObjects)[0]["output"]

        self.assertEqual( expected, output, msg = "Output strings are different!")

    def test_fullManyPieces(self):
        expected = """```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```"""

        self.generator.setXYZ(20,20,30)
        self.generator.setOctaves(1, 0.5, 0.25)
        self.generator.setScales(1, 2, 4)
        self.generator.setExponent(1.5)
        self.generator.setUsePreciseHeight(False)
        self.generator.setUseRidgeNoise(False)
        
        groundAssets = Generator.createObjectList([
            {"asset" : "cf6063bb-5c6e-4107-b3e9-9c0c5ac75768"}
        ])
        placeObjects = Generator.createObjectList([
            { "asset" : AssetManager.addCustomAsset(
                "Tree_3",
                "```H4sIAAAAAAAACzv369xFJgYWBgYGJ8kbgpNqqpxbpJeV8cZNqGMEirladtgz53p7LdwdKCR8eOctkBjLH39vE1cVz5Yr863nOfc2gsTuZC97esZc3HnLsYU7eownvQSJMTMIsAQAaTYGCTYgxcDIwMG0gQECIDQAM1rOhHwAAAA=```"),
                "density" : 10,
                "clumping" : 32,
                "randomNoiseWeight" : 0.8,
                "randomNudgeEnabled" : True,
                "randomRotationEnabled" : True,
                "heightBasedMultiplier" : 0.5,
                "heightBasedOffset" : 0
            },
            { "asset" : AssetManager.addCustomAsset(
                "Tree_2",
                "```H4sIAAAAAAAACzv369xFJgZmBgYGV8sOe+Zcb6+FuwOFhA/vvMUIFGP54+9t4qri2XJlvvU8595GkNid7GVPz5iLO285tnBHj/GklyAxLgYBFgYw4GBSYGRgBokpgAgGAJmdG+RgAAAA```"),
                "density" : 16,
                "clumping" : 16,
                "randomNoiseWeight" : 0.8,
                "randomNudgeEnabled" : True,
                "randomRotationEnabled" : True,
                "heightBasedMultiplier" : 0.5,
                "heightBasedOffset" : 0
            },
            { "asset" : AssetManager.addCustomAsset(
                "Tree_1",
                "```H4sIAAAAAAAACzv369xFJgYmBgYGV8sOe+Zcb6+FuwOFhA/vvMUIFLuTvezpGXNx5y3HFu7oMZ70EiTGz8ABUg4GE8AkAIf2hGVEAAAA```"),
                "density" : 10,
                "clumping" : 1,
                "randomNoiseWeight" : 0.8,
                "randomNudgeEnabled" : True,
                "randomRotationEnabled" : True,
                "heightBasedMultiplier" : 1,
                "heightBasedOffset" : 0
            },
            { "asset" : "98259887-53c2-41d4-a54f-6140b6acf020",
                "density" : 50,
                "clumping" : 3,
                "randomNoiseWeight" : 0.8,
                "randomNudgeEnabled" : False,
                "randomRotationEnabled" : True,
                "heightBasedMultiplier" : 1,
                "heightBasedOffset" : -10
            },
            { "asset" : "6ba81f8e-9a9c-4745-990f-2cb27bb29cfc",
                "density" : 20,
                "clumping" : 16,
                "randomNoiseWeight" : 1.0,
                "randomNudgeEnabled" : True,
                "randomRotationEnabled" : False,
                "heightBasedMultiplier" : 1,
                "heightBasedOffset" : -5
            },
            { "asset" : AssetManager.addCustomAsset(
                "House",
                "```H4sIAAAAAAAACzv369xFJgZmBgYGV8sOe+Zcb6+FuwOFhA/vvMUIFGP54+9t4qri2XJlvvU8595GkNid7GVPz5iLO285tnBHj/GklyAxLgYBFgYw4GBSYGRgBokpgAgGAJmdG+RgAAAA```"),
                "density" : 20,
                "clumping" : 16,
                "randomNoiseWeight" : 1.0,
                "randomNudgeEnabled" : True,
                "randomRotationEnabled" : False,
                "heightBasedMultiplier" : 1,
                "heightBasedOffset" : -5
            }
        ], True)
        output = self.generator.generate(groundAssets, placeObjects, [3, 2])

        self.assertEqual( expected, output, msg = "Output strings are different!")

    

