import json
import math
import numpy
import pyperclip as pc
from opensimplex import OpenSimplex

from objects.asset import Asset
from objects.tile import Tile
from objects.assetManager import AssetManager
from objects.customAsset import CustomAsset
from objects.visualizer import Visualizer
from objects.config import config as Config
from converter.conversionManager import ConversionManager
from generator.noise import Noise
from settings.placeObjectSettings import PlaceObjectSettings
from settings.terrainSettings import TerrainSettings

DEFAULT_X = int(Config.get('generator', 'default_x'))
DEFAULT_Y = int(Config.get('generator', 'default_y'))
DEFAULT_Z = int(Config.get('generator', 'default_z'))
DEFAULT_EXP = float(Config.get('generator', 'default_exponent'))
DEFAULTSEED = int(Config.get('generator', 'seed'))
DEFAULT_USE_RIDGE_NOISE = bool(Config.getboolean('generator', 'useRidgeNoise'))
USE_HEIGHT_ASSET_SPREAD = bool(Config.getboolean('generator', 'heightBasedAssetSpread'))
PRECISE_HEIGHT = bool(Config.getboolean('generator', 'preciseHeight'))

REALY_BIG_NUMBER = 20000


class Generator:

    settings = {"useRidgeNoise": DEFAULT_USE_RIDGE_NOISE,
                "preciseHeight": PRECISE_HEIGHT,
                "heightBasedPlacement": USE_HEIGHT_ASSET_SPREAD,
                }

    def __init__(self):
        self.setXYZ(DEFAULT_X, DEFAULT_Y, DEFAULT_Z)
        self.setSeed(DEFAULTSEED)
        self.setOctaves(1, 0.5, 0.25, 0.125)
        self.setScales(1, 2, 4, 8)
        self.setExponent(DEFAULT_EXP)
        self.setTileSize()

# Setters / Getters
    def setXYZ(self, x, y, z):
        self.x = max(x, 1)
        self.y = max(y, 1)
        self.z = max(z, 1)
        self.elevation = numpy.zeros((self.x, self.y))
        self.placeObjectZ = numpy.zeros((self.x, self.y))

    def setOctaves(self, *args):
        self.noise.setOctaves(*args)

    def setScales(self, *args):
        self.noise.setScales(*args)

    def setExponent(self, exponent):
        self.exponent = float(exponent)

    def setSeed(self, seed):
        self.noise = Noise(seed)

    def setTileSize(self, tileSize=0):
        self.tileSize = max(tileSize, 0)

    def setUseRidgeNoise(self, useRidgeNoise=DEFAULT_USE_RIDGE_NOISE):
        self.settings["useRidgeNoise"] = bool(useRidgeNoise)

    def setUsePreciseHeight(self, usePreiceNoise=PRECISE_HEIGHT):
        self.settings["useRidgeNoise"] = bool(usePreiceNoise)

    def setUseHeightBasedTerrainAssetPlacement(
        self,
        useHeightBasedPlacement=USE_HEIGHT_ASSET_SPREAD
    ):
        self.settings["heightBasedPlacement"] = bool(useHeightBasedPlacement)

    def initializeOutput(self):
        self.output = {
            "unique_asset_count": 0,
            "asset_data": {}
        }

    def getPos(self, x, y, z):
        return math.ceil(self.elevation[x][y] / z)

# Misc Math
    def calculateNewCoordinates(self, placement, rot, asset):
        offset = {
            "x": 0,
            "y": 0
        }
        angle = 0

        cos = round(math.cos(math.radians(rot)))
        sin = round(math.sin(math.radians(rot)))

        axis = {
            "x": {"x": cos, "y": sin},
            "y": {"x": -sin, "y": cos}
        }

        if rot % 180 == 90:
            angle = 180

        angle += (rot + placement["rot"]) % 360

        if type(asset) is Tile:
            if rot == 90:
                if angle % 180 == 90:
                    offset["x"] = -asset.mExtent.z*2
                if angle % 180 == 0:
                    offset["x"] = -asset.mExtent.x*2
            if rot == 180:
                if angle % 180 == 90:
                    offset["x"] = -asset.mExtent.z*2
                    offset["y"] = -asset.mExtent.x*2
                if angle % 180 == 0:
                    offset["x"] = -asset.mExtent.x*2
                    offset["y"] = -asset.mExtent.z*2
            if rot == 270:
                if angle % 180 == 90:
                    offset["y"] = -asset.mExtent.x*2
                if angle % 180 == 0:
                    offset["y"] = -asset.mExtent.z*2

        new = {
            "x": placement["x"]/100,
            "y": placement["y"]/100,
            "z": placement["z"]/100
        }

        return (
            new["x"] * axis["x"]["x"] + new["y"] * axis["y"]["x"] + offset["x"],
            new["y"] * axis["y"]["y"] + new["x"] * axis["x"]["y"] + offset["y"],
            new["z"],
            angle
        )

    def adaptiveThickness(self, x, y, z) -> int:
        current = self.getPos(x, y, z)
        return int(max(
            current - self.getPos(x, max(y-1, 0), z)+1,
            current - self.getPos(x, min(y+1, self.y-1), z)+1,
            current - self.getPos(max(x-1, 0), y, z)+1,
            current - self.getPos(min(x+1, self.x-1), y, z)+1,
            1
        ))

