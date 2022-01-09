import json
import math
import numpy
from generator.modifications import *
from objects.tile import Tile
from objects.assetManager import AssetManager
from objects.customAsset import CustomAsset
from config.config import config as Config
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
    """
    Class for a TaleSpire terrain generation.

    Attributes:
        x,y,z (int): size of block to generate
        noise (Noise): noise generator
        expontent (float): exponent for redistributing terrain
        settings (dict): flags that alter generation
        tileSize (float): maxima of the terrain tile lengths and widths
        output (dict): output to store the not yet encoded TaleSpire object
        elevation (2d array): heightmap for terrain
        placeObjectZ (2d array): scaled elevation heightmap for object placement
        terrainAssets (list): list of terrainSettings
        placeAssets (list): list of placeObjectSettings
        elevationMap (dict, list): a map for corelating height and asset to be placed
        elevationMapSize (int): maximum value in elevationMap
    """

    settings = {
        "useRidgeNoise": DEFAULT_USE_RIDGE_NOISE,
        "preciseHeight": PRECISE_HEIGHT,
        "heightBasedPlacement": USE_HEIGHT_ASSET_SPREAD,
    }

    def __init__(self):
        """
        Constructor for Generator class.
        """
        self.setXYZ(DEFAULT_X, DEFAULT_Y, DEFAULT_Z)
        self.setSeed(DEFAULTSEED)
        self.setOctaves(1, 0.5, 0.25, 0.125)
        self.setScales(1, 2, 4, 8)
        self.setExponent(DEFAULT_EXP)
        self.setTileSize()

# Setters / Getters
    def setXYZ(self, x, y, z):
        """
        Setter for size of blocks to be generated.

        Parameters:
            x (int): size in X dimension
            y (int): size in Y dimension
            z (int): size in Z dimension
        """

        self.x = max(x, 1)
        self.y = max(y, 1)
        self.z = max(z, 1)

    def setOctaves(self, *args):
        """
        Setter for octaves in noise generator.

        Parameters:
            args (list of floats): multipliers for noises intensity
        """

        self.noise.setOctaves(*args)

    def setScales(self, *args):
        """
        Setter for set scales in noise generator.

        Parameters:
            args (list of floats): multipliers for noises scale
        """

        self.noise.setScales(*args)

    def setExponent(self, exponent):
        """
        Setter for redistribution of noise value.

        Parameters:
            exponent (float): exponent for redistribution
        """

        self.exponent = float(exponent)

    def setSeed(self, seed):
        """
        Function to set noise generator seeds.

        Parameters:
            seed (any): seed for the generator
        """

        self.noise = Noise(seed)

    def setTileSize(self, tileSize=0):
        """
        Function to set maximum terrain tile size.

        Parameters:
            tileSize (float): size of largest tiles maximum length or width
        """

        self.tileSize = max(tileSize, 0)

    def setUseRidgeNoise(self, useRidgeNoise=DEFAULT_USE_RIDGE_NOISE):
        """
        Function to set setting if ridge noise will be used.

        Parameters:
            useRidgeNoise (bool): will ridge noise be used
        """

        self.settings["useRidgeNoise"] = bool(useRidgeNoise)

    def setUsePreciseHeight(self, usePreiceNoise=PRECISE_HEIGHT):
        """
        Function to set setting if precise height will be used.

        Parameters:
            usePreiceNoise (bool): will precise height be used
        """

        self.settings["preciseHeight"] = bool(usePreiceNoise)

    def setUseHeightBasedTerrainAssetPlacement(
        self,
        useHeightBasedPlacement=USE_HEIGHT_ASSET_SPREAD
    ):
        """
        Function to set setting if terrain assets will be distributed based on
        their height settings.

        Parameters:
            useHeightBasedPlacement (bool): will height based distribution used
        """

        self.settings["heightBasedPlacement"] = bool(useHeightBasedPlacement)

    def initializeOutput(self):
        """
        Function for initializing output dictionary between block generation
        """

        self.output = {
            "unique_asset_count": 0,
            "asset_data": {}
        }

    def getPos(self, x, y, z):
        """
        Function to get noise value at point X Y and scale it by Z.

        Parameters:
            x (int): X coordinate for noise
            y (int): Y coordinate for noise
            z (float): scaling factor for Z

        Returns:
            float: value at that coordinate from -1.0 to 1.0
        """

        return math.ceil(self.elevation[x+1][y+1] / z)

