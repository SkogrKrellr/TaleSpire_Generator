from objects.config import config as Config
from .settings import Settings

DEFAULT_CLUMPING = float(Config.get('terrainSettings', 'default_clumping'))
DEFAULT_HEIGHT_MIN = bool(Config.getboolean('terrainSettings', 'height_min'))
DEFAULT_HEIGHT_MAX = float(Config.get('terrainSettings', 'height_max'))
DEFAULT_BLEND_MULTIPLIER = float(Config.get('terrainSettings', 'blend_height_multiplier'))


class TerrainSettings(Settings):

    def __init__(self, passedSettings):
        Settings.__init__(self, passedSettings)
        keys = passedSettings.keys()
        self.params.update({
            "clumping": passedSettings['clumping'] if 'clumping' in keys else DEFAULT_CLUMPING,
            "heightMin": passedSettings['heightMin'] if 'heightMin' in keys else DEFAULT_HEIGHT_MIN,
            "heightMax": passedSettings['heightMax'] if 'heightMax' in keys else DEFAULT_HEIGHT_MAX,
            "blendHeightMultiplier": passedSettings['blendHeightMultiplier'] if 'blendHeightMultiplier' in keys else DEFAULT_BLEND_MULTIPLIER
        })
