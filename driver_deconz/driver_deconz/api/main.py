"""API."""

from fastapi import FastAPI, Depends

from . import dependencies

app = FastAPI()


@app.get("/")
def hello(sensors=dependencies.sensor_collection):
    return sensors().by_id(2).data
