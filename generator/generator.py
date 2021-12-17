import re
import json
import math
import numpy
from opensimplex import OpenSimplex
from classes.asset import Asset
from classes.asset_manager import AssetManager
from classes.customAsset import CustomAsset 
from classes.visualizer import Vizualizer
from classes.config import config as Config
from converter.conversion_manager import ConversionManager

DEFAULT_X = int(Config.get('generator', 'default_x'))
DEFAULT_Y = int(Config.get('generator', 'default_y'))
DEFAULT_Z = int(Config.get('generator', 'default_z'))
DEFAULT_EXP = float(Config.get('generator', 'default_exponent'))
DEFAULT_SEED = int(Config.get('generator', 'seed'))

class Generator:

    def __init__(self):
        self.setXYZ(DEFAULT_X, DEFAULT_Y, DEFAULT_Z)
        self.setOctaves(1, 0.5, 0.25, 0.125)
        self.setScales(1, 2, 4, 8)
        self.setExponent(DEFAULT_EXP)
        self.setSeed(DEFAULT_SEED)

# Setters / Getters
    def setXYZ (self, x, y, z) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.max_size = max(x,y,z)
        self.elevation = numpy.zeros((self.x, self.y))
        self.placeObjectZ = numpy.zeros((self.x, self.y))
        self.setTileSize()

    def setOctaves (self, *args ) -> None:
        self.octaves = args
        self.elevationPasses = numpy.zeros((len(args) ,self.x, self.y))

    def setScales (self, *args ) -> None:
        self.scales = args

    def setExponent (self, exponent ) -> None:
        self.exponent = float(exponent)

    def setSeed (self, seed=DEFAULT_SEED) -> None:
        self.noise = OpenSimplex(seed)
        numpy.random.seed(seed)

    def setTileSize(self, tileSize = 0):
        self.tileSize = tileSize

# Misc Math
    def noiseXY(self, x, y) -> float:
        return self.noise.noise2d(x,y)
    
    def calculateNewCoordinates(self, placement, x_pos, y_pos, z_pos, rot):
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

        newPlacement = { 
            "x" : (placement['x'] / 100.0),
            "y" : (placement['y'] / 100.0),
            "z" : (placement['z'] / 100.0)
            }

        angle = placement["rot"] + rot
        
        if rot % 180 != 0:
            angle = angle + 180

        return ( 
            round(newPlacement['x'] * xAxis["x"] + newPlacement['y'] * yAxis["x"] + x_pos , 2), 
            round(newPlacement['x'] * xAxis["y"] + newPlacement['y'] * yAxis["y"] + y_pos , 2), 
            round(newPlacement['z'] + z_pos, 2), 
            angle % 360
            )

    def getPos(self, x_pos, y_pos, z_size):
        return math.ceil( self.elevation[ x_pos ][ y_pos ] / z_size )

# Elevation Generation Helpers
    def getElevationXYValue(self, x, y, wavelength) -> float:
        value = self.noiseXY( x/wavelength, y/wavelength)
        return (1 + value) * 0.5

    def generateElevationArray(self, scale):
        current_pass = numpy.zeros((self.x, self.y))
        for x in range(0, self.x):
            for y in range(0, self.y):
                current_pass[x][y] = self.getElevationXYValue(x,y,self.max_size/scale)
        return current_pass

    def generateElevation (self) -> None:
        octave_sum = sum(self.octaves)
        for count, octave in enumerate(self.octaves):
            current_pass = octave * self.generateElevationArray(self.scales[count])
            self.elevationPasses[count] = current_pass
            self.elevation += current_pass
        self.elevation /= octave_sum

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
    def place(self, asset, x_pos, y_pos, z_pos, rot):
        if type(asset) is CustomAsset:
            self.placeCustom(
                asset, 
                x_pos,
                y_pos, 
                z_pos, 
                rot
                )
        else:
            self.placeAsset(
                asset.uuid, 
                x_pos * 100, 
                y_pos * 100, 
                z_pos * 100, 
                rot
                )
        
    def placeAsset(self, uuid, x_pos, y_pos, z_pos, rot, isTile = False):
        if not uuid in self.output['asset_data'].keys():
            self.output['asset_data'][uuid] = {
                "uuid" : uuid,
                "instance_count" : 0,
                "instances" : []
            }
        
        position = {
            "x" : x_pos,
            "y" : y_pos, # in Unity Y is up
            "z" : z_pos,
            "rot" : rot
        }

        self.output['asset_data'][uuid]['instances'].append(position)
    
    def placeCustom(self, asset, x_pos, y_pos, z_pos, rot):
        dictionary = asset.getDecoded()

        for uuid, values in dictionary.items():
            for placement in values["instances"]:

                newX, newY, newZ, angle = self.calculateNewCoordinates(placement, x_pos, y_pos, z_pos, rot)

                if not(newX < 0 or newY < 0 or newZ < 0):
                    self.placeAsset(
                        uuid,
                        newX * 100,
                        newY * 100,
                        newZ * 100,
                        angle
                    )

# Elevation asset placement
    def populateElevation(self, assetList):
        
        assets = AssetManager.getAssetList(assetList)

        for asset in assets:
            size = asset.mExtent.x*2.0
            if self.tileSize < size:
                self.setTileSize(size)

        for x_pos in range(0, self.x):
            for y_pos in range(0, self.y):
                # get a random asset from list
                assetPos = int(self.getElevationXYValue(x_pos,y_pos, 4) * len(assetList))
                asset = assets[assetPos]

                rot = numpy.random.randint(4)*90
                
                z_size = asset.mExtent.y * 2.0

                for z_pos in range(0, self.adaptiveThickness(x_pos, y_pos, z_size)):
                    z_height = z_size * (self.getPos(x_pos,y_pos,z_size) - z_pos )
                    self.place(
                        asset, 
                        x_pos * self.tileSize, 
                        y_pos * self.tileSize, 
                        z_height, 
                        rot
                        )
                self.placeObjectZ[x_pos][y_pos] = z_size * (self.getPos(x_pos,y_pos,z_size) + 1)

    def adaptiveThickness(self, x_pos, y_pos, z_size) -> int:
        x = self.getPos(x_pos, y_pos, z_size)
        return int(max( 
            x - self.getPos( x_pos, max(y_pos-1, 0), z_size)+1,
            x - self.getPos( x_pos, min(y_pos+1, self.y-1), z_size)+1,
            x - self.getPos( max(x_pos-1, 0), y_pos, z_size)+1,
            x - self.getPos( min(x_pos+1, self.x-1), y_pos, z_size)+1,
            1
        ))

# Place object asset placement
    def populatePlaceObjects(self, assetList):

        assets = AssetManager.getAssetList(assetList)

        for x_pos in range(0, self.x * int(self.tileSize)):
            for y_pos in range(0, self.y * int(self.tileSize)):

                # get a random asset from list
                assetPos = int( len(assetList) * self.getElevationXYValue(x_pos,y_pos, 32))
                probability = assetList[assetPos]['Probability']

                rot = numpy.random.randint(4)*90

                z_pos = self.placeObjectZ[math.floor(x_pos / self.tileSize)][math.floor(y_pos / self.tileSize)]

                if(numpy.random.randint(100) <= probability):
                    self.place(
                        assets[assetPos], 
                        x_pos + 0.5, 
                        y_pos + 0.5, 
                        z_pos, 
                        rot
                        )

