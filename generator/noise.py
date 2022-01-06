import math
import numpy
from opensimplex import OpenSimplex
from config.config import config as Config
from visualizer.visualizer import Visualizer


class Noise:
    """
    Class for a Noise generation using Opensimplex.

    Attributes:
        noise (OpenSimplex): object that generates noise
        octaves (list of floats): multipliers for noises intensity
        scales (list of floats): multipliers for noises scale
    """

    def __init__(self, seed):
        """
        Constructor for Noise class.

        Parameters:
            seed (any): seed for the noise
        """

        self.setSeed(hash(seed))

    def setSeed(self, seed):
        """
        Function to set both generator seeds.

        Parameters:
            seed (any): seed for the generators
        """

        self.noise = OpenSimplex(seed)
        numpy.random.seed(seed)

    def setOctaves(self, *args):
        """
        Function to set octaves.

        Parameters:
            args (list of floats): multipliers for noises intensity
        """

        self.octaves = args

    def setScales(self, *args):
        """
        Function to set scales.

        Parameters:
            args (list of floats): multipliers for noises scale
        """

        self.scales = args

    def noiseXY(self, x, y):
        """
        Function to get noise value at point X Y.

        Parameters:
            x (int): X coordinate for noise
            y (int): Y coordinate for noise

        Returns:
            float: value at that coordinate from -1.0 to 1.0
        """
        value = self.noise.noise2d(x, y)
        return value

    def getNoiseXYValue(self, x, y, scaleX, scaleY):
        """
        Function to get noise value at point X Y, scaled by a value.
        And normalized to values between 0.0 and 1.0

        Parameters:
            x (int): X coordinate for noise
            y (int): Y coordinate for noise
            scaleX (float): Scaling factor for X
            scaleY (float): Scaling factor for Y

        Returns:
            float: value at that scaled coordinate from 0.0 to 1.0
        """
        value = self.noiseXY(x/scaleX, y/scaleY)
        return (1 + value) * 0.5

    def getRidgeNoiseXY(self, x, y, scaleX, scaleY):
        """
        Function to change the distribution of values.
        The new distribution follows the formula:

            y = 2 * abs(0.5 - x)

        y - new value
        x - old value

        Parameters:
            x (int): X coordinate for noise
            y (int): Y coordinate for noise
            scaleX (float): Scaling factor for X
            scaleY (float): Scaling factor for Y

        Returns:
            float: value at that scaled coordinate from 0.0 to 1.0
        """

        noiseValue = self.getNoiseXYValue(x, y, scaleX, scaleY)
        return 2 * (0.5 - abs(0.5 - noiseValue))

    def generateSimpleNoiseArray(
        self,
        xSize, ySize,
        scaleX,
        scaleY=None,
        offset={"x": 0, "y": 0},
        useRidgeNoise=False
    ):
        """
        Function generates a 2d array of size xSize x ySize,
        and fills it with simple noise.

        Parameters:
            xSize (int): size of generated noise in X direction
            ySize (int): size of generated noise in Y direction
            scaleX (float): scaling factor in X direction
            scaleY (float, None): scaling factor in Y direction
            offset (list): Offset in X and Y direction
            useRidgeNoise (bool): Use value remaping

        Returns:
            array: value at that scaled coordinate from 0.0 to 1.0
        """

        if scaleY is None:
            scaleY = scaleX

        currentPass = numpy.zeros((xSize, ySize))
        for x in range(0, xSize):
            for y in range(0, ySize):
                if useRidgeNoise:
                    currentPass[x][y] = self.getRidgeNoiseXY(
                        x + offset["x"],
                        y + offset["y"],
                        scaleX,
                        scaleY
                    )
                else:
                    currentPass[x][y] = self.getNoiseXYValue(
                        x + offset["x"],
                        y + offset["y"],
                        scaleX,
                        scaleY
                    )
        return currentPass

    def generateComplexNoiseArray(
        self,
        xSize, ySize,
        maxSize,
        combinedPasses=True,
        octaves=None,
        scales=None,
        offset={"x": 0, "y": 0},
        useRidgeNoise=False
    ):
        """
        Function generates a 2d array of size xSize x ySize,
        and fills it with complex noise.
        Many passes of noise are generated, combined
        then normalized to values between 0.0 and 1.0

        Parameters:
            xSize (int): size of generated noise in X direction
            ySize (int): size of generated noise in Y direction
            noiseSizeX (float): scaling factor in X direction
            noiseSizeY (float): scaling factor in Y direction
            combinedPasses (bool): Should each be combined
            octaves (list of floats): list of noise level intensities
            scales (list of floats): list of noise level scales
            offset (list): 2 values for X and Y offsets
            useRidgeNoise (bool): Use value remaping

        Returns:
            list: list of arrays of size xSize x ySize
            array: array of size xSize x ySize with combined noise passes
        """

        if octaves is None:
            octaves = self.octaves
        if scales is None:
            scales = self.scales

        octaveSum = sum(octaves)

        passes = []

        for iteration, octave in enumerate(octaves):
            passes.append(octave * self.generateSimpleNoiseArray(
                xSize,
                ySize,
                maxSize/scales[iteration],
                offset=offset,
                useRidgeNoise=useRidgeNoise
            ))

        if combinedPasses:
            return self.compileNoiseMap(passes, octaveSum)

        return passes

    def compileNoiseMap(
        self,
        passes,
        octaveSum
    ):
        """
        Function compiles noise passes, combines them into
        one array, and normalizes it to values between 0.0 and 0.1

        Parameters:
            passes (array): array of passes to be combined
            octaveSum (float): Sum of all pass intensities

        Returns:
            array: combined value passes normalized
        """

        resultingPass = numpy.zeros(passes[0].shape)

        for elevation in passes:
            resultingPass += elevation

        return resultingPass/octaveSum

    def getRandomNoiseMap(
        self,
        sizes,
        offset,
        clumping,
        randomWeight
    ):
        """
        Function compiles noise passes, combines them into
        one array, and normalizes it to values between 0.0 and 0.1

        Parameters:
            sizes (pair): x and y map size
            offset (pair): values for how much x and y should be offset
            clumping (float): scale for noise
            randomWeight (float): how much randomness affects the map

        Returns:
            array: Generated noise map multiplied by 100.0
        """

        maxSize = max(sizes["x"], sizes["y"])

        noiseMap = self.generateSimpleNoiseArray(
            sizes["x"],
            sizes["y"],
            maxSize/clumping,
            offset=offset
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