# Elevation Modifiers
    def multiplyByValue(self) -> None:
        self.elevation *= self.z

    def floorElevation(self, steps) -> None:
        self.elevation = numpy.floor(self.elevation*steps)/steps

    def powerElevation(self) -> None:
        self.elevation **= self.exponent

# Generation
    def generate(
        self,
        terrainAssets=[],
        placeObjects=[],
        sizes=[1, 1]
    ):
        result = []

        for x in range(sizes[0]):
            for y in range(sizes[1]):
                self.initializeOutput
                output = self.generatePart(
                    terrainAssets,
                    placeObjects,
                    [x * self.x, y * self.y]
                )
                result.append({
                    "x": x,
                    "y": y,
                    "output": output
                })

        return result

    def generatePart(
        self,
        terrainAssets,
        placeObjects,
        offset=[0, 0]
    ):
        self.initializeOutput()
        self.generateElevation(offset)
        self.powerElevation()
        self.multiplyByValue()
        self.populateElevation(terrainAssets)
        self.populatePlaceObjects(placeObjects)
        string = json.dumps(self.output)
        return ConversionManager.encode(string).decode("utf-8")

    def generateElevation(
        self,
        offset=[0, 0]
    ):
        self.elevation = self.noise.generateComplexNoiseArray(
            self.x,
            self.y,
            useRidgeNoise=self.settings["useRidgeNoise"],
            offset=offset
        )

# Placement
    def place(self, asset, x, y, z, rot):
        # padding for when rotation places tiles outside bounds
        x += 5
        y += 5

        if type(asset) is CustomAsset:
            self.placeCustom(asset, x, y, z, rot)
        else:
            self.placeAsset(asset.uuid, x, y, z, rot)

    def placeAsset(self, uuid, x, y, z, rot):
        if uuid not in self.output['asset_data'].keys():
            self.output['asset_data'][uuid] = {
                "uuid": uuid,
                "instance_count": 0,
                "instances": []
            }

        self.output['asset_data'][uuid]['instances'].append({
            "x": x * 100,
            "y": y * 100,
            "z": z * 100,
            "rot": rot
        })

    def placeCustom(self, asset, x, y, z, rot):
        dictionary = asset.getDecoded()
        coordinates = []

        minimum = {
            "x": REALY_BIG_NUMBER,
            "y": REALY_BIG_NUMBER
        }

        for item in dictionary:
            placeAsset = AssetManager.getAsset(item["uuid"])
            for placement in item["instances"]:
                newX, newY, newZ, angle = self.calculateNewCoordinates(
                    placement,
                    rot,
                    placeAsset
                )

                minimum["x"] = min(newX, minimum["x"])
                minimum["y"] = min(newY, minimum["y"])

                coordinates.append({
                    "uuid": item["uuid"],
                    "x": newX + x,
                    "y": newY + y,
                    "z": newZ + z,
                    "rot": angle
                })

        for coord in coordinates:
            newX = coord["x"] - minimum["x"]
            newY = coord["y"] - minimum["y"]
            newZ = coord["z"]

            self.placeAsset(
                coord["uuid"],
                newX,
                newY,
                newZ,
                coord["rot"]
            )

