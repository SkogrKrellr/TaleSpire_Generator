import re
import json
import math
import numpy
from opensimplex import OpenSimplex 
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

    def setOctaves (self, *args ) -> None:
        self.octaves = args

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

# Elevation Generation 
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
            self.elevation += current_pass

        self.elevation /= octave_sum

 # Elevation Modifiers
    def multiplyByValue(self,) -> None:
        self.elevation = self.elevation * self.z

    def floorElevation(self, steps) -> None:
        self.elevation = numpy.floor(self.elevation*steps)/steps

    def powerElevation(self) -> None:
        self.elevation = self.elevation**self.exponent


# Terrain asset placement

    def populateElevation(self, assetList, randomRotation = True):
        output = {
            "unique_asset_count": 0,
            "asset_data": {}
        }

        rot = 0

        for x_pos in range(0, self.x):
            for y_pos in range(0, self.y):
                # get a random asset from list
                asset = assetList[numpy.random.randint(len(assetList))]

                if not asset.uuid in output['asset_data'].keys():
                    output['asset_data'][asset.uuid] = {
                        "uuid" : asset.uuid,
                        "instance_count" : 0,
                        "instances" : []
                    }

                x_size = asset.mExtent.x * 2.0
                y_size = asset.mExtent.z * 2.0 # in Unity Y is up
                z_size = asset.mExtent.y * 2.0

                if randomRotation:
                    rot = numpy.random.randint(4)*90

                for z_pos in range(0, int(self.adaptiveThickness(x_pos, y_pos, z_size)/z_size)):
                    
                    newZ = (math.ceil(self.elevation[x_pos][y_pos]/z_size)-z_pos)*z_size

                    position = {
                        "x" : x_pos * x_size * 100,
                        "y" :  y_pos * y_size * 100,
                        "z" : newZ * 100,
                        "rot" : 0
                    }

                    output['asset_data'][asset.uuid]['instances'].append(position)
        
        return json.dumps(output)


    def adaptiveThickness(self, x_pos, y_pos, z_size) -> int:

        x = self.getPos(x_pos, y_pos, z_size)

        return z_size * max( 
            abs( self.getPos( x_pos, max(y_pos-1, 0), z_size)-x ),
            abs( self.getPos( x_pos, min(y_pos+1, self.y-1), z_size)-x ),
            abs( self.getPos( max(x_pos-1, 0), y_pos, z_size)-x ),
            abs( self.getPos( min(x_pos+1, self.x-1), y_pos, z_size)-x ),
            1
        ) 
    
    def getPos(self, x_pos, y_pos, z_size):
            return math.ceil( self.elevation[ x_pos ][ y_pos ] / z_size )