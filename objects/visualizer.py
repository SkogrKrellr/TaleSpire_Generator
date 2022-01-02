import numpy
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from objects.config import config as Config

DEFAULT_CMAP = Config.get('visualizer', 'cmap')


class Visualizer():

    def showImage(
        image,
        clipping=True,
        min=0,
        max=1
    ):
        plt.imshow(image, cmap=DEFAULT_CMAP, interpolation='None')

        if clipping:
            plt.clim(min, max)

        plt.colorbar()
        plt.show()

    def showImages(
        images,
    ):

        rows = 4
        columns = 3

        fig = plt.figure(figsize=(10, 7))
        for n, image in enumerate(images):
            fig.add_subplot(rows, columns, n+1)
            plt.imshow(image["map"])
            plt.axis('off')
            plt.title(image["name"])
        plt.show()

    def show3dPlot(matrix, clip01=True):
        (x, y) = numpy.meshgrid(
            numpy.arange(matrix.shape[0]),
            numpy.arange(matrix.shape[1]))
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        if clip01:
            ax.set_zlim3d(0, 1)

        surf = ax.plot_surface(x, y, matrix, cmap=DEFAULT_CMAP)
        fig.colorbar(surf)
        plt.show()
