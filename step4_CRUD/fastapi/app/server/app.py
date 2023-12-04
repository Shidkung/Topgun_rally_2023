from fastapi import FastAPI
from server.routes.water import router as WaterRouter
from server.mqtt.sensor_data import router as MqttRouter
from server.mockup.get_mockup import router as MockRouter

app = FastAPI()

####router api part

app.include_router(MqttRouter, tags=["MQTT"],prefix="/mqtt")
app.include_router(MockRouter, tags=["Mock"],prefix="/mock")
app.include_router(WaterRouter, tags=["Water"], prefix="/water")

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "My REST API server!"}

