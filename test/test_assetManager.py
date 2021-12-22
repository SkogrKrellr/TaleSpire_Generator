import unittest
import json
from classes.assetManager import AssetManager
from converter.conversionManager import ConversionManager

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
        Position:   x: 0.5 y: 0.5 z: 0.5 w: 0.0
        Rotation:   x: 0.0 y: 0.0 z: 0.0 w: 1.0
        Scale:      x: 1.0 y: 1.0 z: 1.0 w: 0.0
        mCenter:    x: 0.5 y: 0.25 z: 0.5 w: 0.0
        mExtent:    x: 0.5 y: 0.25 z: 0.5 w: 0.0
        """.strip()

        object = AssetManager.getAsset("32cfd208-c363-4434-b817-8ba59faeed17")

        result = object.__str__()

        self.assertMultiLineEqual(
            result, 
            expected
        )

    def test_addCustomAsset(self):

        customAssetUUID = AssetManager.addCustomAsset(
            "Tree",
            "```H4sIAAAAAAAACzv369xFJgZmBgaGe57nRebNPO24TLyae47AxiWMQDFXyw575lxvr4W7A4WED++8BRK7k73s6Rlzcectxxbu6DGe9BIkxsrAwZTAwMDMyCDAAuSCjGNoYGgASgEAg5LcWWAAAAA=```"
        )
        
        expected = f"""
        UUID: {customAssetUUID}
        Name: Tree
        Asset Name: Tree
        String: ```H4sIAAAAAAAACzv369xFJgZmBgaGe57nRebNPO24TLyae47AxiWMQDFXyw575lxvr4W7A4WED++8BRK7k73s6Rlzcectxxbu6DGe9BIkxsrAwZTAwMDMyCDAAuSCjGNoYGgASgEAg5LcWWAAAAA=```
        Position:   x: 0.0 y: 0.0 z: 0.0 w: 0.0
        Rotation:   x: 0.0 y: 0.0 z: 0.0 w: 0.0
        Scale:      x: 0.0 y: 0.0 z: 0.0 w: 0.0
        mCenter:    x: 0.025 y: 0.04 z: 0.0 w: 0.0
        mExtent:    x: 0.025 y: 0.04 z: 1.3 w: 0.0
        """.strip()

        object = AssetManager.getAsset(customAssetUUID)
        result = object.__str__()

        self.assertMultiLineEqual(
            result, 
            expected
        )

    def test_getCustomAsset(self):

        customAssetUUID = AssetManager.addCustomAsset(
            "Tree",
            "```H4sIAAAAAAAACzv369xFJgZmBgaGe57nRebNPO24TLyae47AxiWMQDFXyw575lxvr4W7A4WED++8BRK7k73s6Rlzcectxxbu6DGe9BIkxsDAwaQAJFkYBFgagDQrWKyBhYEBANfydP1gAAAA```"
        )

        expected = {
            '14cf49de-999e-41cb-a617-7b0b9c10b1a4': {'uuid': '14cf49de-999e-41cb-a617-7b0b9c10b1a4', 'instance_count': 1, 'instances': [{'x': 0, 'y': 2, 'z': 130, 'rot': 0}]}, 
            '3f883945-6d03-4a4b-a1bb-511213c3b9da': {'uuid': '3f883945-6d03-4a4b-a1bb-511213c3b9da', 'instance_count': 1, 'instances': [{'x': 4, 'y': 8, 'z': 260, 'rot': 0}]}, 
            'e5a66bdc-37cc-4317-b4c6-a1b88c3392e9': {'uuid': 'e5a66bdc-37cc-4317-b4c6-a1b88c3392e9', 'instance_count': 1, 'instances': [{'x': 5, 'y': 0, 'z': 0, 'rot': 270}]}
            }

        asset = AssetManager.getAsset(customAssetUUID)
        result = asset.getDecoded()

        self.assertDictEqual(
            result,
            expected
        )
