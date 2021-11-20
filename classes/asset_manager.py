from classes.asset import Asset
from classes.tile import Tile
from classes.prop import Prop
from classes.database import Database
import setup.setup as Setup

class AssetManager():

    def __init__ (self):
        self.database = Database()

    def getAsset(self, uuid):
        object = self.database.fetchall(Asset.SqlGetAsset(uuid))

        assetDictionary = Setup.remap(object[0], True)
        className= globals()[assetDictionary["Type"]]
        
        asset = className(assetDictionary)
        return asset

    def addCustomAsset():
        pass #TODO