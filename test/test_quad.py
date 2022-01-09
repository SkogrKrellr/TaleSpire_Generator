import unittest
from objects.quad import Quad


class TestQuad(unittest.TestCase):

    @classmethod
    def setUpClass(self) -> None:
        print("\nQuad: ", end='')
        self.quad = Quad(0, 0.25, 0.5, 1)

    def test_str(self):
        self.assertEqual(
            self.quad.__str__(),
            "x: 0 y: 0.25 z: 0.5 w: 1"
        )

    def test_sqlValues(self):
        self.assertEqual(
            self.quad.SqlValues(),
            "0, 0.25, 0.5, 1"
        )

    def test_sqlFieldNames(self):
        self.assertEqual(
            Quad.SqlFieldNames(),
            "_x, _y, _z, _w"
        )
        self.assertEqual(
            Quad.SqlFieldNames("Prefix"),
            "Prefix_x, Prefix_y, Prefix_z, Prefix_w"
        )

    def test_SqlCreateTableFields(self):
        self.assertMultiLineEqual(
            Quad.SqlCreateFields(),
            """
            _x FLOAT(24),
            _y FLOAT(24),
            _z FLOAT(24),
            _w FLOAT(24)
            """.replace("    ", "").strip()
        )
        self.assertMultiLineEqual(
            Quad.SqlCreateFields("Prefix"),
            """
            Prefix_x FLOAT(24),
            Prefix_y FLOAT(24),
            Prefix_z FLOAT(24),
            Prefix_w FLOAT(24)
            """.replace("    ", "").strip()
        )
