import json
from os import name

from classes.asset import Asset
from classes.prop import Prop
from classes.tile import Tile
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
    jsonFile = open('etc/index.json')
    objects = json.load(jsonFile)
    jsonFile.close()

    database = Database()

    for object in objects["Tiles"]:
        tile = Tile(remap(object))
        database.execute(tile.SqlValues())

    for object in objects["Props"]:
        prop = Prop(remap(object))
        database.execute(prop.SqlValues())

    database.close()

def remap(object, fromDB=False):

    result = {}
    result["Position"] = {}
    result["Rotation"] = {}
    result["Scale"] = {}
    result["mCenter"] = {}
    result["mExtent"] = {}

    if fromDB :
        result["UUID"] = object[0]
        result["Type"] = object[1]
        result["Name"] = object[2]
        result["AssetName"] = object[3]
        
        result["Position"]["x"] = object[4]
        result["Position"]["y"] = object[5]
        result["Position"]["z"] = object[6]
        result["Position"]["w"] = 0

        result["Rotation"]["x"] = object[8]
        result["Rotation"]["y"] = object[9]
        result["Rotation"]["z"] = object[10]
        result["Rotation"]["w"] = object[11]

        result["Scale"]["x"] = object[12]
        result["Scale"]["y"] = object[13]
        result["Scale"]["z"] = object[14]
        result["Scale"]["w"] = 0

        result["mCenter"]["x"] = object[16]
        result["mCenter"]["y"] = object[17]
        result["mCenter"]["z"] = object[18]
        result["mCenter"]["w"] = 0

        result["mExtent"]["x"] = object[20]
        result["mExtent"]["y"] = object[21]
        result["mExtent"]["z"] = object[22]
        result["mExtent"]["w"] = 0

        return result
    
    result["UUID"] = object["Id"]
    result["Name"] = object["Name"]
    result["AssetName"] = object["Assets"][0]["LoaderData"]["AssetName"]
    
    result["Position"]["x"] = object["Assets"][0]["Position"]["x"]
    result["Position"]["y"] = object["Assets"][0]["Position"]["y"]
    result["Position"]["z"] = object["Assets"][0]["Position"]["z"]
    result["Position"]["w"] = 0

    result["Rotation"]["x"] = object["Assets"][0]["Rotation"]["x"]
    result["Rotation"]["y"] = object["Assets"][0]["Rotation"]["y"]
    result["Rotation"]["z"] = object["Assets"][0]["Rotation"]["z"]
    result["Rotation"]["w"] = object["Assets"][0]["Rotation"]["w"]

    result["Scale"]["x"] = object["Assets"][0]["Scale"]["x"]
    result["Scale"]["y"] = object["Assets"][0]["Scale"]["y"]
    result["Scale"]["z"] = object["Assets"][0]["Scale"]["z"]
    result["Scale"]["w"] = 0

    result["mCenter"]["x"] = object["ColliderBoundsBound"]["m_Center"]["x"]
    result["mCenter"]["y"] = object["ColliderBoundsBound"]["m_Center"]["y"]
    result["mCenter"]["z"] = object["ColliderBoundsBound"]["m_Center"]["z"]
    result["mCenter"]["w"] = 0

    result["mExtent"]["x"] = object["ColliderBoundsBound"]["m_Extent"]["x"]
    result["mExtent"]["y"] = object["ColliderBoundsBound"]["m_Extent"]["y"]
    result["mExtent"]["z"] = object["ColliderBoundsBound"]["m_Extent"]["z"]
    result["mExtent"]["w"] = 0

    return result
