import unittest
import json
from classes.asset_manager import AssetManager
from converter.conversion_manager import ConversionManager

class TestAssetManager(unittest.TestCase):
    
    @classmethod
    def setUpClass(self) -> None:
        self.maxDiff = None
        print("\nAssetManager: " ,end = '')

    def test_getAsset(self):
        expected = f"""
                    UUID: 32cfd208-c363-4434-b817-8ba59faeed17
                    Name: Castle Floor 1
                    Asset Name: Castle01_floor_1x1_low
                    String: 
                    Position:   x: 0.5 y: 0.5 z: 0.5 w: 0
                    Rotation:   x: 0.0 y: 0.0 z: 0.0 w: 1.0
                    Scale:      x: 1.0 y: 1.0 z: 1.0 w: 0
                    mCenter:    x: 0.5 y: 0.25 z: 0.5 w: 0
                    mExtent:    x: 0.5 y: 0.25 z: 0.5 w: 0
                    """.strip()

        object = AssetManager.getAsset("32cfd208-c363-4434-b817-8ba59faeed17")

        result = object.__str__()

        self.assertMultiLineEqual(
            result, 
            expected
        )

    def atest_addCustomAsset(self):


        customAssetUUID = AssetManager.addCustomAsset(
            "Tree",
            "```H4sIAAAAAAAACzv369xFJgZmBgaGe57nRebNPO24TLyae47AxiWMQDFXyw575lxvr4W7A4WED++8BRK7k73s6Rlzcectxxbu6DGe9BIkxsDAwaQAJFkYBFgagDQrWKyBhYEBANfydP1gAAAA```"
        )

        object = AssetManager.getAsset(customAssetUUID)
        print(object, customAssetUUID)
        pass