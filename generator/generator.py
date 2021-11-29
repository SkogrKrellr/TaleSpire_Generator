import re
import json
import math
import numpy
from opensimplex import OpenSimplex
from classes.asset import Asset 
from classes.visualizer import Vizualizer
from classes.config import config as Config

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
        self.poZ = numpy.zeros((self.x, self.y))

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

# Misc
    def noiseXY(self, x, y) -> float:
        return self.noise.noise2d(x,y)

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
        
        self.populateElevation(terrainAssets)
        self.populatePlaceObjects(placeObjects)

        return json.dumps(self.output)

# Placement utils 
    def getPos(self, x_pos, y_pos, z_size):
        return math.ceil( self.elevation[ x_pos ][ y_pos ] / z_size )

    def placeAsset(self, asset, x_pos, y_pos, z_pos, rot):
        if not asset.uuid in self.output['asset_data'].keys():
            self.output['asset_data'][asset.uuid] = {
                "uuid" : asset.uuid,
                "instance_count" : 0,
                "instances" : []
            }
            
        position = {
            "x" : x_pos * asset.mExtent.x * 200,
            "y" : y_pos * asset.mExtent.z * 200, # in Unity Y is up
            "z" : z_pos * 100,
            "rot" : rot
        }

        self.output['asset_data'][asset.uuid]['instances'].append(position)

    def placeCustom(self, asset, x_pos, y_pos, rot):
        pass

# Elevation asset placement
    def populateElevation(self, assetList):

        for x_pos in range(0, self.x):
            for y_pos in range(0, self.y):
    
                # get a random asset from list
                asset = assetList[numpy.random.randint(len(assetList))]['Asset']
                z_size = asset.mExtent.y * 2.0

                thickness = self.adaptiveThickness(x_pos, y_pos, z_size)
                for z_pos in range(0, thickness):
                    rot = numpy.random.randint(4)*90
                    newZ = (self.getPos(x_pos,y_pos,z_size) - z_pos )*z_size
                    self.placeAsset(asset, x_pos, y_pos, newZ, rot)

                self.poZ[x_pos][y_pos] = self.getPos(x_pos,y_pos,z_size)*z_size + z_size

    def adaptiveThickness(self, x_pos, y_pos, z_size) -> int:

        x = self.getPos(x_pos, y_pos, z_size)

        return int(max( 
            x - self.getPos( x_pos, max(y_pos-1, 0), z_size),
            x - self.getPos( x_pos, min(y_pos+1, self.y-1), z_size),
            x - self.getPos( max(x_pos-1, 0), y_pos, z_size),
            x - self.getPos( min(x_pos+1, self.x-1), y_pos, z_size),
            1
        ))

# Place object asset placement
    def populatePlaceObjects(self, assetList):

        placementPass = numpy.floor(self.generateElevationArray(self.x*32) * len(assetList))

        for x_pos in range(0, self.x):
            for y_pos in range(0, self.y):
                # get a random asset from list
                assetPos = int(placementPass[x_pos][y_pos])
                asset = assetList[assetPos]['Asset']
                probability = assetList[assetPos]['Probability']

                rot = numpy.random.randint(4)*90
                z_pos = self.poZ[x_pos][y_pos]

                if(numpy.random.randint(100) <= probability):
                    self.placeAsset(asset, x_pos, y_pos, z_pos, rot)
