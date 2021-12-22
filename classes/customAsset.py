from classes.config import *
from classes.asset import Asset
from classes.quad import Quad
from converter.conversionManager import ConversionManager

class CustomAsset(Asset):

    def __init__(self, object) -> None:
        Asset.__init__(self, object)
        if( self.mCenter == Quad(0, 0, 0, 0) or self.mExtent == Quad(0, 0, 0, 0) ):
            dictionary = ConversionManager.decode(self.string)["asset_data"]
            extents = {
                "x" : 0, 
                "y" : 0, 
                "z" : 0, 
            }
            for uuid, values in dictionary.items():
                for placement in values["instances"]:
                    extents["x"] = max(placement["x"]/100, extents["x"])
                    extents["y"] = max(placement["y"]/100, extents["y"])
                    extents["z"] = max(placement["z"]/100, extents["z"])

            self.mCenter = Quad(
                extents["x"]/2,
                extents["y"]/2,
                0,
                0
            )

            self.mExtent = Quad(
                extents["x"]/2,
                extents["y"]/2,
                extents["z"]/2,
                0
            )
 
    def getDecoded( self ):
        return ConversionManager.decode(self.string)["asset_data"]

