import numpy


def multiplyByValue(noiseMap, value):
    """
    Function to multiply noisemap by a value.

    Parameters:
        noieMap (array): noisemap to be changed
        value (float): value for multiplication

    Returns:
        array: modified noiseMap
    """

    noiseMap *= value
    return noiseMap


def createTerrases(noiseMap, steps):
    """
    Function to create terrasses.

    Parameters:
        noieMap (array): noisemap to be changed
        steps (int): amount of terrase levels

    Returns:
        array: modified noiseMap
    """

    noiseMap = numpy.floor(noiseMap*steps)/steps
    return noiseMap


def redistribute(noiseMap, exponent):
    """
    Function to redestribute values with exponent.

    Parameters:
        noieMap (array): noisemap to be changed
        exponent (float): exponent to be applied

    Returns:
        array: modified noiseMap
    """

    noiseMap **= exponent
    return noiseMap


def ridgeNoise(noiseMap):
    """
    Function to change the distribution of values.
    The new distribution follows the formula:

        y = 2 * (0.5 - abs(0.5 - x))

    y - new value
    x - old value

    Parameters:
        noieMap (array): noisemap to be changed

    Returns:
        array: modified noiseMap
    """

    noiseMap = 2 * (0.5 - abs(0.5 - noiseMap))
    return noiseMap


def raiseFloor(noiseMap, level):
    """
    Function to set a floor level

    Parameters:
        noieMap (array): noisemap to be changed
        level (float): floor level (0.0 - 1.0)

    Returns:
        array: modified noiseMap
    """
    for y, x in numpy.ndindex(noiseMap.shape):
        noiseMap[y, x] = max(noiseMap[y][x], level)
    return noiseMap


def lowerCeiling(noiseMap, level):
    """
    Function to set a ceiling level

    Parameters:
        noieMap (array): noisemap to be changed
        level (float): floor level (0.0 - 1.0)

    Returns:
        array: modified noiseMap
    """

    for y, x in numpy.ndindex(noiseMap.shape):
        noiseMap[y, x] = min(noiseMap[y][x], level)
    return noiseMap


def normalize(noiseMap):
    """
    Function to set a set scale noiseMap, so that its lowest
    value would be 0.0 and the highest value 1.0

    Parameters:
        noieMap (array): noisemap to be changed

    Returns:
        array: modified noiseMap
    """

    min = numpy.amin(noiseMap)
    max = numpy.amax(noiseMap)

    noiseMap -= min
    noiseMap /= (max-min)
    return noiseMap
