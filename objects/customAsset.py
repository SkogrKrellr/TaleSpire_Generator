import objects.assetManager
from objects.config import *
from objects.asset import Asset
from objects.quad import Quad
from converter.conversionManager import ConversionManager

class CustomAsset(Asset):

    def __init__(self, object) -> None:
        Asset.__init__(self, object)
        if( self.mCenter == Quad(0, 0, 0, 0) or self.mExtent == Quad(0, 0, 0, 0) ):
            decoded = ConversionManager.decode(self.string)
            dictionary = decoded['asset_data']
            offset= {}
            
            extentsMax = {
                "x" : 0, 
                "y" : 0, 
                "z" : 0, 
            }
            for item in dictionary:
                asset = objects.assetManager.AssetManager.getAsset(str(item["uuid"]).lower())
                for placement in item["instances"]:
                    if placement["rot"] % 180 == 0:
                        offset["x"] = asset.mExtent.x  
                        offset["y"] = asset.mExtent.z
                    else:
                        offset["x"] = asset.mExtent.z
                        offset["y"] = asset.mExtent.x

                    offset["x"] *= 2.0
                    offset["y"] *= 2.0

                    extentsMax["x"] = max((placement["x"]/100) + offset["x"], extentsMax["x"])
                    extentsMax["y"] = max((placement["y"]/100) + offset["y"], extentsMax["y"])
                    extentsMax["z"] = max(placement["z"]/100, extentsMax["z"])

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

    def getDecoded( self ):
        return ConversionManager.decode(self.string)["asset_data"]

