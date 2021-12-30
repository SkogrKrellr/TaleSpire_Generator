import json
import unittest

from converter.conversionManager import ConversionManager


class TestEncodeDecode(unittest.TestCase):
    
    @classmethod
    def setUpClass(self) -> None:
        self.maxDiff = None
        print("\nEncode/Decode: ", end='')
        self.encoded = "```H4sIAAAAAAAC/1WRIU8DQRCFh2vSIKpqmlNXU3UnmktFZUV/A0HgQPIjEOeaJidxKBQBjVhBgllMCSRY/kENWYXi3u53pF3zMu/Nm9m82f3uPjLLzOzi9vpxs/1ZP3zt377PtvNFx51+vteXr4v182Rzf/e0n8zt+L2MwTLhaml2hSZcDRPejOBz+AJ+llD+qNfo3RzPHM8eT191knih5gqlR+z1bk5Ln1D/aOlv6Y96jl7Al/CdP6AL9c+AHg50/fM8S3uE2iPUnsjn1J3fwbuDWv7pIPmF0oX6X+Rz+FlC9TeDtKdBb9CF/3cYJtQ8I3cjdyN3O8i7z1c+j8/j8/g8Po/Pc6eKfCvyqsizIreKnFrqljpwn4A/cJ/AfQJzlJ/qmG9fl+Rbwy9TnnqOOzh8jjs4/A6/wz8lz4gF+ZfkX5OzkfOInMfcoUCnT/8w+wPbqNAXVAMAAA==```"

        self.decoded = {
            "unique_asset_count": 2,
            "asset_data": {
                "ad6c985c-8d8b-44f2-abd5-edc9de568d30": {
                    "uuid": "ad6c985c-8d8b-44f2-abd5-edc9de568d30",
                    "instance_count": 52,
                    "instances": [
                        {"x": 0, "y": 0, "z": 0, "rot": 0},
                        {"x": 0, "y": 300, "z": 0, "rot": 0},
                        {"x": 0, "y": 700, "z": 0, "rot": 0},
                        {"x": 0, "y": 900, "z": 0, "rot": 0},
                        {"x": 100, "y": 0, "z": 0, "rot": 0},
                        {"x": 100, "y": 100, "z": 0, "rot": 0},
                        {"x": 100, "y": 200, "z": 0, "rot": 0},
                        {"x": 100, "y": 400, "z": 0, "rot": 0},
                        {"x": 100, "y": 500, "z": 0, "rot": 0},
                        {"x": 100, "y": 600, "z": 0, "rot": 0},
                        {"x": 100, "y": 700, "z": 0, "rot": 0},
                        {"x": 100, "y": 800, "z": 0, "rot": 0},
                        {"x": 100, "y": 900, "z": 0, "rot": 0},
                        {"x": 200, "y": 0, "z": 0, "rot": 0},
                        {"x": 200, "y": 300, "z": 0, "rot": 0},
                        {"x": 200, "y": 700, "z": 0, "rot": 0},
                        {"x": 300, "y": 0, "z": 0, "rot": 0},
                        {"x": 300, "y": 200, "z": 0, "rot": 0},
                        {"x": 300, "y": 300, "z": 0, "rot": 0},
                        {"x": 300, "y": 700, "z": 0, "rot": 0},
                        {"x": 300, "y": 800, "z": 0, "rot": 0},
                        {"x": 400, "y": 0, "z": 0, "rot": 0},
                        {"x": 400, "y": 100, "z": 0, "rot": 0},
                        {"x": 400, "y": 200, "z": 0, "rot": 0},
                        {"x": 400, "y": 300, "z": 0, "rot": 0},
                        {"x": 400, "y": 400, "z": 0, "rot": 0},
                        {"x": 400, "y": 500, "z": 0, "rot": 0},
                        {"x": 400, "y": 700, "z": 0, "rot": 0},
                        {"x": 400, "y": 800, "z": 0, "rot": 0},
                        {"x": 500, "y": 400, "z": 0, "rot": 0},
                        {"x": 500, "y": 600, "z": 0, "rot": 0},
                        {"x": 500, "y": 700, "z": 0, "rot": 0},
                        {"x": 500, "y": 800, "z": 0, "rot": 0},
                        {"x": 500, "y": 900, "z": 0, "rot": 0},
                        {"x": 600, "y": 0, "z": 0, "rot": 0},
                        {"x": 600, "y": 100, "z": 0, "rot": 0},
                        {"x": 600, "y": 200, "z": 0, "rot": 0},
                        {"x": 600, "y": 400, "z": 0, "rot": 0},
                        {"x": 600, "y": 600, "z": 0, "rot": 0},
                        {"x": 700, "y": 200, "z": 0, "rot": 0},
                        {"x": 700, "y": 600, "z": 0, "rot": 0},
                        {"x": 700, "y": 900, "z": 0, "rot": 0},
                        {"x": 800, "y": 0, "z": 0, "rot": 0},
                        {"x": 800, "y": 200, "z": 0, "rot": 0},
                        {"x": 800, "y": 300, "z": 0, "rot": 0},
                        {"x": 800, "y": 400, "z": 0, "rot": 0},
                        {"x": 800, "y": 600, "z": 0, "rot": 0},
                        {"x": 800, "y": 900, "z": 0, "rot": 0},
                        {"x": 900, "y": 100, "z": 0, "rot": 0},
                        {"x": 900, "y": 400, "z": 0, "rot": 0},
                        {"x": 900, "y": 600, "z": 0, "rot": 0},
                        {"x": 900, "y": 700, "z": 0, "rot": 0},
                    ],
                },
                "32cfd208-c363-4434-b817-8ba59faeed17": {
                    "uuid": "32cfd208-c363-4434-b817-8ba59faeed17",
                    "instance_count": 48,
                    "instances": [
                        {"x": 0, "y": 100, "z": 0, "rot": 0},
                        {"x": 0, "y": 200, "z": 0, "rot": 0},
                        {"x": 0, "y": 400, "z": 0, "rot": 0},
                        {"x": 0, "y": 500, "z": 0, "rot": 0},
                        {"x": 0, "y": 600, "z": 0, "rot": 0},
                        {"x": 0, "y": 800, "z": 0, "rot": 0},
                        {"x": 100, "y": 300, "z": 0, "rot": 0},
                        {"x": 200, "y": 100, "z": 0, "rot": 0},
                        {"x": 200, "y": 200, "z": 0, "rot": 0},
                        {"x": 200, "y": 400, "z": 0, "rot": 0},
                        {"x": 200, "y": 500, "z": 0, "rot": 0},
                        {"x": 200, "y": 600, "z": 0, "rot": 0},
                        {"x": 200, "y": 800, "z": 0, "rot": 0},
                        {"x": 200, "y": 900, "z": 0, "rot": 0},
                        {"x": 300, "y": 100, "z": 0, "rot": 0},
                        {"x": 300, "y": 400, "z": 0, "rot": 0},
                        {"x": 300, "y": 500, "z": 0, "rot": 0},
                        {"x": 300, "y": 600, "z": 0, "rot": 0},
                        {"x": 300, "y": 900, "z": 0, "rot": 0},
                        {"x": 400, "y": 600, "z": 0, "rot": 0},
                        {"x": 400, "y": 900, "z": 0, "rot": 0},
                        {"x": 500, "y": 0, "z": 0, "rot": 0},
                        {"x": 500, "y": 100, "z": 0, "rot": 0},
                        {"x": 500, "y": 200, "z": 0, "rot": 0},
                        {"x": 500, "y": 300, "z": 0, "rot": 0},
                        {"x": 500, "y": 500, "z": 0, "rot": 0},
                        {"x": 600, "y": 300, "z": 0, "rot": 0},
                        {"x": 600, "y": 500, "z": 0, "rot": 0},
                        {"x": 600, "y": 700, "z": 0, "rot": 0},
                        {"x": 600, "y": 800, "z": 0, "rot": 0},
                        {"x": 600, "y": 900, "z": 0, "rot": 0},
                        {"x": 700, "y": 0, "z": 0, "rot": 0},
                        {"x": 700, "y": 100, "z": 0, "rot": 0},
                        {"x": 700, "y": 300, "z": 0, "rot": 0},
                        {"x": 700, "y": 400, "z": 0, "rot": 0},
                        {"x": 700, "y": 500, "z": 0, "rot": 0},
                        {"x": 700, "y": 700, "z": 0, "rot": 0},
                        {"x": 700, "y": 800, "z": 0, "rot": 0},
                        {"x": 800, "y": 100, "z": 0, "rot": 0},
                        {"x": 800, "y": 500, "z": 0, "rot": 0},
                        {"x": 800, "y": 700, "z": 0, "rot": 0},
                        {"x": 800, "y": 800, "z": 0, "rot": 0},
                        {"x": 900, "y": 0, "z": 0, "rot": 0},
                        {"x": 900, "y": 200, "z": 0, "rot": 0},
                        {"x": 900, "y": 300, "z": 0, "rot": 0},
                        {"x": 900, "y": 500, "z": 0, "rot": 0},
                        {"x": 900, "y": 800, "z": 0, "rot": 0},
                        {"x": 900, "y": 900, "z": 0, "rot": 0},
                    ],
                },
            },
        }

    def test_encode(self) -> None:
        generated = ConversionManager.encode(
            json.dumps(self.decoded)
            ).decode('ascii')
        self.assertEqual(generated, self.encoded)

    def atest_decode(self):
        output = ConversionManager.decode(self.encoded)
        self.assertDictEqual(self.decoded, output)
