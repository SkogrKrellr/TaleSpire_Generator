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
        self.tileThickness = 0

    def setUseRidgeNoise(self, useRidgeNoise=DEFAULT_USE_RIDGE_NOISE):
        self.settings["useRidgeNoise"] = bool(useRidgeNoise)

    def setUsePreciseHeight(self, usePreiceNoise=PRECISE_HEIGHT):
        self.settings["preciseHeight"] = bool(usePreiceNoise)

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
        return math.ceil(self.elevation[x+1][y+1] / z)

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

    def adaptiveThickness(self, x, y, z):
        current = self.getPos(x, y, z)
        return int(max(
            current - self.getPos(x, y-1, z)+1,
            current - self.getPos(x, y+1, z)+1,
            current - self.getPos(x-1, y, z)+1,
            current - self.getPos(x+1, y, z)+1,
            1
        ))

# Elevation Modifiers
    def multiplyByValue(self, value=None):
        if value is None:
            value = self.z
        self.elevation *= value

    def floorElevation(self, steps):
        self.elevation = numpy.floor(self.elevation*steps)/steps

    def powerElevation(self, value=None):
        if value is None:
            value = self.exponent
        self.elevation **= value

# Generation
    def generate(
        self,
        terrainAssets=[],
        placeObjects=[],
        sizes=[1, 1]
    ):
        result = []

        self.generateElevation(
            self.x*sizes[0],
            self.y*sizes[1],
            terrainAssets
        )
        self.powerElevation()
        self.multiplyByValue()
        self.setTileSize(self.terrainAssets[0].mExtent.x*2.0)

        self.generatePlaceObjects(
            int(self.x*sizes[0]*self.tileSize),
            int(self.y*sizes[1]*self.tileSize),
            placeObjects
        )

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
        self.populateElevation(terrainAssets, offset)
        self.populatePlaceObjects(placeObjects, offset)
        string = json.dumps(self.output)
        return ConversionManager.encode(string).decode("ascii")

    def generateElevation(self, sizeX, sizeY, assetList):
        self.elevation = numpy.zeros((sizeX+2, sizeY+2))
        self.placeObjectZ = numpy.zeros((sizeX+2, sizeY+2))

        self.terrainAssets = AssetManager.getAssetList(assetList)

        self.createHeightColorMap(assetList)
        self.elevation = self.noise.generateComplexNoiseArray(
            sizeX+2,
            sizeY+2,
            self.x, self.y,
            useRidgeNoise=self.settings["useRidgeNoise"],
        )

    def generatePlaceObjects(self, sizeX, sizeY, assetList):
        self.placeAssets = AssetManager.getAssetList(assetList)
        self.objectPlacements = []
        for position, asset in enumerate(self.placeAssets):
            assetSettings = assetList[position].getParam()
            placeObject = self.compilePlaceObjectNoiseMap(
                sizeX,
                sizeY,
                assetSettings,
                position
            )
            self.objectPlacements.append({
                "name": asset.name,
                "map": placeObject
            })

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
    def compilePlaceObjectNoiseMap(self, sizeX, sizeY, settings, position):
        noiseMap = self.noise.getRandomNoiseMap(
                {
                    "x": sizeX,
                    "y": sizeY
                },
                [  # Offset so that each asset would have a unique noise map
                    7**(position+2),
                    7**(position+2)
                ],
                settings["clumping"],
                settings["randomNoiseWeight"],
            )
        for x in range(0, sizeX):
            for y in range(0, sizeY):
                if settings["heightBasedMultiplier"] > 0:
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
            self.elevationMap = map
            self.elevationMapSize = 100
            return

        sum = 0
        for position, asset in enumerate(assetList):
            map.append({
                    "asset": asset.getParam("asset"),
                    "prob": sum + asset.getParam("density"),
                    "probPrev": sum
                })
            sum += asset.getParam("density")

        self.elevationMap = map
        self.elevationMapSize = sum
        return

    def getAssetFromMap(
        self,
        x,
        y,
        assetList
    ):
        if self.settings["heightBasedPlacement"]:
            height = int(self.elevation[x][y]/self.z*100)
            settings = assetList[self.elevationMap[height][0]].getParam()

            if settings["blendHeightMultiplier"] > 0:
                height += numpy.random.randint(
                    low=-settings["blendHeightMultiplier"],
                    high=settings["blendHeightMultiplier"])
                height = max(min(100, height), 0)

            return self.elevationMap[height][0]

        random = numpy.random.randint(self.elevationMapSize-1)
        placeAsset = ""
        for item in self.elevationMap:
            if random >= item["probPrev"] and random < item["prob"]:
                placeAsset = item["asset"]
                break

        for counter, asset in enumerate(self.terrainAssets):
            if asset.uuid == placeAsset:
                return counter

# Asset placement
    def populateElevation(self, assetList, offset):
        for x in range(0, self.x):
            for y in range(0, self.y):
                offsetX = x + offset[0]
                offsetY = y + offset[1]
                assetPosition = self.getAssetFromMap(
                            offsetX,
                            offsetY,
                            assetList
                        )
                asset = self.terrainAssets[assetPosition]

                if self.settings["preciseHeight"] and x == 1 and y == 1:
                    self.place(
                        asset,
                        x * self.tileSize,
                        y * self.tileSize,
                        numpy.amin(self.elevation),
                        0
                        )

                z = asset.mExtent.y * 2.0
                currentHeight = self.getPos(offsetX, offsetY, z)
                self.placeObjectZ[offsetX][offsetY] = z * (currentHeight + 1)

                for w in range(0, self.adaptiveThickness(offsetX, offsetY, z)):
                    self.place(
                        asset,
                        x * self.tileSize,
                        y * self.tileSize,
                        z * (currentHeight - w),
                        numpy.random.randint(4)*90
                        )

    def populatePlaceObjects(self, assetList, offset):
        for position, placement in enumerate(self.objectPlacements):
            for x in range(0, self.x * int(self.tileSize)):
                for y in range(0, self.y * int(self.tileSize)):
                    offsetX = x + offset[0]
                    offsetY = y + offset[1]
                    if placement["map"][offsetX][offsetY]:

                        assetSettings = assetList[position].getParam()
                        asset = self.placeAssets[position]

                        scaledX = math.floor(x/self.tileSize) + offset[0]
                        scaledY = math.floor(y/self.tileSize) + offset[1]

                        newX = x + 0.5
                        newY = y + 0.5
                        newZ = self.placeObjectZ[scaledX][scaledY] + assetSettings["verticalOffset"]
                        newRot = 0

                        if assetSettings["randomRotationEnabled"]:
                            newRot = numpy.random.randint(4)*90

                        if assetSettings["randomNudgeEnabled"]:
                            newX += (numpy.random.randint(100)-50)/100
                            newY += (numpy.random.randint(100)-50)/100

                        self.place(asset, newX, newY, newZ, newRot)
