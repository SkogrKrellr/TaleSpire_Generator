import unittest
import json
from objects.assetManager import AssetManager

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

    def atest_addCustomAsset(self):

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
        mCenter:    x: 1.281880145072937 y: 1.2120859622955322 z: 0.0 w: 0.0
        mExtent:    x: 1.281880145072937 y: 1.2120859622955322 z: 2.6 w: 0.0
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
        asset = AssetManager.getAsset(customAssetUUID)
        result = asset.getDecoded()
        
        expected = [
            {'uuid': '14CF49DE-999E-41CB-A617-7B0B9C10B1A4', 'instance_count': 1, 'instances': [{'x': 0, 'y': 2, 'z': 130, 'rot': 0}]},
            {'uuid': '3F883945-6D03-4A4B-A1BB-511213C3B9DA', 'instance_count': 1, 'instances': [{'x': 4, 'y': 8, 'z': 260, 'rot': 0}]}, 
            {'uuid': 'E5A66BDC-37CC-4317-B4C6-A1B88C3392E9', 'instance_count': 1, 'instances': [{'x': 5, 'y': 0, 'z': 0, 'rot': 270}]},
        ]

        self.assertListEqual(
            result,
            expected
        )
