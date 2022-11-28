from ..deconz.sensors_collection import SensorCollection


def sensor_collection():
    return SensorCollection.instance()
