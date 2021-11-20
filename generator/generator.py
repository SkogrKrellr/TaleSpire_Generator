import numpy
import re
from opensimplex import * 
from classes.visualizer import Vizualizer
from classes.config import config as Config

DEFAULT_X = int(Config.get('generator', 'default_x'))
DEFAULT_Y = int(Config.get('generator', 'default_y'))
DEFAULT_Z = int(Config.get('generator', 'default_z'))
DEFAULT_EXP = float(Config.get('generator', 'default_exponent'))
DEFAULT_SEED = int(Config.get('generator', 'seed')) #random value


class Generator:

    def __init__(self):
        self.setXYZ(DEFAULT_X, DEFAULT_Y, DEFAULT_Z)
        self.setOctaves(1, 0.5, 0.25, 0.125)
        self.setScales(1, 2, 4, 8)
        self.setExponent(DEFAULT_EXP)
        self.setSeed(DEFAULT_SEED)

# Misc
    def prettyPrintElevation(self):
        arrayString = numpy.array2string(
            self.elevation,
        )

        return re.sub(' +', ' ', arrayString)

# Setters / Getters
    def setXYZ (self, x, y, z) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.max_size = max(x,y,z)
        self.elevation = numpy.zeros((self.y, self.x))

    def setOctaves (self, *args ) -> None:
        self.octaves = args

    def setScales (self, *args ) -> None:
        self.scales = args

    def setExponent (self, exponent ) -> None:
        self.exponent = float(exponent)

    def setSeed (self, seed=DEFAULT_SEED) -> None:
        self.noise = OpenSimplex(seed)
    
# Generation 
    def noiseXY(self, y, x) -> float:
        return self.noise.noise2d(y,x)

    def getElevationXYValue(self, x, y, wavelength) -> float:
        value = self.noiseXY( y/wavelength, x/wavelength)
        return (1 + value) * 0.5

    def generateElevationArray(self, scale):
        current_pass = numpy.zeros((self.y, self.x))

        for y in range(0, self.y):
            for x in range(0, self.x):
                current_pass[y][x] = self.getElevationXYValue(y,x,self.max_size/scale)

        return current_pass

    def generateElevation (self) -> None:
        octave_sum = sum(self.octaves)
        
        for count, octave in enumerate(self.octaves):
            current_pass = octave * self.generateElevationArray(self.scales[count])
            self.elevation += current_pass

        self.elevation /= octave_sum

    def scaleToZHeight(self) -> None:
        self.elevation = self.elevation * self.z

    def floorElevation(self, steps) -> None:
        self.elevation = numpy.floor(self.elevation*steps)/steps

    def powerElevation(self) -> None:
        self.elevation = self.elevation**self.exponent
