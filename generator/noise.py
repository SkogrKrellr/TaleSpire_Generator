from math import log1p
import numpy
import poisson_disc as pd
from opensimplex import OpenSimplex
from classes.config import config as Config

class Noise:
    def __init__ (self, seed):
        self.setSeed(seed)

    def setSeed (self, seed) -> None:
        self.noise = OpenSimplex(seed)
        numpy.random.seed(seed)
    
    def setOctaves (self, *args ) -> None:
        self.octaves = args

    def setScales (self, *args ) -> None:
        self.scales = args

    def noiseXY(self, x, y) -> float:
        return self.noise.noise2d(x,y)

    def getNoiseXYValue(self, x, y, wavelength) -> float:
        value = self.noiseXY( x/wavelength, y/wavelength)
        return (1 + value) * 0.5

    def getRidgeNoiseXY(self, x, y, wavelength) -> float:
        return  2 * (0.5 - abs(0.5 - self.getNoiseXYValue(x, y, wavelength)))

    def generateSimpleNoiseArray(self, xSize, ySize, scale, xOffset = 0, yOffest = 0, useRidgeNoise = False):
        currentPass = numpy.zeros((xSize, ySize))

        for x in range(0, xSize):
            for y in range(0, ySize):
                if useRidgeNoise:
                    currentPass[x][y] = self.getRidgeNoiseXY( x+xOffset, y+yOffest ,scale)
                else:
                    currentPass[x][y] = self.getNoiseXYValue( x+xOffset, y+yOffest ,scale)
        return currentPass

    def generateComplexNoiseArray (self, xSize, ySize, combinedPasses = True, octaves=None, scales=None, offset = {"x": 0, "y": 0}, useRidgeNoise = False):
        if octaves is None: octaves = self.octaves
        if scales is None: scales = self.scales

        maxSize = max(xSize, ySize)
        octaveSum = sum(octaves)

        passes = []

        for iteration, octave in enumerate(octaves):
            passes.append(octave * self.generateSimpleNoiseArray( xSize, ySize, maxSize/scales[iteration], offset["x"], offset["y"], useRidgeNoise))
            
        if combinedPasses:
            return self.compileNoiseMap(passes, octaveSum)
        
        return passes

    def compileNoiseMap(self, passes, octaveSum):

        resultingPass = numpy.zeros(passes[0].shape)

        for iteration, elevation in enumerate(passes):
            resultingPass += passes[iteration]

        return resultingPass/octaveSum 

    def getRandomNoiseMap(self, sizes, offset, clumping, randomWeight):

        maxSize = max(sizes["x"], sizes["y"])
    
        noiseMap = self.generateSimpleNoiseArray(
            sizes["x"],
            sizes["y"],
            maxSize/clumping,
            offset["x"],
            offset["y"]
        ) 

        noiseMap = numpy.around((1.0-noiseMap)*3)/3

        randomMap = numpy.random.random((sizes["x"], sizes["y"]))

        noiseMap = (noiseMap * (1-randomWeight)) + (randomMap * randomWeight)

        correctionMin = numpy.amin(noiseMap)
        correctionMax = numpy.amax(noiseMap)

        noiseMap -= correctionMin
        noiseMap *= 1.0/(correctionMax-correctionMin)

        return noiseMap * 100.0

