import numpy
from opensimplex import *
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

DEFAULT_X = 50
DEFAULT_Y = 50
DEFAULT_Z = 50
DEFAULT_SEED = 1487 #random value
DEFAULT_CMAP = 'tab20b'

class Generator:

    def __init__(self):
        self.setXYZ(DEFAULT_X, DEFAULT_Y, DEFAULT_Z)
        self.setOctaves(1, 0.5, 0.25)
        self.setScales(1, 2, 4)
        self.setExponent(1)
        self.setSeed(DEFAULT_SEED)

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
        self.exponent = exponent

    def setSeed (self, seed=DEFAULT_SEED) -> None:
        self.noise = OpenSimplex(seed)
    
    def generateElevation (self) -> None:
        octave_sum = sum(self.octaves)
        
        for count, octave in enumerate(self.octaves):
            current_pass = octave * self.getNoiseValueArray(self.scales[count])
            self.elevation += current_pass

        self.elevation /= octave_sum
        self.elevation = self.elevation**self.exponent

        #self.addImage(self.elevation)
        #self.show3dPlot(self.elevation)
        
    def noiseXY(self, y, x) -> float:
        noise = self.noise.noise2d(y,x)
        return noise
    
    def getNoiseXYValue(self, x, y, wavelength) -> float:
        value = self.noiseXY( y/wavelength, x/wavelength)
        return (1 + value) * 0.5

    def getNoiseValueArray(self, scale) -> numpy.array:
        current_pass = numpy.zeros((self.y, self.x))

        for y in range(0, self.y):
            for x in range(0, self.x):
                current_pass[y][x] = self.getNoiseXYValue(y,x,self.max_size/scale)

        return current_pass


# unrelated to generation only here for previewing terrain
    def addImage(self, image) -> None:
        plt.imshow(image, cmap=DEFAULT_CMAP, interpolation='None')
        plt.clim(0,1)
        plt.colorbar()
        plt.show()

    def show3dPlot(self, matrix):
        (x,y) = numpy.meshgrid(numpy.arange(matrix.shape[0]), numpy.arange(matrix.shape[1]))
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.set_zlim3d(0,1)
        surf = ax.plot_surface(x, y, matrix, cmap=DEFAULT_CMAP)
        fig.colorbar(surf)
        plt.show()

