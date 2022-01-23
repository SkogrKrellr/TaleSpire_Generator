import json
from generator.generator import Generator
from objects.assetManager import AssetManager
import pyperclip as pc

from visualizer.visualizer import Visualizer

generator = Generator()

seed = 2022

# Size per tile
x, y, z = 10, 10, 10
exponent = 1.3

# How many consequitive tiles will be generated
xTiles, yTiles = 2, 3

# Set operating variables

generator.setXYZ(x, y, z) # How large will one tile be
generator.setExponent(exponent) # What is the exponent for redistribution
generator.setSeed(seed) # Seed for repeatable results
generator.setOctaves(1, 0.5, 0.25)
generator.setScales(1, 2, 4)
generator.setUsePreciseHeight(True) # If generating more than 1x1 consequitive tiles, this should be enabled
generator.setUseRidgeNoise(False) # Redistributes values to make ridges, good for deserts
generator.setUseHeightBasedTerrainAssetPlacement(False) # Place terrain assets based on height

# Possible options for terrain asset:
# 
# "asset":                  [String]  Asset that is going to be placed [REQUIRED]
# "clumping":               [Integer] How much similar tiles will clump together
# "density":                [Integer] Proportion of it in terrain (If height based distribution disabled),
# "heightMin":              [Integer] Minimum height at which this tile will appear (If height based distribution enabled),
# "heightMax":              [Integer] Maximum height at which this tile will appear (If height based distribution enabled),
# "blendHeightMultiplier":  [Float] How much tiles spread from minimum and maximum height (If height based distribution enabled),

terrainAssets = [
    {  # Grass - Lush
        "asset": "01c3a210-94fb-449f-8c47-993eda3e7126",
        "density": 10
    },
    {  # Grass - Sparse
        "asset": "3911d10d-142b-4f33-9fea-5d3a10c53781",
        "density": 90
    },
]


# This is how we add custom complex assets
customTreeUUID = AssetManager.addCustomAsset(
                "Tree 4 Tall",
                "```H4sIAAAAAAAACzv369xFJgZmBgYGV8sOe+Zcb6+FuwOFhA/vvMUIFGP54+9t4qri2XJlvvU8595GJqDYnexlT8+YiztvObZwR4/xpJcgdYwMEmxACmiOAIsBQwMjEwMHUwADBEBoAGi/N01oAAAA```"
            )


# Possible options for place object assets:
# 
# "asset":                  [String] Asset UUID that is going to be placed [REQUIRED]
# "density":                [Integer] How often do objects appear 
# "verticalOffset":         [Float]   Vertical offset for objecy (if you want to place things into the earth)
# "clumping":               [Float]   How much similar tiles will clump together,
# "randomNoiseWeight":      [Float]   How much random random noise affects object placement
# "randomNudgeEnabled":     [Boolean] Will object be slightly nudged from its center
# "randomRotationEnabled":  [Boolean] Will objects have random rotation enabled
# "heightBasedMultiplier":  [Float]   Multiplier fir how much more likely are objects to appear lower in terrain 
# "heightBasedOffset":      [Float]   Constant offset of how likelieness of objects are to appear lower
# "placeOnCenter":          [Boolean] Objects will be placed on center of tiles

placeObjects = [
    {  # Custom Tree
        "asset": customTreeUUID,
        "density": 17,
        "clumping": 64,
        "randomNoiseWeight": 0.3,
    },
    {  # Fern 02
        "asset": "98259887-53c2-41d4-a54f-6140b6acf020",
        "density": 30,
        "clumping": 3,
        "randomNoiseWeight": 0.5,
        "randomNudgeEnabled": False,
        "randomRotationEnabled": True,
        "placeOnCenter": False
    },
]



generator.pregenerate(
    terrainAssets,
    placeObjects,
    [xTiles, yTiles]
)

# If we want to visualize the used heightmap in 2d
Visualizer.showImage(generator.elevation, True, 0, z)

# If we want to visualize the used heightmap in 2d
Visualizer.show3dPlot(generator.elevation, True, 0, z)

# If we want to visualize the object placements
Visualizer.showImages(generator.objectPlacements)

print("Do you want to continue with these results? Enter - yes, Ctrl-C - no")
input()

output = generator.generate()

# Quick and dirty json output
# print(json.dumps(output, indent=4))

# More elegant output to clipboard
print(f"Your terrain consists of {xTiles} by {yTiles} tiles.")
print("Now Just paste them one by one into talespire, lining them up!")

for entry in output:
    print(f"\t{entry['x']+1} : {entry['y']+1} copied into clipboard! Press enter to copy next tile", end = '')
    pc.copy(entry["output"])
    input()

print("All Done!")