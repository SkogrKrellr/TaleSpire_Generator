import numpy
import matplotlib.pyplot as plt
from config.config import config as Config

DEFAULT_CMAP = Config.get('visualizer', 'cmap')


class Visualizer():
    """
    Class for Visualizing 2d arrays and heightmaps.
    """

    def showImage(
        image,
        clipping=True,
        min=0.0,
        max=1.0
    ):
        """
        Function for showing a single map on the screen as 2d plots.

        Parameters:
            image (2d array): A 2d array to be displayed.
            clipping (bool): Enable clipping of displayed image.
            min (float): Minimum value to be displayed image.
            max (float): MAximum value to be displayed image.
        """

        plt.imshow(image, cmap=DEFAULT_CMAP)

        if clipping:
            plt.clim(min, max)

        plt.colorbar()
        plt.show()

    def showImages(
        images
    ):
        """
        Function for showing a single map on the screen as 2d plots.

        Input dictionary structure:

            [
                {  "name" : str
                    "map" : 2d array },
                ...
                {}
            ]

        Parameters:
            images (list of dict): A list of dictionaries to be displayed
        """

        rows = int(numpy.ceil(len(images)/3))
        columns = 4

        color_map = plt.cm.get_cmap(DEFAULT_CMAP)

        fig = plt.figure(figsize=(10, 10))
        for n, image in enumerate(images):
            fig.add_subplot(rows, columns, n+1)
            plt.imshow(image["map"], cmap=color_map, interpolation='None')
            plt.title(image["name"])
        plt.show()

    def show3dPlot(
        image,
        clipping=True,
        min=0.0,
        max=1.0
    ):

        """
        Function for showing a single map on the screen, as a 3d model.

        Parameters:
            image (2d array): A 2d array to be displayed.
            clipping (bool): Enable clipping of displayed image.
            min (float): Minimum value to be displayed image.
            max (float): MAximum value to be displayed image.
        """
        (x, y) = numpy.meshgrid(
            numpy.arange(image.shape[0]),
            numpy.arange(image.shape[1]))
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        if clipping:
            ax.set_zlim3d(min, max)

        surf = ax.plot_surface(x, y, image, cmap=DEFAULT_CMAP)
        fig.colorbar(surf)
        plt.show()
