import re
import json
import math
import numpy
import pyperclip as pc
from opensimplex import OpenSimplex
from classes.asset import Asset
from classes.assetManager import AssetManager
from classes.customAsset import CustomAsset 
from classes.visualizer import Vizualizer
from classes.config import config as Config
from converter.conversionManager import ConversionManager
from generator.noise import Noise
from generator.placeObjectSettings import PlaceObjectSettings
from generator.terrainSettings import TerrainSettings

DEFAULT_X = int(Config.get('generator', 'default_x'))
DEFAULT_Y = int(Config.get('generator', 'default_y'))
DEFAULT_Z = int(Config.get('generator', 'default_z'))
DEFAULT_EXP = float(Config.get('generator', 'default_exponent'))
DEFAULTSEED = int(Config.get('generator', 'seed'))
DEFAULT_USE_RIDGE_NOISE = bool(Config.getboolean('generator', 'useRidgeNoise'))

CORRECTION_MINIMUM = int(Config.get('noiseCorrection', 'minimum'))
CORRECTION_MAXIMUM = int(Config.get('noiseCorrection', 'maximum'))

class Generator:

    def __init__(self):
        self.setXYZ(DEFAULT_X, DEFAULT_Y, DEFAULT_Z)
        self.noise = Noise(DEFAULTSEED)
        self.setOctaves(1, 0.5, 0.25, 0.125)
        self.setScales(1, 2, 4, 8)
        self.setExponent(DEFAULT_EXP)
        self.setUseRidgeNoise(DEFAULT_USE_RIDGE_NOISE)

