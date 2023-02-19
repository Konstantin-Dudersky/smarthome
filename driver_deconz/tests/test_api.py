from fastapi.testclient import TestClient

from driver_deconz.api.main import Api

from driver_deconz.deconz import sensors


api = Api(
    depends_sensors=sensors.SensorCollection(
        sensors=[],
    ),
)
client = TestClient(api.app)


def test_sensors():
    response = client.get("/sensors")
    assert response.status_code == 200
