import numpy
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from classes.config import config as Config

DEFAULT_CMAP = Config.get('visualizer', 'cmap')

class Vizualizer():

    def showImage(image, clip01 = True) -> None:
        plt.imshow(image, cmap=DEFAULT_CMAP, interpolation='None')

        if clip01:
            plt.clim(0,100)

        plt.colorbar()
        plt.show()

    def show3dPlot(matrix, clip01 = True):
        (x,y) = numpy.meshgrid(numpy.arange(matrix.shape[0]), numpy.arange(matrix.shape[1]))
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        if clip01:
            ax.set_zlim3d(0,1)
            
        surf = ax.plot_surface(x, y, matrix, cmap=DEFAULT_CMAP)
        fig.colorbar(surf)
        plt.show()

    
