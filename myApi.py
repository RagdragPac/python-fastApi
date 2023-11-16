import os
import requests

from fastapi import FastAPI, Path
from fastapi.responses import Response
from fastapi import Request
from fastapi import HTTPException
from fastapi import responses
from pydantic import BaseModel
from typing import List

class Message(BaseModel) :
    message: str

    class Config :
        schema_extra = {
            'example': [{
                'message' : 'test'
            }]
        }

class Ingredient(BaseModel):
    name: str

class Food(BaseModel) : 
    name : str
    price : int
    calories : str
    ingredients: List[Ingredient]

myFastApi = FastAPI()

foodData = {
    "324" : {
        "name": "hamburger",
        "price": "10",
        "calories": "380kcal",
        "ingredients": [
            {"name": "bun"},
            {"name": "cheese"},
            {"name": "pickles"},
            {"name": "patty"},
            {"name": "bun"},
        ]
    }
}


@myFastApi.get("/")
def test_init() :
    return {"name" : "test"}

@myFastApi.get("/getAllFoodData")
def get_all_food_data() :
    return foodData

@myFastApi.get("/get-food/{food_id}")
def get_specific_food_data(food_id: str = Path(..., description="The id of food that you want to view")) :
    return foodData.get(food_id, {"Data": "Not Found"})

@myFastApi.get("/get-food-byName")
def get_food_by_name(foodName: str) :
    for foodId, foodInfo in foodData.items():
        if foodInfo["name"] == foodName:
            return {foodId: foodInfo}
    return {"Data": "Not Found"}

@myFastApi.post("/add-food/{food_id}")
def add_food_data(food_id: str, food: Food) :
    if food_id in foodData:
        return {"Error": "Food Exist"}

    foodData[food_id] = food.dict()
    return {"message": "Food added successfully", "food_id": food_id}

@myFastApi.put("/update-food/{food_id}", responses={404: {'model' : Message}})
def udpate_food_data(food_id: str, food: Food) :
    responses
    if food_id not in foodData :
        raise HTTPException(status_code=404, detail=Message(message="Food Not Found"))
    
    foodData[food_id] = food.dict()
    return {"message": "Food updated successfully", "food_id": food_id}

@myFastApi.delete("/delete-food/{food_id}", responses={404: {'model' : Message}})
def delete_food_data(food_id: str) :
    responses
    if food_id not in foodData :
        raise HTTPException(status_code=404, detail=Message(message="Food Not Found"))
    
    del foodData[food_id]
    return {"message": "Food deleted sucessfully", "food_id": food_id}