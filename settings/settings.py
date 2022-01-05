from config.config import config as Config

DEFAULT_DENSITY = float(Config.get('settings', 'default_density'))
DEFAULT_CLUMPING = float(Config.get('settings', 'default_clumping'))


class Settings:
    """
    This is a class for setting and fetching settings.

    Attributes:
        params (dict): A dictionary for settings.
    """

    def __init__(
        self,
        passedSettings
    ):
        """
        The constructor for Settings class.

        If no value is supplied in the parsedSettings, then It defaults
        to a value in the config.ini file

        Parameters:
            passedSettings (dict, None): A dictionary to be converted to settings.
        """

        keys = passedSettings.keys()
        self.params = {
            "asset": passedSettings['asset'],
            "density": passedSettings['density'] if 'density' in keys else DEFAULT_DENSITY,
            "clumping": passedSettings['clumping'] if 'clumping' in keys else DEFAULT_CLUMPING,
        }

    def getParam(
        self,
        param=None
    ):
        """
        The function to get parameter from settings.

        Parameters:
            param (str, None): parameter to be fetched.

        Returns:
            str: If the param to fetch is a valid setting.
            None: If the param to fetch is not a valid setting.
            dict: If the no param specified.
        """

        if param is None:
            return self.params
        if param not in self.params.keys():
            return None
        return self.params[param]

    def setParam(
        self,
        paramName,
        value
    ):
        """
        The function to set parameter.

        Parameters:
            paramName (str): parameter to be changed.
            value (any): new value for the parameter to be changed.
        """

        if paramName in self.params.keys():
            self.params[paramName] = value

    def __str__(self):
        """
        The function to convert the object to a string.
        """

        output = ""
        for key in self.params.keys():
            output += f"{key}: {self.params[key]}\n"
        return output.strip()
