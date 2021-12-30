import json
from objects.asset import Asset
from objects.tile import Tile
from objects.prop import Prop
from objects.customAsset import CustomAsset
from database.database import Database
from converter.conversionManager import ConversionManager


class AssetManager():

    def __init__(self):
        pass

    def getAsset(uuid, name=None):
        database = Database()
        object = database.fetchall(Asset.SqlGetAsset(str(uuid).lower()))
        assetDictionary = AssetManager.remap(object[0], True)
        className = globals()[assetDictionary["Type"]]

        asset = className(assetDictionary)
        return asset

    def addCustomAsset(name, string):
        database = Database()

        customAsset = CustomAsset({
            "Name": name,
            "String": string
        })

        database.execute(customAsset.SqlValues())
        return customAsset.uuid

    def remap(object, fromDB=False):
        result = {
            "Position": {},
            "Rotation": {},
            "Scale": {},
            "mCenter": {},
            "mExtent": {}
        }

        if fromDB:
            result["UUID"] = object[0]
            result["Type"] = object[1]
            result["Name"] = object[2]
            result["AssetName"] = object[3]
            result["String"] = object[4]

            result["Position"]["x"] = object[5]
            result["Position"]["y"] = object[6]
            result["Position"]["z"] = object[7]
            result["Position"]["w"] = object[8]

            result["Rotation"]["x"] = object[9]
            result["Rotation"]["y"] = object[10]
            result["Rotation"]["z"] = object[11]
            result["Rotation"]["w"] = object[12]

            result["Scale"]["x"] = object[13]
            result["Scale"]["y"] = object[14]
            result["Scale"]["z"] = object[15]
            result["Scale"]["w"] = object[16]

            result["mCenter"]["x"] = object[17]
            result["mCenter"]["y"] = object[18]
            result["mCenter"]["z"] = object[19]
            result["mCenter"]["w"] = object[20]

            result["mExtent"]["x"] = object[21]
            result["mExtent"]["y"] = object[22]
            result["mExtent"]["z"] = object[23]
            result["mExtent"]["w"] = object[24]

            return result

        result["UUID"] = object["Id"]
        result["Name"] = object["Name"]
        result["AssetName"] = object["Assets"][0]["LoaderData"]["AssetName"]
        result["String"] = ""

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

    def getAssetList(assetList):
        assets = []
        for asset in assetList:
            assets.append(AssetManager.getAsset(asset.params["asset"]))

        return assets
