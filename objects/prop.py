from objects.config import *
from objects.asset import Asset


class Prop(Asset):

    def __init__(self, object) -> None:
        Asset.__init__(self, object)
