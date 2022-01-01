from objects.config import config as Config

DEFAULT_DENSITY = float(Config.get('settings', 'default_density'))
DEFAULT_CLUMPING = float(Config.get('settings', 'default_clumping'))


class Settings:

    def __init__(self, passedSettings):
        keys = passedSettings.keys()
        self.params = {
            "asset": passedSettings['asset'],
            "density": passedSettings['density'] if 'density' in keys else DEFAULT_DENSITY,
            "clumping": passedSettings['clumping'] if 'clumping' in keys else DEFAULT_CLUMPING,
        }

    def getParam(self, param=None):
        if param is None:
            return self.params
        if param not in self.params.keys():
            return None
        return self.params[param]

    def __str__(self):
        output = ""
        for key in self.params.keys():
            output += f"{key}: {self.params[key]}\n"
        return output.strip()
