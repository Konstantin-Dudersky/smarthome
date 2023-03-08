from fastapi.testclient import TestClient

from driver_deconz.api.main import Api
from driver_deconz.deconz import sensors

from shared.messagebus import MessageBus

api = Api(
    depends_sensors=sensors.SensorCollection(
        sensors=[],
        messagebus=MessageBus(),
    ),
)
client = TestClient(api.app)


def test_sensors():
    response = client.get("/sensors")
    assert response.status_code == 200
