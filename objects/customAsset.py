import objects.assetManager
from objects.config import *
from objects.asset import Asset
from objects.quad import Quad
from converter.conversionManager import ConversionManager


class CustomAsset(Asset):
    """
    Class for a custom asset. This class extends asset.

    It has no aditional attributes when compared to its parent class
    """

    def __init__(
        self,
        object
    ):
        """
        Constructor for custom assets.

        In addition to parent classes constructor, it also calculates the
        dimensions (mesh Center and mesh Extents) of the current object.

        Parameters:
            object (dict): A dictionary of atributes for the asset.
        """

        Asset.__init__(self, object)
        if(
            self.mCenter == Quad(0, 0, 0, 0) or
            self.mExtent == Quad(0, 0, 0, 0)
        ):
            decoded = ConversionManager.decode(self.string)
            dictionary = decoded['asset_data']
            offset = {}
            extentsMax = {
                "x": 0,
                "y": 0,
                "z": 0,
            }
            for item in dictionary:
                uuid = str(item["uuid"])
                asset = objects.assetManager.AssetManager.getAsset(uuid)
                for placement in item["instances"]:
                    if placement["rot"] % 180 == 0:
                        offset["x"] = asset.mExtent.x
                        offset["y"] = asset.mExtent.z
                    else:
                        offset["x"] = asset.mExtent.z
                        offset["y"] = asset.mExtent.x

                    offset["x"] *= 2.0
                    offset["y"] *= 2.0

                    extentsMax["x"] = max(
                        (placement["x"]/100) + offset["x"],
                        extentsMax["x"]
                        )
                    extentsMax["y"] = max(
                        (placement["y"]/100) + offset["y"],
                        extentsMax["y"]
                        )
                    extentsMax["z"] = max(
                        placement["z"]/100,
                        extentsMax["z"]
                        )

            self.mCenter = Quad(
                (extentsMax["x"])/2,
                (extentsMax["y"])/2,
                0,
                0
            )

            self.mExtent = Quad(
                (extentsMax["x"])/2,
                (extentsMax["y"])/2,
                extentsMax["z"],
                0
            )

    def getDecoded(self):
        """
        Function for getting the decoded version of the asset string

        Returns:
            dict: A dictionary of assets and their positions
        """

        return ConversionManager.decode(self.string)["asset_data"]
