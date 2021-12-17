import unittest
import json
from classes.asset_manager import AssetManager
from classes.prop import Prop

class TestProp(unittest.TestCase):
    
    @classmethod
    def setUpClass(self) -> None:
        print("\nProp: " ,end = '')
        self.maxDiff = None
        self.prop = Prop(
            AssetManager.remap(json.loads(
                '{"Id":"6e22a681-4902-4cc4-a5f2-2284fb3c53b6","Name":"Campfire","IsDeprecated":false,"GroupTag":"campfire","Tags":["1x1","campfire","illuminated","light","lit","fire","wood","stone","brown","grey","gray","rest","cooking","glow","glowing","travelling","small","camping","camp"],"Assets":[{"LoaderData":{"BundleId":"otr_vfx_fire01_1468140860","AssetName":"VFX_SmallFire"},"Position":{"x":0.020799368619918823,"y":0.29339998960494995,"z":0.04866328835487366},"Rotation":{"x":0,"y":0,"z":0,"w":1},"Scale":{"x":0.93205726146698,"y":0.93205726146698,"z":0.93205726146698}},{"LoaderData":{"BundleId":"tileset_lightingset_1471790033","AssetName":"Campfire_logs"},"Position":{"x":0.004819363355636597,"y":0,"z":0.1010565459728241},"Rotation":{"x":0,"y":0,"z":0,"w":1},"Scale":{"x":1,"y":1,"z":1}}],"IsInteractable":false,"ColliderBoundsBound":{"m_Center":{"x":0,"y":0.3435215950012207,"z":0},"m_Extent":{"x":0.38203075528144836,"y":0.34022027254104614,"z":0.36165329813957214}},"Icon":{"AtlasIndex":0,"Region":{"serializedVersion":"2","x":0.5,"y":0.6875,"width":0.0625,"height":0.0625}}}'
                )
            )
        )

    def test_str(self):
        expected = f"""
        UUID: 6e22a681-4902-4cc4-a5f2-2284fb3c53b6
        Name: Campfire
        Asset Name: VFX_SmallFire
        String: 
        Position:   x: 0.020799368619918823 y: 0.29339998960494995 z: 0.04866328835487366 w: 0
        Rotation:   x: 0 y: 0 z: 0 w: 1
        Scale:      x: 0.93205726146698 y: 0.93205726146698 z: 0.93205726146698 w: 0
        mCenter:    x: 0 y: 0.3435215950012207 z: 0 w: 0
        mExtent:    x: 0.38203075528144836 y: 0.34022027254104614 z: 0.36165329813957214 w: 0
        """.strip()

        self.assertMultiLineEqual(
            expected,
            self.prop.__str__()
        )
        