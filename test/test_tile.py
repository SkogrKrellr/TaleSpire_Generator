import unittest
import json
from classes.assetManager import AssetManager
from classes.tile import Tile

class TestTile(unittest.TestCase):

    @classmethod
    def setUpClass(self) -> None:
        print("\nTiles: " ,end = '')
        self.maxDiff = None
        self.tile = Tile(
            AssetManager.remap(json.loads(
                '{"Id":"32cfd208-c363-4434-b817-8ba59faeed17","Name":"Castle Floor 1","Assets":[{"LoaderData":{"AssetName":"Castle01_floor_1x1_low"},"Position":{"x":0.5,"y":0.5,"z":0.5},"Rotation":{"x":0,"y":0,"z":0,"w":1},"Scale":{"x":1,"y":1,"z":1}}],"ColliderBoundsBound":{"m_Center":{"x":0.5,"y":0.25,"z":0.5},"m_Extent":{"x":0.5,"y":0.25,"z":0.5}}}'
                )
            )
        )

    def test_str(self):
        expected = f"""
        UUID: 32cfd208-c363-4434-b817-8ba59faeed17
        Name: Castle Floor 1
        Asset Name: Castle01_floor_1x1_low
        String: 
        Position:   x: 0.5 y: 0.5 z: 0.5 w: 0
        Rotation:   x: 0 y: 0 z: 0 w: 1
        Scale:      x: 1 y: 1 z: 1 w: 0
        mCenter:    x: 0.5 y: 0.25 z: 0.5 w: 0
        mExtent:    x: 0.5 y: 0.25 z: 0.5 w: 0
        """.strip()
        self.assertMultiLineEqual(
            expected,
            self.tile.__str__()
        )