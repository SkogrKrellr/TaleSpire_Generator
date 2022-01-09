import unittest

from objects.asset import Asset


class TestAsset(unittest.TestCase):

    @classmethod
    def setUpClass(self) -> None:
        print("\nAsset: ", end='')

    def test_SqlCreateTable(self):
        expected = """
        CREATE TABLE Assets (
            UUID tinytext PRIMARY KEY,
            Type tinytext NOT NULL,
            Name tinytext NOT NULL,
            AssetName tinytext NOT NULL,
            String text NULL,
            Position_x FLOAT(24),
            Position_y FLOAT(24),
            Position_z FLOAT(24),
            Position_w FLOAT(24),
            Rotation_x FLOAT(24),
            Rotation_y FLOAT(24),
            Rotation_z FLOAT(24),
            Rotation_w FLOAT(24),
            Scale_x FLOAT(24),
            Scale_y FLOAT(24),
            Scale_z FLOAT(24),
            Scale_w FLOAT(24),
            mCenter_x FLOAT(24),
            mCenter_y FLOAT(24),
            mCenter_z FLOAT(24),
            mCenter_w FLOAT(24),
            mExtent_x FLOAT(24),
            mExtent_y FLOAT(24),
            mExtent_z FLOAT(24),
            mExtent_w FLOAT(24)
        );
        """.replace("    ", "").strip()
        self.assertMultiLineEqual(
            expected,
            Asset.SqlCreateTable()
        )

    def test_SqlDropTable(self):
        expected = """DROP TABLE IF EXISTS Assets;"""
        self.assertMultiLineEqual(
            expected,
            Asset.SqlDropTable()
        )

    def test_SqlGetAsset(self):
        expected = """SELECT * FROM Assets WHERE UUID = 'TEST-UUID';"""
        self.assertMultiLineEqual(
            expected,
            Asset.SqlGetAsset("TEST-UUID")
        )

    def test_SqlDeleteAsset(self):
        expected = """DELETE FROM Assets WHERE UUID = 'TEST-UUID';"""
        self.assertMultiLineEqual(
            expected,
            Asset.SqlDeleteAsset("TEST-UUID")
        )
