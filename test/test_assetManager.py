import unittest
import json
from classes.asset_manager import AssetManager

class TestAssetManager(unittest.TestCase):
    
    @classmethod
    def setUpClass(self) -> None:
        print("\nAssetManager: " ,end = '')
        self.assetManager = AssetManager()

    def test_getAsset(self):
        object = self.assetManager.getAsset("32cfd208-c363-4434-b817-8ba59faeed17")
        self.assertMultiLineEqual(
            object.__str__(), 
            """UUID: 32cfd208-c363-4434-b817-8ba59faeed17
            Name: Castle Floor 1
            Asset Name: Castle01_floor_1x1_low
            Position:   x: 0.5 y: 0.5 z: 0.5 w: 0
            Rotation:   x: 0.0 y: 0.0 z: 0.0 w: 1.0
            Scale:      x: 1.0 y: 1.0 z: 1.0 w: 0
            mCenter:    x: 0.5 y: 0.25 z: 0.5 w: 0
            mExtent:    x: 0.5 y: 0.25 z: 0.5 w: 0
            """.strip()
        )