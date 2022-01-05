from config.config import *
from objects.asset import Asset


class Prop(Asset):
    """
    Class for Prop type assets. This class extends Assets
    """

    def __init__(self, object) -> None:
        Asset.__init__(self, object)
