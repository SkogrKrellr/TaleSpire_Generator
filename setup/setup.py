import json
from os import name

from classes.asset import Asset
from classes.asset_manager import AssetManager
from classes.prop import Prop
from classes.tile import Tile
from classes.customAsset import CustomAsset
from classes.database import Database

def FirstTimeSetup() -> None:
    CreateTables()
    populateAssets()

def CreateTables():
    database = Database()

    database.execute( Asset.SqlDropTable() )
    database.execute( Asset.SqlCreateTable() )

    database.close()

def populateAssets():

    database = Database()

    jsonFile = open('etc/index.json')
    objects = json.load(jsonFile)
    jsonFile.close()

    sqlQuerry = ""

    for object in objects["Tiles"]:
        tile = Tile(AssetManager.remap(object))
        sqlQuerry += tile.SqlValues()
        
    for object in objects["Props"]:
        prop = Prop(AssetManager.remap(object))
        sqlQuerry += prop.SqlValues()

    database.executeScript(sqlQuerry)
    database.close()