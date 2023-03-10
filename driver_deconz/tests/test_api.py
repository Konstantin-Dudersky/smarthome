from fastapi.testclient import TestClient

from driver_deconz.api.main import Api
from driver_deconz.deconz import sensors

from shared.simple_deque import SimpleDeque
from shared.tasks_runner import TasksRunner

api = Api(
    depends_sensors=sensors.SensorCollection(
        sensors=[],
        messagebus=SimpleDeque(),
    ),
    runner=TasksRunner(),
)
client = TestClient(api.app)


def test_sensors():
    response = client.get("/sensors")
    assert response.status_code == 200
