from math import log1p
import numpy
import poisson_disc as pd
from opensimplex import OpenSimplex
from objects.config import config as Config
from objects.visualizer import Visualizer


class Noise:

    def __init__(self, seed):
        self.setSeed(seed)

    def setSeed(self, seed):
        self.noise = OpenSimplex(seed)
        numpy.random.seed(seed)

    def setOctaves(self, *args):
        self.octaves = args

    def setScales(self, *args):
        self.scales = args

    def noiseXY(self, x, y):
        return self.noise.noise2d(x, y)

    def getNoiseXYValue(self, x, y, wavelength):
        value = self.noiseXY(x/wavelength, y/wavelength)
        return (1 + value) * 0.5

    def getRidgeNoiseXY(self, x, y, wavelength):
        return 2 * (0.5 - abs(0.5 - self.getNoiseXYValue(x, y, wavelength)))

    def generateSimpleNoiseArray(
        self,
        xSize,
        ySize,
        scale,
        offset=[0, 0],
        useRidgeNoise=False
    ):
        currentPass = numpy.zeros((xSize, ySize))
        for x in range(0, xSize):
            for y in range(0, ySize):
                if useRidgeNoise:
                    currentPass[x][y] = self.getRidgeNoiseXY(
                        x + offset[0],
                        y + offset[1],
                        scale
                    )
                else:
                    currentPass[x][y] = self.getNoiseXYValue(
                        x + offset[0],
                        y + offset[1],
                        scale
                    )
        return currentPass

    def generateComplexNoiseArray(
        self,
        xSize, ySize,
        combinedPasses=True,
        octaves=None,
        scales=None,
        offset=[0, 0],
        useRidgeNoise=False
    ):

        if octaves is None:
            octaves = self.octaves
        if scales is None:
            scales = self.scales

        maxSize = max(xSize, ySize)
        octaveSum = sum(octaves)

        passes = []

        for iteration, octave in enumerate(octaves):
            passes.append(octave * self.generateSimpleNoiseArray(
                xSize,
                ySize,
                maxSize/scales[iteration],
                offset,
                useRidgeNoise
            ))

        if combinedPasses:
            return self.compileNoiseMap(passes, octaveSum)

        return passes

    def compileNoiseMap(self, passes, octaveSum):

        resultingPass = numpy.zeros(passes[0].shape)

        for elevation in passes:
            resultingPass += elevation

        return resultingPass/octaveSum

    def getRandomNoiseMap(self, sizes, offset, clumping, randomWeight):

        maxSize = max(sizes["x"], sizes["y"])

        noiseMap = self.generateSimpleNoiseArray(
            sizes["x"],
            sizes["y"],
            maxSize/clumping,
            offset
        )

        # Set 6 distinct levels of density
        # 0% 20% 40% 60% 80% 100%
        noiseMap = numpy.around((1.0-noiseMap)*5)/5

        # Then generate randomness to make the edges more fuzzy
        randomMap = numpy.random.random((sizes["x"], sizes["y"]))

        # Then combine them
        noiseMap = (noiseMap * (1-randomWeight)) + (randomMap * randomWeight)

        # Normalize so that values are in range of [0.0, 1.0]
        correctionMin = numpy.amin(noiseMap)
        correctionMax = numpy.amax(noiseMap)
        noiseMap -= correctionMin
        noiseMap *= 1.0/(correctionMax-correctionMin)

        return noiseMap * 100.0