# Setters / Getters
    def setXYZ (self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.setTileSize()
        self.clearArrays()

    def setOctaves (self, *args ):
        self.noise.setOctaves(*args)

    def setScales (self, *args ):
        self.noise.setScales(*args)

    def setExponent (self, exponent ):
        self.exponent = float(exponent)

    def setTileSize(self, tileSize = 0):
        self.tileSize = tileSize

    def setUseRidgeNoise(self, useRidgeNoise = False):
        self.useRidgeNoise = useRidgeNoise

# Misc Math
    def calculateNewCoordinates(self, placement, xPos, yPos, zPos, rot):
        rot = rot % 360
        rotRadians = math.radians(rot)
        rotRadiansRightAngle = math.radians(rot+90)

        xAxis = { 
            "x" : math.cos(rotRadians), 
            "y" : math.sin(rotRadians)
            }

        yAxis = { 
            "x" : math.cos(rotRadiansRightAngle),
            "y" : math.sin(rotRadiansRightAngle)
            }

        angle = placement["rot"] + rot
        
        if rot % 180 != 0:
            angle = angle + 180

        return ( 
            placement['x'] * xAxis["x"] + placement['y'] * yAxis["x"] + xPos*100 , 
            placement['x'] * xAxis["y"] + placement['y'] * yAxis["y"] + yPos*100 , 
            placement['z'] + zPos*100, 
            angle % 360
            )

    def getPos(self, xPos, yPos, zSize):
        return math.ceil( self.elevation[ xPos ][ yPos ] / zSize )

# Elevation Generation Helpers
    def clearArrays(self):
        self.elevation = numpy.zeros((self.x, self.y))
        self.placeObjectZ = numpy.zeros((self.x, self.y))

    def generateElevation (self) -> None:
        self.elevation = self.noise.generateComplexNoiseArray(
            self.x,
            self.y,
            useRidgeNoise = self.useRidgeNoise
        )

# Elevation Modifiers
    def multiplyByValue(self) -> None:
        self.elevation = self.elevation * self.z

    def floorElevation(self, steps) -> None:
        self.elevation = numpy.floor(self.elevation*steps)/steps

    def powerElevation(self) -> None:
        self.elevation = self.elevation**self.exponent

# Generation
    def generate(self, terrainAssets, placeObjects):
        self.output = {
            "unique_asset_count": 0,
            "asset_data": {}
        }
        self.generateElevation()
        self.powerElevation()
        self.multiplyByValue()
        self.populateElevation( terrainAssets ) 
        self.populatePlaceObjects( placeObjects ) 
        return json.dumps(self.output)

# Placement utils 
    def place(self, asset, xPos, yPos, zPos, rot):
        # padding for when rotation places tiles outside bounds
        xPos += 5
        yPos += 5

        if type(asset) is CustomAsset:
            self.placeCustom(
                asset, 
                xPos,
                yPos, 
                zPos, 
                rot
                )
        else:
            self.placeAsset(
                asset.uuid, 
                xPos * 100, 
                yPos * 100, 
                zPos * 100, 
                rot
                )
        
    def placeAsset(self, uuid, xPos, yPos, zPos, rot):
        if not uuid in self.output['asset_data'].keys():
            self.output['asset_data'][uuid] = {
                "uuid" : uuid,
                "instance_count" : 0,
                "instances" : []
            }
        
        self.output['asset_data'][uuid]['instances'].append({
            "x" : xPos,
            "y" : yPos, # in Unity Y is up
            "z" : zPos,
            "rot" : rot
        })
    
    def placeCustom(self, asset, xPos, yPos, zPos, rot):
        dictionary = asset.getDecoded()

        for uuid, values in dictionary.items():
            for placement in values["instances"]:

                newX, newY, newZ, angle = self.calculateNewCoordinates(placement, xPos, yPos, zPos, rot)

                if not(newX < 0 or newY < 0 or newZ < 0):
                    self.placeAsset(
                        uuid,
                        newX,
                        newY,
                        newZ,
                        angle
                    )

# Elevation asset placement
    def createObjectList(list, placeObjects = False):
        resultingList = []
        for item in list:
            if placeObjects:
                resultingList.append(PlaceObjectSettings(item))
            else:
                resultingList.append(TerrainSettings(item))
        return resultingList

    def populateElevation(self, assetList):
        assets = AssetManager.getAssetList(assetList)
        
        for asset in assets:
            size = asset.mExtent.x*2.0
            if self.tileSize < size:
                self.setTileSize(size)

        for xPos in range(0, self.x):
            for yPos in range(0, self.y):
                assetPos = int(self.noise.getNoiseXYValue(xPos,yPos, 4) * len(assetList))
                asset = assets[assetPos]
                zSize = asset.mExtent.y * 2.0

                for zPos in range(0, self.adaptiveThickness(xPos, yPos, zSize)):
                    zHeight = zSize * (self.getPos(xPos,yPos,zSize) - zPos )
                    self.place(
                        asset, 
                        xPos * self.tileSize, 
                        yPos * self.tileSize, 
                        zHeight, 
                        numpy.random.randint(4)*90
                        )

                self.placeObjectZ[xPos][yPos] = zSize * (self.getPos(xPos,yPos,zSize) + 1)

    def adaptiveThickness(self, xPos, yPos, zSize) -> int:
        x = self.getPos(xPos, yPos, zSize)
        return int(max( 
            x - self.getPos( xPos, max(yPos-1, 0), zSize)+1,
            x - self.getPos( xPos, min(yPos+1, self.y-1), zSize)+1,
            x - self.getPos( max(xPos-1, 0), yPos, zSize)+1,
            x - self.getPos( min(xPos+1, self.x-1), yPos, zSize)+1,
            1
        ))

# Place object asset placement
    def populatePlaceObjects(self, assetList):

        assets = AssetManager.getAssetList(assetList)

        # self.place( assets[0], 10, 10, 0, 0)
        # self.place( assets[0], 10, 10, 5, 90)
        # self.place( assets[0], 10, 10, 10, 180)
        # self.place( assets[0], 10, 10, 15, 270)
        # return
        
        for position, asset in enumerate(assets):            
            settings = assetList[position].getParam()

            noiseMap = self.noise.getRandomNoiseMap(
                { "x" : self.x * int(self.tileSize), 
                  "y" : self.y * int(self.tileSize)},
                { "x" : 7**(position+2),
                  "y" : 7**(position+2)},
                settings["clumping"],
                settings["randomNoiseWeight"],
                )

            #Vizualizer.showImage(noiseMap, False)

            for xPos in range(0, self.x * int(self.tileSize)):
                for yPos in range(0, self.y * int(self.tileSize)):

                    x = math.floor(xPos / self.tileSize)
                    y = math.floor(yPos / self.tileSize)

                    if settings["heightBasedEnabled"]:
                       noiseMap[xPos][yPos] += self.elevation[x][y] * settings["heightBasedMultiplier"] + settings["heightBasedOffset"]

                    if noiseMap[xPos][yPos] <= settings["density"]:
                        newX = xPos + 0.5
                        newY = yPos + 0.5
                        newZ = self.placeObjectZ[x][y]
                        newRot = 0

                        if settings["randomRotationEnabled"]:
                            newRot = numpy.random.randint(4)*90

                        if settings["randomNudgeEnabled"]:
                            newX += (numpy.random.randint(100)-50)/100
                            newY += (numpy.random.randint(100)-50)/100
                    
                        self.place( asset, newX, newY, newZ, newRot)


