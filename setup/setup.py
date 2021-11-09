import json

from classes.database import Database
from classes.prop import Prop
from classes.tile import Tile
from classes.config import config as Config

def FirstTimeSetup() -> None:
    CreateTables()
    populateAssets()

def CreateTables():
    database = Database()

    database.execute(Tile.dropTableSql())
    database.execute(Tile.tableCreationSql())

    database.execute(Prop.dropTableSql())
    database.execute(Prop.tableCreationSql())

    database.close()

def populateAssets():
    jsonFile = open('etc/index.json')
    objects = json.load(jsonFile)
    jsonFile.close()

    database = Database()

    for object in objects["Tiles"]:
        tile = Tile(object)
        database.execute(tile.Sql())

    for object in objects["Props"]:
        prop = Prop(object)
        database.execute(prop.Sql())