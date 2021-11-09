import unittest
import json
from classes.prop import Prop

class TestAsset(unittest.TestCase):

    @classmethod
    def setUpClass(self) -> None:
        self.maxDiff = None
        self.prop = Prop(json.loads('{"Id":"32cfd208-c363-4434-b817-8ba59faeed17","Name":"Castle Floor 1","Assets":[{"LoaderData":{"AssetName":"Castle01_floor_1x1_low"},"Position":{"x":0.5,"y":0.5,"z":0.5},"Rotation":{"x":0,"y":0,"z":0,"w":1},"Scale":{"x":1,"y":1,"z":1}}],"ColliderBoundsBound":{"m_Center":{"x":0.5,"y":0.25,"z":0.5},"m_Extent":{"x":0.5,"y":0.25,"z":0.5}}}'))

    def test_str(self):
        self.assertMultiLineEqual(
            self.prop.__str__(), 
            """UUID: 32cfd208-c363-4434-b817-8ba59faeed17
            Name: Castle Floor 1
            Asset Name: Castle01_floor_1x1_low
            Position:   x: 0.5 y: 0.5 z: 0.5 w: 0
            Rotation:   x: 0 y: 0 z: 0 w: 1
            Scale:      x: 1 y: 1 z: 1 w: 0
            mCenter:    x: 0.5 y: 0.25 z: 0.5 w: 0
            mExtent:    x: 0.5 y: 0.25 z: 0.5 w: 0
            """.strip()
        )

    def test_toSql(self):
        self.assertMultiLineEqual(
            self.prop.Sql(),
            """
            INSERT INTO props 
            (UUID,
            Name,
            AssetName,
            Position_x, Position_y, Position_z, Position_w,
            Rotation_x, Rotation_y, Rotation_z, Rotation_w,
            Scale_x, Scale_y, Scale_z, Scale_w,
            mCenter_x, mCenter_y, mCenter_z, mCenter_w,
            mExtent_x, mExtent_y, mExtent_z, mExtent_w)
            VALUES(
                "32cfd208-c363-4434-b817-8ba59faeed17", 
                "Castle Floor 1", 
                "Castle01_floor_1x1_low", 
                0.5, 0.5, 0.5, 0, 
                0, 0, 0, 1,
                1, 1, 1, 0,
                0.5, 0.25, 0.5, 0,
                0.5, 0.25, 0.5, 0
            );""".strip()
        )

    def test_toSqlValues(self):
        self.assertMultiLineEqual(
            Prop.SqlValues(),
            """UUID,
            Name,
            AssetName,
            Position_x, Position_y, Position_z, Position_w,
            Rotation_x, Rotation_y, Rotation_z, Rotation_w,
            Scale_x, Scale_y, Scale_z, Scale_w,
            mCenter_x, mCenter_y, mCenter_z, mCenter_w,
            mExtent_x, mExtent_y, mExtent_z, mExtent_w
            """.strip()
        )

    def test_tableCreationSql(self):
        self.assertMultiLineEqual(
            Prop.tableCreationSql(), 
            """CREATE TABLE props (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            UUID tinytext NOT NULL,
            Name tinytext NOT NULL,
            AssetName tinytext NOT NULL,
            Position_x FLOAT(24), Position_y FLOAT(24), Position_z FLOAT(24), Position_w FLOAT(24),
            Rotation_x FLOAT(24), Rotation_y FLOAT(24), Rotation_z FLOAT(24), Rotation_w FLOAT(24),
            Scale_x FLOAT(24), Scale_y FLOAT(24), Scale_z FLOAT(24), Scale_w FLOAT(24),
            mCenter_x FLOAT(24), mCenter_y FLOAT(24), mCenter_z FLOAT(24), mCenter_w FLOAT(24),
            mExtent_x FLOAT(24), mExtent_y FLOAT(24), mExtent_z FLOAT(24), mExtent_w FLOAT(24));
            """.strip()
        )
    
    def test_dropTableSql(self):
        self.assertMultiLineEqual(
            Prop.dropTableSql(), 
            """ DROP TABLE IF EXISTS props;""".strip()
        )