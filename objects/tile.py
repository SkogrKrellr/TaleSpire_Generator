from objects.config import *
from objects.asset import Asset


class Tile(Asset):
    """
    Class for Tile type assets. This class extends Assets
    """

    def __init__(self, object) -> None:
        Asset.__init__(self, object)