# Misc Math
    def calculateNewCoordinates(self, placement, rot, asset):
        """
        Function to rotate a part of a complex asset around its
        left botto most corner.

        Parameters:
            placement (dict): placement of the elementary asset in
                              relation to the complex assets origin
            rot (int): amount of degrees to rotate
            asset (Asset): asset that is going to be rotated

        Returns:
            dict: a set of new coordinates after rotation
        """

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
        """
        Function to calculate the biggest change in elevation in neighboring
        tiles

        Parameters:
            x (int): X coordinate for referance tile to check change against
            y (int): Y coordinate for referance tile to check change against
            z (float): scaling factor for Z

        Returns:
            int: biggest tile difference in neighboring tiles
        """

        current = self.getPos(x, y, z)
        return int(max(
            current - self.getPos(x, y-1, z)+1,
            current - self.getPos(x, y+1, z)+1,
            current - self.getPos(x-1, y, z)+1,
            current - self.getPos(x+1, y, z)+1,
            1
        ))

# Generation
    def generate(
        self,
        terrainAssets=[],
        placeObjects=[],
        sizes=[1, 1]
    ):
        """
        Function to generate X*Y ammount of terrain blocks, with
        a set list of assets to be used in terrain.
        And a set list of assets to be placed on the terrain

        Parameters:
            terrainAssets (list): list of terrain settings
            placeObjects (list): list of place object settings
            size (list): x and y component for how many blocks to generate in
                         each direction

        Returns:
            dict: generated output for each x, y coordinate
        """

        result = []

        terrainAssets = Generator.createObjectList(terrainAssets)
        placeObjects = Generator.createObjectList(placeObjects, True)

        self.generateElevation(
            self.x*sizes[0],
            self.y*sizes[1],
            terrainAssets
        )
        redistribute(self.elevation, self.exponent)
        multiplyByValue(self.elevation, self.z)
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
        """
        Function to generate one terrain blocks, with
        a set list of assets to be used in terrain.
        And a set list of assets to be placed on the terrain

        Parameters:
            terrainAssets (list): list of terrain settings
            placeObjects (list): list of place object settings
            offset (list): x and y offset, for which block is being currently
                           generated

        Returns:
            string: encoded TaleSpire string for generated block
        """

        self.initializeOutput()
        self.populateElevation(terrainAssets, offset)
        self.populatePlaceObjects(placeObjects, offset)
        string = json.dumps(self.output)
        return ConversionManager.encode(string).decode("ascii")

    def generateElevation(self, sizeX, sizeY, assetList):
        """
        Function to generate elevation and unpack terrain setting list

        Parameters:
            sizeX (int): total X size of terrain to be generated
            sizeY (int): total Y size of terrain to be generated
            assetList (list): terrain setting list
        """

        self.elevation = numpy.zeros((sizeX+2, sizeY+2))
        self.placeObjectZ = numpy.zeros((sizeX+2, sizeY+2))

        self.terrainAssets = AssetManager.getAssetList(assetList)

        self.createHeightColorMap(assetList)
        self.elevation = self.noise.generateComplexNoiseArray(
            sizeX+2,
            sizeY+2,
            max(self.x, self.y),
            useRidgeNoise=self.settings["useRidgeNoise"],
        )

    def generatePlaceObjects(self, sizeX, sizeY, assetList):
        """
        Function to generate elevation and unpack place object setting list

        Parameters:
            sizeX (int): total X size of place object map to be generated
            sizeY (int): total Y size of  place object map to be generated
            assetList (list): place object setting list
        """

        self.placeAssets = AssetManager.getAssetList(assetList)
        self.objectPlacements = []
        for position, asset in enumerate(self.placeAssets):
            assetSettings = assetList[position].getParam()
            placeObject = self.compilePlaceObjectNoiseMap(
                sizeX,
                sizeY,
                assetSettings
            )
            self.objectPlacements.append({
                "name": asset.name,
                "map": placeObject
            })

