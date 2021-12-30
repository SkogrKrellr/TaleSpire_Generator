from objects.config import *
from objects.asset import Asset


class Tile(Asset):

    def __init__(self, object) -> None:
        Asset.__init__(self, object)
