from objects.config import config as Config

DEFAULT_DENSITY = float(Config.get('settings', 'default_density'))
DEFAULT_CLUMPING = float(Config.get('settings', 'default_clumping'))

class Settings:

    def __init__(self, passedSettings):
        keys = passedSettings.keys()
        self.params = {
            "asset" : passedSettings['asset'],
            "densityMax" : passedSettings['densityMax']  if 'densityMax' in keys else DEFAULT_DENSITY,
            "clumping" : passedSettings['clumping'] if 'clumping' in keys else DEFAULT_CLUMPING,
        }

    def getParam(self, param = None):
        if param is None:
            return self.params
        return self.params[param]