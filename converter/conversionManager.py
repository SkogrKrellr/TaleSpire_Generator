from .encode import encode
from .decode import decode


class ConversionManager():
    """
    Class for a Conversion manager. It is responsible for encoding data into
    TaleSpire readable format and decoding data into dictionary format
    """

    def decode(data):
        """
        Function to decode TaleSpire string into dictionary

        Parameters:
            data (str): TaleSpire string

        Returns:
            dict: decoded dictionary
        """

        return decode(data)

    def encode(data):
        """
        Function to encode dictionary into TaleSpire readable string

        Parameters:
            data (dict): dictionary to be encoded

        Returns:
            str: TaleSpire readable string
        """

        return encode(data)
