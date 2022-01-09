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
        images,
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

        rows = 1
        columns = len(images)

        color_map = plt.cm.get_cmap(DEFAULT_CMAP)
        reversed_color_map = color_map.reversed()

        fig = plt.figure(figsize=(10, 10))
        for n, image in enumerate(images):
            fig.add_subplot(rows, columns, n+1)
            plt.imshow(image["map"], cmap=reversed_color_map, interpolation='None')
            plt.title(image["name"])
            # plt.clim(0, 1)
            plt.colorbar()
        plt.show()

    def show3dPlot(
        image,
        clip01=True
    ):

        """
        Function for showing a single map on the screen, as a 3d model.

        Parameters:
            image (2d array): A 2d array to be displayed.
            clip01 (bool): Enable clipping of values to 0 to 1.
        """
        (x, y) = numpy.meshgrid(
            numpy.arange(image.shape[0]),
            numpy.arange(image.shape[1]))
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        if clip01:
            ax.set_zlim3d(0, 1)

        surf = ax.plot_surface(x, y, image, cmap=DEFAULT_CMAP)
        fig.colorbar(surf)
        plt.show()