# Helpers
    def compilePlaceObjectNoiseMap(self, settings, position):
        noiseMap = self.noise.getRandomNoiseMap(
                {
                    "x": self.x * int(self.tileSize),
                    "y": self.y * int(self.tileSize)
                },
                [  # Offset so that each asset would have a unique noise map
                    7**(position+2),
                    7**(position+2)
                ],
                settings["clumping"],
                settings["randomNoiseWeight"],
                )

        for x in range(0, self.x * int(self.tileSize)):
            for y in range(0, self.y * int(self.tileSize)):
                if settings["heightBasedMultiplier"] >= 0:
                    scaledX = math.floor(x / self.tileSize)
                    scaledY = math.floor(y / self.tileSize)
                    noiseMap[x][y] += self.elevation[scaledX][scaledY]
                    noiseMap[x][y] *= settings["heightBasedMultiplier"]
                    noiseMap[x][y] += settings["heightBasedOffset"]

                if noiseMap[x][y] <= settings["density"]:
                    noiseMap[x][y] = 1.0
                else:
                    noiseMap[x][y] = 0.0
        return noiseMap

    def createObjectList(list, placeObjects=False):
        resultingList = []
        for item in list:
            if placeObjects:
                resultingList.append(PlaceObjectSettings(item))
            else:
                resultingList.append(TerrainSettings(item))
        return resultingList

    def createHeightColorMap(self, assetList):
        map = []

        if self.settings["heightBasedPlacement"]:
            for x in range(101):
                map.append([])
            for position, asset in enumerate(assetList):
                map[int(asset.getParam("heightMax"))].append(position)
            for x in range(100, 0, -1):  # Fill empty spaces from top to bottom
                if map[x-1] == []:
                    map[x-1] = map[x]
            for x in range(101):  # Fill empty spaces from bottom to top
                if map[x] == []:
                    map[x] = map[x-1]
            return map, 100

        sum = 0
        for position, asset in enumerate(assetList):
            map.append({
                    "asset": asset.getParam("asset"),
                    "prob": sum + asset.getParam("densityMax"),
                    "probPrev": sum
                })
            sum += asset.getParam("densityMax")
        return map, sum

    def getAssetFromMap(
        self,
        map,
        mapSize,
        x,
        y,
        maximum,
        assetList,
        assets
    ):
        if self.settings["heightBasedPlacement"]:
            relativeHeight = int(self.elevation[x][y] / maximum * 100)
            settings = assetList[map[relativeHeight][0]].getParam()

            if settings["blendHeightMultiplier"] > 0:
                relativeHeight += numpy.random.randint(
                    low=-settings["blendHeightMultiplier"],
                    high=settings["blendHeightMultiplier"])
                relativeHeight = max(min(100, relativeHeight), 0)

            return assets[map[relativeHeight][0]]

        random = numpy.random.randint(mapSize-1)
        placeAsset = ""
        for item in map:
            if random >= item["probPrev"] and random < item["prob"]:
                placeAsset = item["asset"]
                break
        for asset in assets:
            if asset.uuid == placeAsset:
                return asset

# Asset placement
    def populateElevation(self, assetList):
        assets = AssetManager.getAssetList(assetList)
        map, mapSize = self.createHeightColorMap(assetList)

        for asset in assets:
            size = max(asset.mExtent.x, asset.mExtent.z)*2.0
            if self.tileSize < size:
                self.setTileSize(size)

        maximumHeight = numpy.amax(self.elevation)

        for x in range(0, self.x):
            for y in range(0, self.y):

                asset = self.getAssetFromMap(
                            map,
                            mapSize,
                            x,
                            y,
                            maximumHeight,
                            assetList,
                            assets
                        )

                if self.settings["preciseHeight"] and x == 0 and y == 0:
                    self.place(
                        asset,
                        x * self.tileSize,
                        y * self.tileSize,
                        0,
                        numpy.random.randint(4)*90
                        )

                z = asset.mExtent.y * 2.0
                currentHeight = self.getPos(x, y, z)

                for w in range(0, self.adaptiveThickness(x, y, z)):
                    self.place(
                        asset,
                        x * self.tileSize,
                        y * self.tileSize,
                        z * (currentHeight - w),
                        numpy.random.randint(4)*90
                        )

                self.placeObjectZ[x][y] = z * (currentHeight + 1)

    def populatePlaceObjects(self, assetList):
        assets = AssetManager.getAssetList(assetList)
        for position, asset in enumerate(assets):
            assetSettings = assetList[position].getParam()
            placeObject = self.compilePlaceObjectNoiseMap(
                assetSettings,
                position
            )
            for x in range(0, self.x * int(self.tileSize)):
                for y in range(0, self.y * int(self.tileSize)):
                    if placeObject[x][y]:
                        scaledX = math.floor(x / self.tileSize)
                        scaledY = math.floor(y / self.tileSize)

                        newX = x + 0.5
                        newY = y + 0.5
                        newZ = self.placeObjectZ[scaledX][scaledY]
                        newRot = 0

                        if assetSettings["randomRotationEnabled"]:
                            newRot = numpy.random.randint(4)*90

                        if assetSettings["randomNudgeEnabled"]:
                            newX += (numpy.random.randint(100)-50)/200
                            newY += (numpy.random.randint(100)-50)/200

                        self.place(asset, newX, newY, newZ, newRot)
