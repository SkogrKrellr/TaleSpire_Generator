from classes.config import config as Config
from generator.settings import Settings

DEFAULT_DENSITY = float(Config.get('terrainSettings', 'default_density'))
DEFAULT_CLUMPING = float(Config.get('terrainSettings', 'default_clumping'))
DEFAULT_RANDOM_NUDGE_ENABLED = bool(Config.getboolean('terrainSettings', 'random_nudge_enabled'))
DEFAULT_RANDOM_ROTATION_ENABLED = bool(Config.getboolean('terrainSettings', 'random_rotation_enabled'))
DEFAULT_HEIGHT_MIN = bool(Config.getboolean('terrainSettings', 'height_min'))
DEFAULT_HEIGHT_MAX = float(Config.get('terrainSettings', 'height_max'))
DEFAULT_BLEND_MULTIPLIER = float(Config.get('terrainSettings', 'blend_multiplier'))

class TerrainSettings(Settings):

    def __init__(self, passedSettings):
        Settings.__init__(self, passedSettings)
        keys = passedSettings.keys()
        self.params.update({
            "density" : passedSettings['density']  if 'density' in keys else DEFAULT_DENSITY,
            "clumping" : passedSettings['clumping'] if 'clumping' in keys else DEFAULT_CLUMPING,

            "randomNudgeEnabled" : passedSettings['randomNudge'] if 'randomNudge' in keys else DEFAULT_RANDOM_NUDGE_ENABLED,
            "randomRotationEnabled" : passedSettings['randomRotation'] if 'randomRotation' in keys else DEFAULT_RANDOM_ROTATION_ENABLED,

            "heightMin" : passedSettings['heightMin'] if 'heightMin' in keys else DEFAULT_HEIGHT_MIN,
            "heightMax" : passedSettings['heightMax'] if 'heightMax' in keys else DEFAULT_HEIGHT_MAX,
            "blendHeightMultiplier" : passedSettings['blendHeightMultiplier'] if 'blendHeightMultiplier' in keys else DEFAULT_BLEND_MULTIPLIER
        })