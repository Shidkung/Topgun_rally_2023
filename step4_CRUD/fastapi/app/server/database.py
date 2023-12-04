import motor.motor_asyncio
from bson.objectid import ObjectId

MONGO_DETAILS = "mongodb://tesarally:contestor@mongoDB:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.water_data
db2 = client.mockupdata
db3 = client.heightdata
db4 = client.QH3data
height_collection = db3.get_collection("height")
QH3_collection = db4.get_collection("QH3")
waterdata = db2.get_collection("waterdata");
water_collection = database.get_collection("waters_collection")
def water_helper(water) -> dict:
    return {
        "id": str(water["_id"]),
        "year": water["year"],
        "month": water["month"],
        "date": water["date"],
        "w_height": water["w_height"],
        "w_cubic": water["w_cubic"],
    }
def height_helper(height)->dict:
    return{
        "id":str(height["_id"]),
        "count": height["count"],
        "height": height["height"]    
        }
def QH3_helper(height)->dict:
    return{
        "id":str(height["_id"]),
        "height": height["height"],
        "discharge": height["discharge"],
        "Day":height["Day"]    
        }
# Retrieve all waters present in the database
async def retrieve_waters():
    waters = []
    async for water in water_collection.find():
        waters.append(water_helper(water))
    return waters
async def retrieve_heights():
    waters = []
    async for water in height_collection.find():
        waters.append(height_helper(water))
    return waters

async def retrieve_QH3():
    waters = []
    async for water in QH3_collection.find():
        waters.append(QH3_helper(water))
    return waters
async def retrieve_waterss():
    waters = []
    async for water in waterdata.find():
        waters.append(water)
    return waters

# Add a new water into to the database
async def add_water(water_data: dict) -> dict:
    water = await water_collection.insert_one(water_data)
    new_water = await water_collection.find_one({"_id": water.inserted_id})
    return water_helper(new_water)

async def add_QH3(QH3_data: dict) -> dict:
    water = await QH3_collection.insert_one(QH3_data)
    new_water = await QH3_collection.find_one({"_id": water.inserted_id})
    return  QH3_helper(new_water)

async def add_height(height_data: dict) -> dict:
    water = await height_collection.insert_one(height_data)
    new_water = await water_collection.find_one({"_id": water.inserted_id})
    return height_helper(new_water)
# Retrieve a water data with a matching ID
async def retrieve_water(id: str) -> dict:
    water = await water_collection.find_one({"_id": ObjectId(id)})
    if water:
        return water_helper(water)

async def retrieve_waters(id: str) -> dict:
    water = await water_collection.find_one({"_id": ObjectId(id)})
    if water:
        return water_helper(water)
# Update a water with a matching ID
async def update_water(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    water = await water_collection.find_one({"_id": ObjectId(id)})
    if water:
        updated_water = await water_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_water:
            return True
        return False


# Delete a water from the database
async def delete_water(id: str):
    water = await water_collection.find_one({"_id": ObjectId(id)})
    if water:
        await water_collection.delete_one({"_id": ObjectId(id)})
        return True
