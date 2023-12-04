from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from server.database import (
    add_water,
    delete_water,
    retrieve_water,
    retrieve_waters,
    update_water,
    retrieve_heights,
    add_QH3
)
from server.models.water import (
    ErrorResponseModel,
    ResponseModel,
    WaterSchema,
    UpdateWaterModel,QH3Schema,UpdateQH3Schema
)

router = APIRouter()

@router.post("/", response_description="Water data added into the database")
async def add_water_data(water: WaterSchema = Body(...)):
    water = jsonable_encoder(water)
    new_water = await add_water(water)
    return ResponseModel(new_water, "Water added successfully.")

@router.get("/", response_description="Waters retrieved")
async def get_waters():
    waters = await retrieve_waters()
    if waters:
        return ResponseModel(waters)
    return ResponseModel(waters, "Empty list returned")
@router.post("/addHS3",response_description="Waters retrieved")
async def add_QH3_data(QH3: QH3Schema = Body(...)):
    QH3 = jsonable_encoder(QH3)
    new_water = await add_QH3(QH3)
    return ResponseModel(new_water,"success")

@router.get("/heights", response_description="Waters retrieved")
async def get_waters():
    waters = await retrieve_heights()
    if waters:
        return ResponseModel(waters,"gets data")
    
    return ResponseModel(waters, "Empty list returned")
@router.get("/{id}", response_description="Water data retrieved")
async def get_water_data(id):
    water = await retrieve_water(id)
    if water:
        return ResponseModel(water, "Water data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Student doesn't exist.")

@router.put("/{id}")
async def update_water_data(id: str, req: UpdateWaterModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_water = await update_water(id, req)
    if updated_water:
        return ResponseModel(
            "Water with ID: {} name update is successful".format(id),
            "Water name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the water data.",
    )


@router.delete("/{id}", response_description="Water data deleted from the database")
async def delete_water_data(id: str):
    deleted_water = await delete_water(id)
    if deleted_water:
        return ResponseModel(
            "Water with ID: {} removed".format(id), "Water deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Water with id {0} doesn't exist".format(id)
    )