# Placement

    def place(self, asset, x, y, z, rot):
        """
        Function to place an asset in specific X, Y, Z coordinates with a
        specific rotation

        Parameters:
            asset (Asset): asset to be placed
            x (float): X coordinate where to place the asset
            y (float): Y coordinate where to place the asset
            z (float): Z coordinate where to place the asset
            rot (int): Rotation of this asset
        """

        # padding for when rotation places tiles outside bounds
        x += 5
        y += 5
        if type(asset) is CustomAsset:
            self.placeCustom(asset, x, y, z, rot)
        else:
            self.placeAsset(asset.uuid, x, y, z, rot)

    def placeAsset(self, uuid, x, y, z, rot):
        """
        Function to place an elementary asset in specific X, Y, Z coordinates
        with a specific rotation

        Parameters:
            asset (Asset): asset to be placed
            x (float): X coordinate where to place the asset
            y (float): Y coordinate where to place the asset
            z (float): Z coordinate where to place the asset
            rot (int): Rotation of this asset
        """

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
        """
        Function to place a complex asset in specific X, Y, Z coordinates with
        a specific rotation

        Parameters:
            asset (Asset): asset to be placed
            x (float): X coordinate where to place the asset
            y (float): Y coordinate where to place the asset
            z (float): Z coordinate where to place the asset
            rot (int): Rotation of this asset
        """

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
    def compilePlaceObjectNoiseMap(self, sizeX, sizeY, settings):
        """
        Function to generate distribution map for each place objects

        Parameters:
            sizeX (int): total X size of place object map to be generated
            sizeY (int): total Y size of place object map to be generated
            settings (Setting): current place objects settings

        Returns:
            array: map of placements of the asset
        """

        noiseMap = self.noise.getRandomNoiseMap(
                {
                    "x": sizeX,
                    "y": sizeY
                },
                {  # Offset so that each asset would have a unique noise map
                    "x": numpy.random.randint(0, REALY_BIG_NUMBER),
                    "y": numpy.random.randint(0, REALY_BIG_NUMBER)
                },
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
        """
        Function to compile dictionary int o list of settings

        Parameters:
            list (dict): total X size of place object map to be generated
            placeObjects (bool): is the list for place objects

        Returns:
            list: list of the apropriate Setting type
        """

        resultingList = []
        for item in list:
            if placeObjects:
                resultingList.append(PlaceObjectSettings(item))
            else:
                resultingList.append(TerrainSettings(item))

        return resultingList

    def createHeightColorMap(self, assetList):
        """
        Function to create a lookup map for distributing terrain assets.
        Based of flag "heightBasedPlacement" it will either generate
        tiles based on the height value,
        Or by utilising noise.

        Parameters:
            assetList (list of terrain settings):
                list of all tiles that are going to be used in terrain
        """

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
        """
        Function to get asset from the generated elevation map.

        Parameters:
            x (float): X coordinate where to place the asset
            y (float): Y coordinate where to place the asset
            assetList (list of terrain settings):
                list of all tiles that are going to be used in terrain
        """

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
        """
        Function to turn elevation into a list of TaleSpire assets.

        Parameters:
            assetList (list of terrain settings):
                list of all tiles that are going to be used in terrain
            offset (list): x and y offset for currently generating block
        """

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
        """
        Function to turn place object maps into a list of TaleSpire assets.

        Parameters:
            assetList (list of terrain settings):
                list of all assets that are going to be placed on the terrain
            offset (list): x and y offset for currently generating block
        """

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

                        placeHeight = self.placeObjectZ[scaledX][scaledY]

                        newX = x
                        newY = y
                        newZ = placeHeight + assetSettings["verticalOffset"]
                        newRot = 0

                        if assetSettings["placeOnCenter"]:
                            newX += 0.5
                            newY += 0.5

                        if assetSettings["randomRotationEnabled"]:
                            newRot = numpy.random.randint(4)*90

                        if assetSettings["randomNudgeEnabled"]:
                            newX += (numpy.random.randint(100)-50)/100
                            newY += (numpy.random.randint(100)-50)/100

                        self.place(asset, newX, newY, newZ, newRot)
