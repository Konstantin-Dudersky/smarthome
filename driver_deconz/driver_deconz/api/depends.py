from ..deconz.sensors_collection import SensorCollection


sensors_type = SensorCollection


def sensors_depends() -> sensors_type:
    """Датчики."""
    return SensorCollection.instance()
