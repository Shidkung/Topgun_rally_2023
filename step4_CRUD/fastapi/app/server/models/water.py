from typing import Optional
from pydantic import BaseModel, Field


class WaterSchema(BaseModel):
    year: int = Field(..., gt=1990, lt=2030)
    date: int = Field(..., gt=0, lt=32)
    month: int = Field(..., gt=0, lt=13)
    w_height: float = Field(..., ge=0.0)
    w_cubic: float = Field(..., ge=0.0) 

    class Config:
        schema_extra = {
            "example": {
                "year": 2020,
                "month":12,
                "date":13,
                " w_height":121.1,
                "w_cubic":111.3
            }
        }
class heightSchema(BaseModel):
    height: float = Field(..., ge=0.0)
 
    class Config:
        schema_extra = {
            "example": {
                "height":121.1,
            }
        }

class QH3Schema(BaseModel):
    height: float = Field(..., ge=0.0)
    discharge: float = Field(..., ge=0.0)
    Day: int = Field(..., gt=0, lt=61)
    class Config:
        schema_extra = {
            "example": {
                "height":121.1,
                "Day":1,
                "discharge":743.35
            }
        }

class UpdateQH3Schema(BaseModel):
    height: float = Field(..., ge=0.0)
    discharge: float = Field(..., ge=0.0)
    Day: int = Field(..., gt=0, lt=61)
    class Config:
        schema_extra = {
            "example": {
                "height":121.1,
                "Day":1,
                "discharge":743.35
            }
        }
class UpdateWaterModel(BaseModel):
    year: Optional[int]
    date: Optional[int]
    month: Optional[int]
    w_height: Optional[float]
    w_cubic: Optional[float]

    class Config:
        schema_extra = {
            "example": {        
                "year": 2020,
                "month":12,
                "date":13,
                "w_height":121.1,
                "w_cubic":111.3,
            }
        }

class UpdateheightModel(BaseModel):
    height: Optional[float]

    class Config:
        schema_extra = {
            "example": {         
                "height":121.1,
            }
        }
def ResponseModel(data,message):
    return {
        "data": [data],
        "len" : len(data),
        "message":message
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}