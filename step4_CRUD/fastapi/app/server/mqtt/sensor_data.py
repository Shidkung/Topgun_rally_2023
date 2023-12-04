from fastapi import APIRouter 
#fastapi_mqtt
from fastapi_mqtt.fastmqtt import FastMQTT
from fastapi_mqtt.config import MQTTConfig
import json

from server.database import (
    add_water,
    delete_water,
    retrieve_water,
    retrieve_waters,
    update_water,
    add_height,
    retrieve_heights
)
from server.models.water import (
    ErrorResponseModel,
    ResponseModel,
    WaterSchema,
    UpdateWaterModel,
    UpdateheightModel,
    heightSchema
)
mqtt_config = MQTTConfig(
    host ='192.168.1.2',
    port= 1883,
    keepalive = 60,
    username="TGR_GROUP17",
    password="MQ405O"
    )

fast_mqtt = FastMQTT(config=mqtt_config)

router = APIRouter()

fast_mqtt.init_app(router)

from server.database import (
    add_water,
)
from server.models.water import (
    ErrorResponseModel,
    ResponseModel,
    WaterSchema,
)



#@fast_mqtt.on_message()
#async def message(client, topic, payload, qos, properties):
#    print("Received message: ", topic, payload.decode(), qos, properties)
@fast_mqtt.on_connect()
def connect(client, flags, rc, properties):
    fast_mqtt.client.subscribe("TGR_17") #subscribing mqtt topic
    print("Connected: ", client, flags, rc, properties)

@fast_mqtt.subscribe("TGR_17")
async def message_to_topic(client, topic, payload, qos, properties):
    print("Received message to specific topic: ", topic, payload.decode())
    message = payload.decode()
    json_message = json.loads(message)
    if json_message["height"] == "invalid" or  json_message["height"] == 0 :
        return 0
    try: 
        json_message["count"] == json_message["count"]+1
        return await add_height(json_message),"success"
    except Exception as e:
        print(f"Error adding data to MongoDB: {e}")

@fast_mqtt.on_disconnect()
def disconnect(client, packet, exc=None):
    print("Disconnected")

#@fast_mqtt.on_subscribe()
#def subscribe(client, mid, qos, properties):
#    print("subscribed", client, mid, qos, properties)


@router.get("/", response_description="test publish to mqtt")
async def publish_hello():
    counting = await retrieve_heights()
    print(len(counting))
    jsont = {
        "cmd":"getdata", 
        "counting":len(counting)+1
    }
    fast_mqtt.publish("TGR_17/h2o/cmd",jsont) #publishing mqtt topic
    return {"result": True,"message":"Published" }
