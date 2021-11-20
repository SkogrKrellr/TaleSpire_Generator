from classes.config import *
from classes.asset import Asset

class Tile(Asset):

    def __init__(self, object) -> None:
        Asset.__init__(self, object)
