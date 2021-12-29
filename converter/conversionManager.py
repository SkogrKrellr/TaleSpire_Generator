from .encode import encode
from .decode import decode

class ConversionManager():

    def __init__ (self):
        pass

    def decode( data ):
        return decode(data)

    def encode( data ):
        return encode(data)