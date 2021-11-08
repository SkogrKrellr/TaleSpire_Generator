import unittest
from classes.quad import Quad

class TestQuad(unittest.TestCase):

    @classmethod
    def setUpClass(self) -> None:
        self.quad = Quad(0,0.25,0.5,1)

    def test_str(self):
        self.assertEqual(self.quad.__str__(), "x: 0 y: 0.25 z: 0.5 w: 1")

    def test_toSql(self):
        self.assertEqual(self.quad.Sql(), "0, 0.25, 0.5, 1")

    def test_toSqlValues(self):
        self.assertEqual(Quad.SqlValues(), "_x, _y, _z, _w")
        self.assertEqual(Quad.SqlValues("foobar"), "foobar_x, foobar_y, foobar_z, foobar_w")

    def test_tableCreationSql(self):
        self.assertEqual(Quad.tableCreationSql(), "_x FLOAT(24), _y FLOAT(24), _z FLOAT(24), _w FLOAT(24)")
        self.assertEqual(Quad.tableCreationSql("foobar"), "foobar_x FLOAT(24), foobar_y FLOAT(24), foobar_z FLOAT(24), foobar_w FLOAT(24)")