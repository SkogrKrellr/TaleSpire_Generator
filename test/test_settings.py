import unittest
from settings.settings import Settings
from settings.placeObjectSettings import PlaceObjectSettings
from settings.terrainSettings import TerrainSettings


class TestSettings(unittest.TestCase):

    @classmethod
    def setUpClass(self) -> None:
        print("\nSettings: ", end='')
        self.terrainSettings = TerrainSettings({
            "asset": "3911d10d-142b-4f33-9fea-5d3a10c53781",
            "density": 35,
            "clumping": 11,
            "heightMin": 12,
            "heightMax": 57,
            "blendHeightMultiplier": 1.0
        }
        )
        self.placeObjectSettings = PlaceObjectSettings({
            "asset": "3911d10d-142b-4f33-9fea-5d3a10c53781",
            "clumping": 23,
            "density": 20,
            "clumping": 12,
            "randomNoiseWeight": 0.5,
            "randomNudgeEnabled": True,
            "randomRotationEnabled": True,
            "heightBasedMultiplier": 1.0,
            "heightBasedOffset": -7
            }
        )

    def test_str(self):
        expected = """
        asset: 3911d10d-142b-4f33-9fea-5d3a10c53781
        density: 35
        clumping: 11
        heightMin: 12
        heightMax: 57
        blendHeightMultiplier: 1.0
        """.replace("    ", "").strip()
        self.assertMultiLineEqual(
            self.terrainSettings.__str__(),
            expected
        )

        expected = """
        asset: 3911d10d-142b-4f33-9fea-5d3a10c53781
        density: 20
        clumping: 12
        randomNoiseWeight: 0.5
        randomNudgeEnabled: True
        randomRotationEnabled: True
        heightBasedMultiplier: 1.0
        heightBasedOffset: -7
        """.replace("    ", "").strip()
        self.assertMultiLineEqual(
            self.placeObjectSettings.__str__(),
            expected
        )

    def test_getParams(self):
        expected = {
            'asset': '3911d10d-142b-4f33-9fea-5d3a10c53781',
            'density': 35,
            'clumping': 11,
            'heightMin': 12,
            'heightMax': 57,
            'blendHeightMultiplier': 1.0
        }
        self.assertDictEqual(
            self.terrainSettings.getParam(),
            expected
        )

        expected = "3911d10d-142b-4f33-9fea-5d3a10c53781"
        self.assertEqual(
            self.terrainSettings.getParam("asset"),
            expected
        )

        expected = None
        self.assertEqual(
            self.terrainSettings.getParam("NonExistantTag"),
            expected
        )
