import requests
import json
from fastapi import APIRouter 

from server.models.water import (
    ErrorResponseModel,
    ResponseModel,
    UpdateWaterModel
)
from server.database import (
    add_water,
    delete_water,
    retrieve_water,
    retrieve_waters,
    update_water,
)
router = APIRouter()

@router.get("/{id}", response_description="water data retrieved")
async def get_mockup_data(id):
    #url = 'http://192.168.10.159/v1/'+str(id)
    
    url = 'http://192.168.1.3:7078/'+id#/'+str(id)
    mockup = requests.get(url)
    if mockup:
        message = mockup.json()
        message = message[0]
        time = message['w_date'].split("T")[0].split("-")
        Object: UpdateWaterModel = {
            "year": time[0],
            "date": time[1],
            "month":time[2],
            "w_height": message["w_height"],
            "w_cubic": message["w_cubic"]
        }
        return await add_water(Object),ResponseModel(str(mockup.text), "API data id:" +str(id) +" retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "data doesn't exist.")